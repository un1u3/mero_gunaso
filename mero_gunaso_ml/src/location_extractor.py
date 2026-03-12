from __future__ import annotations
import re
from pathlib import Path
from typing import Optional
import pandas as pd
import spacy
from fuzzywuzzy import fuzz  # match words even if spelling is wrong

class LocationExtractor:
    def __init__(self,
        geo_data_path: str | Path | None = None,
        nlp_model= 'en_core_web_sm'):
        if geo_data_path is None:
            geo_data_path = (
                Path(__file__).resolve().parents[1]
                / "data"
                / "geography"
                / "geography.csv"
            )
        self.geo_df = pd.read_csv(geo_data_path)
        # what nlp_model will do : " near pashupatitinath temple " to Pashupatinath temple as loaction
        try:
            self.nlp = spacy.load(nlp_model) # testinng each and hardcoding laater 
        except OSError:
            # Keep the extractor usable even if the model isn't installed.
            self.nlp = spacy.blank("en")
        self.wards = set(self.geo_df['ward_number'])
        self.municipalities = self.geo_df['municipality'].unique()
        # Backwards-compat alias (typo).
        self.muncipalities = self.municipalities
        # hard codind province beacause data doesnot contain 2 and mistake of 7 
        self.provinces = [
                            "koshi",
                            "madhesh",
                            "bagmati",
                            "gandaki",
                            "lumbini",
                            "karnali",
                            "sudurpashchim"
                        ]

        # abbervation for famous  munciaplities 
        self.abbr_map = {
            'BMP':'Bimeshwor Muncipality', #best muncipalityy:: I live here 
            "KMC": "Kathmandu Metropolitan City", #
            "LMC": "Lalitpur Metropolitan City", 
            # yk something is missing :), 
        }

    def extract_ward(self,text):
        # eg road damage in ward3 
        # capture number after ward keyword(can accept dashes)
        match = re.search(r'ward\s*-?\s*(\d+)', text.lower())
        # inp : ward 3 op : 3 
        if match:
            ward = int(match.group(1))

            if ward in self.wards:
                return ward
        return None

    def extract_province(self, text):
        text = text.lower()
        for province in self.provinces:
            if province.lower() in text:
                return province
        return None

    def extract_municipality(self, text) -> Optional[str]:
        for abbr, full in self.abbr_map.items():
            if abbr.lower() in text.lower():
                return full

        # fuzzy helsp to to match even if speelling is not right 
        words  = text.split()
        best_score = 0
        best_match: Optional[str] = None

        for word in words:
            for municipality in self.municipalities:
                # the fuzz.ratio gives similarity score between 2 words 
                # why we are doing this ,
                # we are trying to extract location from the user input
                # user spelling might not be correct or anythign so we are taking a guess 
                # acc to similarity 
                score = fuzz.ratio(word.lower(), str(municipality).lower())
                if score > best_score:
                    best_score = score
                    best_match = str(municipality)

        if best_score > 80:
            return best_match
        return None

    # Backwards-compat method name (typo).
    def extract_muncipality(self, text):
        return self.extract_municipality(text)


    def extract_landmarks(self, text):
        doc = self.nlp(text)
        landmarks = []
        for ent in doc.ents:
            if ent.label_ in ['LOC',"FAC"]:
                landmarks.append(ent.text)
        return landmarks
    
    def extract_all(self, text):
        return {
            'ward': self.extract_ward(text),
            'municipality': self.extract_municipality(text),
            'landmarks': self.extract_landmarks(text),
            'remaining_text':text
        }

if __name__ == "__main__":
    extractor = LocationExtractor()
    text  = 'Large potholes near Pashupatinath Temple in Ward 3, KMC Bagmati'
    result = extractor.extract_all(text)
    print(result) 
