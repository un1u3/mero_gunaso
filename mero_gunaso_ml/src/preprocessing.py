import re
import unicodedata

from nltk.corpus import stopwords as nltk_stopwords


def clean_text(text: str) -> str:
    if not text:
        return ""

    # Unicode normalization (important for nepali + mixed text)
    text = unicodedata.normalize("NFKC", text)
    # remove urls   
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # remove emails
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '', text)
    # remove pn 
    text = re.sub(r'\b\d{7,15}\b', '', text)
    # rm specical chars
    text = re.sub(r'[^0-9A-Za-z\u0900-\u097F\s\.,!?]', '', text)
    # rm extra white space 
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing spaces
    text = text.strip()
    return text



def remove_stopwords(text: str) -> str:
    if not text:
        return ""

    try:
        english_stopwords = set(nltk_stopwords.words("english"))
    except LookupError:
        return text

    words = text.split()
    filtered_words = [
        word for word in words if word.lower() not in english_stopwords
    ]
    return " ".join(filtered_words)


def preprocess_complaint(text: str) -> str:
    if not text:
        return ""
    text = clean_text(text)
    text = remove_stopwords(text)
    return text  
