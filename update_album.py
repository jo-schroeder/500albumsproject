import sys
import json
import pandas as pd

# get row_number from command line
if len(sys.argv) < 2:
    print("Usage: python update_album.py <row_number>")
    sys.exit(1)

try:
    row_number = int(sys.argv[1])
except ValueError:
    print("row_number must be an integer")
    sys.exit(1)

# load full CSV (with accent marks)
csv_file = "data/albums_500_wikidata.csv"
try:
    df = pd.read_csv(csv_file, encoding="latin-1")  # handles accents
except FileNotFoundError:
    print(f"CSV file not found: {csv_file}")
    sys.exit(1)

# check row_number is in range
if row_number < 1 or row_number > len(df):
    print(f"row_number must be between 1 and {len(df)}")
    sys.exit(1)

# select the album (convert 1-based to 0-based index)
album_row = df.iloc[row_number - 1]

# build album dict, handle missing columns
album_dict = {
    "Album": album_row.get("Album", "Unknown"),
    "Artist": album_row.get("Artist", "Unknown"),
    "release_date": album_row.get("release_date", ""),
    "genre": album_row.get("genre", ""),
    "album_art": album_row.get("album_art", "")
}

# write JSON for HTML
output_file = "album.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(album_dict, f, indent=2, ensure_ascii=False)

print(f"album.json updated with row_number {row_number} ({album_dict['Album']} — {album_dict['Artist']})")
