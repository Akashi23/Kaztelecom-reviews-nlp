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
