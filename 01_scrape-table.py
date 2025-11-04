import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = "https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Albums/500"

# Add a User-Agent to avoid 403 errors
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/119.0.0.0 Safari/537.36"
}

# Fetch page
res = requests.get(url, headers=headers)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")

# Find the main wikitable
table = soup.find("table", {"class": "wikitable"})

# Extract header names
headers = [th.get_text(strip=True) for th in table.find_all("th")]

# Extract all rows
rows = []
for tr in table.find_all("tr")[1:]:
    cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
    if cells:
        rows.append(cells)

# Convert to DataFrame
df = pd.DataFrame(rows, columns=headers[:len(rows[0])])

# Clean Album and Artist
df["Album"] = df["Album"].str.replace(r"\s*\(.*?\)", "", regex=True).str.strip()
df["Artist"] = df["Artist(s)"].str.replace(r"\s*\(.*?\)", "", regex=True).str.strip()

print(df.head())
df.to_csv("./data/albums_500.csv", index=False)
print("Saved to albums_500.csv")