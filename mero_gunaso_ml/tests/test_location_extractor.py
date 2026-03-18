from types import SimpleNamespace

import pytest

from mero_gunaso_ml.src.location_extractor import LocationExtractor


def make_entity(text, label):
    return SimpleNamespace(text=text, label_=label)


def make_doc(*entities):
    return SimpleNamespace(ents=list(entities))


@pytest.fixture
def extractor(tmp_path):
    csv_path = tmp_path / "geography.csv"
    csv_path.write_text(
        "\n".join(
            [
                "ward_number,municipality,district,province",
                "1,Kathmandu Metropolitan City,Kathmandu,Bagmati Province",
                "3,Kathmandu Metropolitan City,Kathmandu,Bagmati Province",
                "5,Pokhara,Kaski,Gandaki Province",
            ]
        ),
        encoding="utf-8",
    )
    return LocationExtractor(
        geo_data_path=csv_path,
        nlp_model="__missing_spacy_model__",
    )


def test_extract_ward_returns_known_ward(extractor):
    assert extractor.extract_ward("Road damage in ward 3") == 3


def test_extract_ward_returns_none_for_unknown_ward(extractor):
    assert extractor.extract_ward("Road damage in ward 9") is None


def test_extract_province_is_case_insensitive(extractor):
    assert extractor.extract_province("Issue reported in BAGMATI") == "bagmati"


def test_extract_municipality_expands_abbreviation(extractor):
    assert (
        extractor.extract_municipality("Problem in KMC ward 3")
        == "Kathmandu Metropolitan City"
    )


def test_extract_municipality_uses_fuzzy_match(extractor):
    assert extractor.extract_municipality("Pothole in Pokharaa") == "Pokhara"


def test_extract_muncipality_alias_uses_same_logic(extractor):
    assert extractor.extract_muncipality("Problem in KMC") == (
        "Kathmandu Metropolitan City"
    )


def test_extract_landmarks_keeps_only_loc_and_fac(extractor):
    extractor.nlp = lambda text: make_doc(
        make_entity("Pashupatinath Temple", "FAC"),
        make_entity("Kathmandu", "LOC"),
        make_entity("Ram", "PERSON"),
    )

    assert extractor.extract_landmarks("Near Pashupatinath Temple") == [
        "Pashupatinath Temple",
        "Kathmandu",
    ]


def test_extract_all_returns_expected_shape(extractor):
    extractor.nlp = lambda text: make_doc(
        make_entity("Pashupatinath Temple", "FAC")
    )
    text = "Large potholes near Pashupatinath Temple in ward 3, KMC Bagmati"

    assert extractor.extract_all(text) == {
        "ward": 3,
        "municipality": "Kathmandu Metropolitan City",
        "landmarks": ["Pashupatinath Temple"],
        "remaining_text": text,
    }
