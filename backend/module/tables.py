from pandas import DataFrame
import nltk


def get_word_freq(df: DataFrame, column: str) -> DataFrame:

    all_text = ""
    for i in df[column]:
        all_text += (
            " "
            + str(i)
            .strip()
            .replace("\n", " ")
            .replace("\t", " ")
            .replace("...", " ")
            .lower()
        )

    text = nltk.word_tokenize(all_text)
    fdist5 = nltk.FreqDist(text)
    freq = {}
    for w in set(text):
        if len(w) > 5 and fdist5[w] > 5:
            freq[fdist5[w]] = w

    keys = sorted(freq, reverse=True)

    list_text_pd = []
    for i in keys:
        if i > 50:
            list_text_pd.append([freq[i], i])

    return DataFrame(list_text_pd, columns=["Label", "Count"])


def get_rating(df: DataFrame) -> list:
    rating_number = df['rating'].dropna()\
                                    .unique()\
                                    .tolist()

    rating_number = [int(i) for i in rating_number]
    rating_number.sort()

    rating_count = df['rating'].value_counts().tolist()

    data = {
        'rating_count': rating_count,
        'rating_number': rating_number        
    }
    print(data)
    return data

def get_reaction(df: DataFrame) -> list:
    reaction_number = df['reaction'].dropna()\
                                    .unique()\
                                    .tolist()

    reaction_number.sort()
    reaction_count = df['reaction'].value_counts().tolist()

    data = {
        'reaction_count': reaction_count,
        'reaction_number': reaction_number        
    }
    print(df['reaction'].value_counts(sort=False),reaction_number, reaction_count)
    return data