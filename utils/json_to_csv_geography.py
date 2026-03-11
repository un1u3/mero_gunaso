import csv
import json
from pathlib import Path

ML_DIR = Path(__file__).resolve().parents[1]

# input file
json_file = ML_DIR / "data" / "geography" / "en.json"

# output file
output_file = ML_DIR / "data" / "geography" / "geography.csv"


def _iter_children(node):
    if node is None:
        return []
    if isinstance(node, list):
        return node
    if isinstance(node, dict):
        return node.values()
    raise TypeError(f"Expected list or dict, got {type(node).__name__}")

# Load JSON
with open(json_file, encoding="utf-8") as f:
    data = json.load(f)

rows = []

# Loop through provinces, districts, municipalities, wards
for province in data:
    province_name = province["name"]
    for district in _iter_children(province.get("districts")):
        district_name = district["name"]
        for muni in _iter_children(district.get("municipalities")):
            municipality_name = muni["name"]
            for ward_number in muni.get("wards", []):
                rows.append([ward_number, municipality_name, district_name, province_name])

# write to csv
output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ward_number", "municipality", "district", "province"])
    writer.writerows(rows)

print(f"CSV created successfully with {len(rows)} rows -> {output_file}")
