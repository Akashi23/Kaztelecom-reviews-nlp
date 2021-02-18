import json
import uvicorn
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from module.tables import get_word_freq, get_rating, get_reaction
from module.ML import train_model_classification, predict


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dataset = pd.read_csv("../dataset_full/kazakhtel_review.csv")
dataset_nlp = pd.read_csv("../dataset_nlp/kazakhtel_review_reaction.csv")


@app.get("/features/")
async def features(select: str):
    # try:
        if select == "freq,title":
            df_title = get_word_freq(dataset, "title")
            return {'word_title_freq': df_title.values.tolist()}

        elif select == "freq,text":
            df_text = get_word_freq(dataset, "text")
            return {'word_text_freq': df_text.values.tolist()}

        elif select.split(',')[0] == "rating":
            return get_rating(dataset)
        
        elif select.split(',')[0] == "reaction":
            return get_reaction(dataset)
            
        else:
            data = {}
            for feature in select.split(','):
                data[feature] = dataset[feature].dropna().tolist()
            return data
    # except:
    #     print("except")
    #     return {"error": "features are not selectable"}


@app.get("/train/")
async def train(APIKEY: str):
    try:
        if APIKEY == "123":
            return train_model_classification(dataset_nlp)
        else:
            return {"error": "APIKEY is not correct"}
    except:
        return {"error": "train Error"}


@app.post("/predict")
async def prediction(text: dict):
    try:
        return predict(str(text["text"]))
    except:
        return {"error": "prediction error"}


@app.get("/keywords/")
async def detect_keywords(keywords: str):
    # try:
        list_keywords = keywords.split(",")
        df_title = get_word_freq(dataset, "title")
        df_text = get_word_freq(dataset, "text")

        df_keywords = pd.DataFrame(columns=["Label", "Count"])
        for keyword in list_keywords:
            filter1 = keyword == df_title["Label"]
            filter2 = keyword == df_text["Label"]
            df1 = df_title.where(filter1, None).dropna()
            df2 = df_text.where(filter2, None).dropna()
            if df1.empty or df2.empty:
                continue
            cond = df1["Label"].sort_index(inplace=True) == df2["Label"].sort_index(
                inplace=True
            )
            if cond:
                sum_mentioning = df1["Count"].iloc[0] + df2["Count"].iloc[0]
                df_sum_mentioning = pd.DataFrame(
                    [[keyword, sum_mentioning]], columns=["Label", "Count"]
                )
                df_keywords = pd.concat(
                    [df_sum_mentioning, df_keywords], ignore_index=True
                )
            else:
                df_keywords = pd.concat(
                    [pd.concat([df1, df2], ignore_index=True), df_keywords],
                    ignore_index=True,
                )

        return json.loads(df_keywords.to_json())
    # except:
    #     return {"error": "1"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=3000, reload=True)
