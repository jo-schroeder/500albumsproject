import pandas as pd
import time
from SPARQLWrapper import SPARQLWrapper, JSON

# Initialize SPARQL endpoint with a proper User-Agent
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)
sparql.agent = "JoannaRollingStone500Bot/1.0 (https://github.com/yourusername/500albumsproject; email@example.com)"

# --- Helper functions ---
def safe_sparql_literal(text):
    """Escape special characters for SPARQL."""
    if not isinstance(text, str) or not text.strip():
        return None
    return text.replace("\\", "\\\\").replace('"', '\\"').strip()

def query_album(album_title, artist_name=None):
    album_title_safe = safe_sparql_literal(album_title)
    if not album_title_safe:
        return {
            "wikidata_qid": None,
            "artist": None,
            "release_date": None,
            "album_art": None,
            "genre": None,
        }

    query = f"""
    SELECT ?album ?albumLabel ?artistLabel ?releaseDate ?image ?genreLabel WHERE {{
      ?album wdt:P31 wd:Q482994;
             rdfs:label "{album_title_safe}"@en.
      OPTIONAL {{ ?album wdt:P175 ?artist. }}
      OPTIONAL {{ ?album wdt:P577 ?releaseDate. }}
      OPTIONAL {{ ?album wdt:P18 ?image. }}
      OPTIONAL {{ ?album wdt:P136 ?genre. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 5
    """

    try:
        sparql.setQuery(query)
        results = sparql.query().convert()
        bindings = results["results"]["bindings"]
        if not bindings:
            return {
                "wikidata_qid": None,
                "artist": None,
                "release_date": None,
                "album_art": None,
                "genre": None,
            }

        row = bindings[0]
        qid = row["album"]["value"].split("/")[-1]

        # Get album art from P18 if available
        image_url = row.get("image", {}).get("value")

        return {
            "wikidata_qid": qid,
            "artist": row.get("artistLabel", {}).get("value"),
            "release_date": row.get("releaseDate", {}).get("value"),
            "album_art": image_url,
            "genre": row.get("genreLabel", {}).get("value"),
        }

    except Exception as e:
        print(f"Error querying '{album_title}': {e}")
        return {
            "wikidata_qid": None,
            "artist": None,
            "release_date": None,
            "album_art": None,
            "genre": None,
        }

# --- Main Loop ---

# Read CSV safely with fallback encoding
albums = pd.read_csv("./data/albums_500.csv", encoding="latin1", keep_default_na=False)

results = []
for i, row in albums.iterrows():
    title = row.get("Album", "")
    artist = row.get("Artist", "")
    info = query_album(title, artist)
    results.append(info)
    print(f"[{i+1}/{len(albums)}] {title} — done.")
    time.sleep(1)  # polite 1-second delay per request

# Merge results with original CSV
wikidata_df = pd.DataFrame(results)
enriched_df = pd.concat([albums, wikidata_df], axis=1)

# Save enriched CSV
enriched_df.to_csv("albums_500_wikidata_enriched.csv", index=False)
print("✅ Saved enriched data to albums_500_wikidata_enriched.csv")

