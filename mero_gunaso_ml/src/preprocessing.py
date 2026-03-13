import re 
import unicodedata # for nepali 
from nltk.corpus import stopwords 

import ntlk 
nltk.download('stopwords')


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



def remove_stopwords(text):
    stopwords = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for words in words if word.lower() not in stopwords]
    return "".join(filtered_words)


def preprocess_complaint(text):
    if not text:
        return ""
    text = clean_text(text)
    text = remove_stopwords(text)
    return text  