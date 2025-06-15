import os
import re
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def normalize_title(title: str) -> str:
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s{2,}", " ", title)
    return title.strip()

class OmdbClient:
    def __init__(self):
        self.api_key = os.getenv("OMDB_API_KEY")
        self.base_url = "https://www.omdbapi.com/"

    def get_movie(self, title: str) -> dict | None:
        title = normalize_title(title)
        params = {"apikey": self.api_key, "t": title}

        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("Response") == "True":
                    if data.get("Type") != "movie":
                        print(f"[OMDb] Skipped non-movie: {title}")
                        return None
                    return {
                        "title": data.get("Title"),
                        "year": data.get("Year"),
                        "genre": data.get("Genre"),
                        "director": data.get("Director")
                    }
                else:
                    print(f"[OMDb] Movie not found: {title}")
            else:
                print(f"[OMDb] Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[OMDb ERROR] Failed to fetch {title}: {e}")

        return None

def main():
    client = OmdbClient()
    movie = client.get_movie("Spider-Man: Homecoming")
    print(movie)

if __name__ == "__main__":
    main()
