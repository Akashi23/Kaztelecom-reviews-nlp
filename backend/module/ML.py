import string
import nltk
import joblib
from pandas import DataFrame
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

def clean_text(text):
    stemmer = SnowballStemmer("russian") 
    # lower text
    text = text.lower().replace('\n', '').replace('\t', '')
    # tokenize text and remove puncutation
    text = [word.strip(string.punctuation) for word in text.split(" ")]
    # remove words that contain numbers
    text = [word for word in text if not any(c.isdigit() for c in word)]
    # remove stop words
    stop = stopwords.words('russian')
    text = [x for x in text if x not in stop]
    # remove empty tokens
    text = [t for t in text if len(t) > 0]
    # pos tag text
    pos_tags = pos_tag(text)
    # lemmatize text
    text = [stemmer.stem(word) for word in text]
    text = [t for t in text if len(t) > 1]
    # join all
    text = " ".join(text)
    return(text)

def train_model_classification(df: DataFrame) -> dict:

    df["text"] = df["text"].apply(lambda x: clean_text(str(x)))

    cv = CountVectorizer(max_features = 1500)
    X = cv.fit_transform(df['text']).toarray()
    y = df['reaction']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15, random_state = 0)
    print('Training ..........')
    classifier = XGBClassifier()
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    conf_matrix = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    text_for_test = """Добрый день! Спасибо за информацию,
             благодаря подобным обращениям 
             мы делаем наш сервис лучше."""

    text_test = cv.transform([clean_text(str(text_for_test))]).toarray()
    text_test_pred = classifier.predict(text_test)
    joblib.dump(classifier, 'data/model.sav')
    joblib.dump(cv, 'data/count_vect.sav')
    return {
        'confusion matrix': conf_matrix.tolist(),
        'accuracy': float(accuracy),
        'text for test': text_for_test,
        'text test prediction': text_test_pred.tolist()[0]
    }

def predict(text: str) -> int:
    cv = joblib.load('data/count_vect.sav')
    model = joblib.load('data/model.sav')
    x_text_test = cv.transform([clean_text(str(text))]).toarray()
    return model.predict(x_text_test).tolist()[0]

