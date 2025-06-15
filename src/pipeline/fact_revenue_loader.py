import os
import re
import pandas as pd
import uuid
from dotenv import load_dotenv
from pathlib import Path
from src.oracle_connection import OracleConnector

load_dotenv()

def normalize_title(title: str) -> str:
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s{2,}", " ", title)
    return title.strip().lower()

def normalize_distributor(name: str) -> str:
    return name.strip().lower()

class FactRevenueLoader:
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path

    def load_lookup_maps(self):
        movie_map = {}
        distributor_map = {}

        with OracleConnector() as db:
            db.execute("SELECT title, movie_id FROM dim_movies")
            for title, movie_id in db.cursor:
                movie_map[normalize_title(title)] = movie_id

            db.execute("SELECT name, distributor_id FROM dim_distributors")
            for name, distributor_id in db.cursor:
                distributor_map[normalize_distributor(name)] = distributor_id

        return movie_map, distributor_map

    def prepare_fact_records(self, movie_map, distributor_map):
        try:
            df = pd.read_csv(self.csv_path)
            records = []

            for _, row in df.iterrows():
                title = normalize_title(str(row["title"]))
                distributor = normalize_distributor(str(row["distributor"]))

                movie_id = movie_map.get(title)
                distributor_id = distributor_map.get(distributor)

                if movie_id and distributor_id:
                    try:
                        revenue = float(row["revenue"])
                        revenue_date = pd.to_datetime(row["date"], errors='coerce').date()
                        if pd.notna(revenue_date):
                            records.append((str(uuid.uuid4()), movie_id, distributor_id, revenue, revenue_date))
                    except Exception as e:
                        print(f"[WARN] Invalid record skipped: {e}")
                else:
                    print(f"[WARN] Movie or distributor not found: {row['title']} / {row['distributor']}")

            return records

        except Exception as e:
            print(f"[ERROR] Failed to prepare FACT_REVENUE records: {e}")
            return []

    def insert_records(self, records, batch_size=100):
        insert_query = """
            INSERT INTO fact_revenue (id, movie_id, distributor_id, revenue, revenue_date)
            VALUES (:1, :2, :3, :4, :5)
        """
        with OracleConnector() as db:
            for i in range(0, len(records), batch_size):
                batch = records[i : i + batch_size]
                try:
                    db.executemany(insert_query, batch)
                    print(f"[INFO] Inserted batch {i // batch_size + 1} with {len(batch)} records.")
                except Exception as e:
                    print(f"[ORACLE ERROR] Failed to insert batch {i // batch_size + 1}: {e}")

    def run(self):
        movie_map, distributor_map = self.load_lookup_maps()
        fact_records = self.prepare_fact_records(movie_map, distributor_map)
        if fact_records:
            self.insert_records(fact_records)
        else:
            print("[INFO] No records to insert into FACT_REVENUE.")

def main():
    csv_path = Path(os.getenv("CSV_PATH"))
    loader = FactRevenueLoader(csv_path)
    loader.run()

if __name__ == "__main__":
    main()
