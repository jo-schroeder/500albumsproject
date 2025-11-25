import csv
import json

csv_file = "./data/albums_500_wikidata.csv"
json_file = "./data/albums_500_wikidata.json"

with open(csv_file, "r", encoding="latin-1") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2, ensure_ascii=False)