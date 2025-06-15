import os
import pandas as pd
import uuid
from dotenv import load_dotenv
from pathlib import Path
from time import sleep

from src.utils.omdb_client import OmdbClient
from src.oracle_connection import OracleConnector

load_dotenv()


class MovieLoader:
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self.omdb = OmdbClient()

    def get_first_100_movies(self) -> list[tuple]:
        try:
            df = pd.read_csv(self.csv_path).dropna(subset=["title"])
            unique_titles = df["title"].drop_duplicates().head(100).tolist()
            movie_records = []

            for i, title in enumerate(unique_titles, start=1):
                print(f"[INFO] ({i}/100) Processing: {title}")
                movie_data = self.omdb.get_movie(title)
                if movie_data:
                    movie_records.append(
                        (
                            str(uuid.uuid4()),
                            movie_data["title"],
                            movie_data["year"],
                            movie_data["genre"],
                            movie_data["director"],
                        )
                    )
                sleep(0.25)

            return movie_records

        except Exception as e:
            print(f"[ERROR] Failed to extract movies: {e}")
            return []

    def insert_movies(self, movies: list[tuple]):
        insert_query = """
            INSERT INTO dim_movies (movie_id, title, year, genre, director)
            VALUES (:1, :2, :3, :4, :5)
        """
        with OracleConnector() as db:
            try:
                db.executemany(insert_query, movies)
                print(f"[INFO] Inserted {len(movies)} movies.")
            except Exception as e:
                print(f"[ORACLE ERROR] Insert failed: {e}")

    def run(self):
        movies = self.get_first_100_movies()
        if movies:
            self.insert_movies(movies)
        else:
            print("[INFO] No movie records to insert.")


def main():
    csv_path = Path(os.getenv("CSV_PATH"))
    loader = MovieLoader(csv_path)
    loader.run()


if __name__ == "__main__":
    main()
