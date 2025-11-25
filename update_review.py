import sys
import json
import pandas as pd
import os

if len(sys.argv) < 2:
    print("Usage: python update_review.py '<row>/<emoji>/<haiku>'")
    sys.exit(1)

raw_input = sys.argv[1]

# --- Split only first 3 components ---
parts = raw_input.split("/", 2)

if len(parts) < 3:
    print("Input must be formatted like: row/emoji/haiku")
    sys.exit(1)

row_number_str, emoji, haiku = parts

try:
    row_number = int(row_number_str.strip())
except:
    print("Row number must be an integer.")
    sys.exit(1)

# --- Load metadata from CSV ---
csv_file = "data/albums_500_wikidata.csv"
df = pd.read_csv(csv_file, encoding="latin-1")

if row_number < 1 or row_number > len(df):
    print("Row number out of range.")
    sys.exit(1)

album_row = df.iloc[row_number - 1]

entry = {
    "row_number": row_number,
    "Album": album_row.get("Album", "Unknown"),
    "Artist": album_row.get("Artist", "Unknown"),
    "emoji": emoji.strip(),
    "haiku": haiku.strip()
}

# --- Load or initialize reviews.json ---
reviews_file = "reviews.json"
if os.path.exists(reviews_file):
    with open(reviews_file, "r", encoding="utf-8") as f:
        try:
            reviews = json.load(f)
        except json.JSONDecodeError:
            reviews = []
else:
    reviews = []

# --- Update existing entry or append new one ---
updated = False
for i, r in enumerate(reviews):
    if r["row_number"] == row_number:
        reviews[i] = entry
        updated = True
        break

if not updated:
    reviews.append(entry)

# Sort by album order
reviews.sort(key=lambda x: x["row_number"])

# --- Write back to JSON ---
with open(reviews_file, "w", encoding="utf-8") as f:
    json.dump(reviews, f, indent=2, ensure_ascii=False)

print(f"Updated review for #{row_number}: {entry['Album']} — {emoji}")
