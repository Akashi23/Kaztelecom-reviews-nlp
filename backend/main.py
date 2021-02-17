import json
import uvicorn
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from module.tables import get_word_freq
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
    try:
        if select == "freq,title":
            df_title = get_word_freq(dataset, "title")
            return json.loads(df_title.to_json())

        elif select == "freq,text":
            df_text = get_word_freq(dataset, "text")
            return json.loads(df_text.to_json())

        else:
            data = dataset[select.split(",")]
            return json.loads(data.to_json())
    except:
        return {"error": "features are not selectable"}

@app.get("/train/")
async def train(APIKEY: str):
    try:
        if APIKEY == '123':
            return train_model_classification(dataset_nlp)
        else:
            return {"error": "APIKEY is not correct"}
    except:
        return {"error": "train Error"}

@app.post("/predict")
async def prediction(text: dict):
    try:
        return predict(str(text['text']))
    except:
        return {"error": "prediction error"}

@app.get("/keywords/")
async def detect_keywords(keywords: str):
    try:
        list_keywords = keywords.split(",")
        df_title = get_word_freq(dataset, 'title')
        df_text = get_word_freq(dataset, 'text')
        
        df_keywords = pd.DataFrame(columns=['Label', 'Count'])
        for keyword in keywords:
            if keyword in df_text['Label']:
                df_keywords.append(df_text['Label'][keyword])

            if keyword in df_title['Label']:
                df_keywords.append(df_title['Label'][keyword])
        return json.loads(df_keywords.to_json())
    except:
        return {"error": "1"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=3000, reload=True)
