from types import SimpleNamespace
from unittest.mock import patch

from mero_gunaso_ml.src import preprocessing


def stopwords_with_words():
    return SimpleNamespace(words=lambda language: ["this", "is", "a", "the"])


def stopwords_with_error():
    def words(language):
        raise LookupError

    return SimpleNamespace(words=words)


def test_clean_text_returns_empty_string_for_empty_input():
    assert preprocessing.clean_text("") == ""


def test_clean_text_removes_urls_emails_phone_numbers_and_symbols():
    raw = (
        "Road damage near ward office. Visit https://example.com or email "
        "team@example.com. Call 9812345678. Thanks #urgent"
    )

    cleaned = preprocessing.clean_text(raw)

    assert "Road damage near ward office." in cleaned
    assert "Thanks urgent" in cleaned
    assert "http" not in cleaned
    assert "@" not in cleaned
    assert "9812345678" not in cleaned
    assert "#" not in cleaned


def test_remove_stopwords_removes_known_words():
    with patch.object(preprocessing, "nltk_stopwords", stopwords_with_words()):
        assert preprocessing.remove_stopwords("This is a test") == "test"


def test_remove_stopwords_returns_original_text_when_corpus_is_missing():
    with patch.object(preprocessing, "nltk_stopwords", stopwords_with_error()):
        assert preprocessing.remove_stopwords("Hello world") == "Hello world"


def test_preprocess_complaint_runs_cleaning_and_stopword_removal():
    with patch.object(preprocessing, "nltk_stopwords", stopwords_with_words()):
        text = "This is a road complaint at the bridge https://example.com"
        assert preprocessing.preprocess_complaint(text) == "road complaint at bridge"
