from src.location_extractor import LocationExtractor

def test_location_extractor():
    extractor = LocationExtractor(
        
    )
    text  = 'Large potholes near Pashupatinath Temple in Ward 3, KMC Bagmati'
    result = extractor.extract_all(text)
    print(result)    

test_location_extractor()