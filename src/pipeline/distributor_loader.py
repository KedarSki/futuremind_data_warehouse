import os
import pandas as pd
import uuid
from dotenv import load_dotenv
import sys
from pathlib import Path
from src.oracle_connection import OracleConnector

load_dotenv()

class DistributorLoader:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def get_unique_distributors(self):
        try:
            df = pd.read_csv(self.csv_path)
            distributors = df['distributor'].dropna().unique()
            distributor_list = [(str(uuid.uuid4()), name) for name in distributors]
            return distributor_list
        except Exception as e:
            print(f"[ERROR] Failed to extract distributors: {e}")
            return []

    def insert_distributors(self, distributors):
        insert_query = """
            INSERT INTO dim_distributors (distributor_id, name)
            VALUES (:1, :2)
        """
        with OracleConnector() as db:
            try:
                db.executemany(insert_query, distributors)
                print(f"[INFO] Inserted {len(distributors)} distributors.")
            except Exception as e:
                print(f"[ORACLE ERROR] Insert failed: {e}")

    def run(self):
        distributors = self.get_unique_distributors()
        if distributors:
            self.insert_distributors(distributors)
        else:
            print("[INFO] No distributors found or failed to read CSV.")

def main():
    csv_path = Path(os.getenv("CSV_PATH"))
    loader = DistributorLoader(csv_path)
    loader.run()

if __name__ == "__main__":
    main()