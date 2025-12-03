import sys
import json
import pandas as pd
from datetime import datetime
import os

# --- Get row_number from command line ---
if len(sys.argv) < 2:
    print("Usage: python update_album.py <row_number>")
    sys.exit(1)

try:
    row_number = int(sys.argv[1])
except ValueError:
    print("row_number must be an integer")
    sys.exit(1)

# --- Load CSV ---
csv_file = "data/albums_500_wikidata.csv"
if not os.path.exists(csv_file):
    print(f"CSV file not found: {csv_file}")
    sys.exit(1)

df = pd.read_csv(csv_file, encoding="latin-1")

if row_number < 1 or row_number > len(df):
    print(f"row_number must be between 1 and {len(df)}")
    sys.exit(1)

# --- Add 'date_started' column if missing ---
if 'date_started' not in df.columns:
    df['date_started'] = ""

# --- Update 'date_started' only if empty ---
current_date = datetime.now().isoformat()
if not df.at[row_number - 1, 'date_started']:
    df.at[row_number - 1, 'date_started'] = current_date
    print(f"Set date_started for row {row_number} to {current_date}")
else:
    current_date = df.at[row_number - 1, 'date_started']
    print(f"Row {row_number} already has date_started: {current_date}")

# --- Select the album row ---
album_row = df.iloc[row_number - 1]

# --- Build album dict for JSON ---
album_dict = {
    "row_number": int(album_row.get("#", 0)),
    "Album": album_row.get("Album", "Unknown"),
    "Artist": album_row.get("artist", "Unknown"),
    "release_date": album_row.get("release_date", ""),
    "genre": album_row.get("genre", ""),
    "album_art": album_row.get("album_art", ""),
    "date_started": current_date
}

# --- Write album.json ---
output_file = "album.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(album_dict, f, indent=2, ensure_ascii=False)

print(f"album.json updated with row_number {row_number} ({album_dict['Album']} — {album_dict['Artist']})")
print(f"Listening started: {current_date}")

# --- Write back updated CSV ---
df.to_csv(csv_file, index=False, encoding="latin-1")
print(f"CSV updated: {csv_file}")

if row_number > 1:
    next_row = df.iloc[row_number - 2]  # previous row

    next_album_dict = {
        "row_number": int(next_row.get("#", 0)),
        "Album": next_row.get("Album", "Unknown"),
        "Artist": next_row.get("artist", "Unknown"),
        "release_date": next_row.get("release_date", ""),
        "genre": next_row.get("genre", ""),
        "album_art": next_row.get("album_art", "")
    }

    with open("next_album.json", "w", encoding="utf-8") as f:
        json.dump(next_album_dict, f, indent=2, ensure_ascii=False)

    print(f"next_album.json updated (up next: {next_album_dict['Album']} — {next_album_dict['Artist']})")

else:
    # If row_number == 1, no "previous" album exists
    if os.path.exists("next_album.json"):
        os.remove("next_album.json")
    print("No next album (row_number = 1). Removed next_album.json if it existed.")

# --- Write back updated CSV ---
df.to_csv(csv_file, index=False, encoding="latin-1")
print(f"CSV updated: {csv_file}")