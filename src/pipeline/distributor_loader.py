import sys
import os
import pandas as pd
import uuid
from dotenv import load_dotenv
from oracle_connection import OracleConnector



class DistributorLoader:
    def __init__(self, csv_path: str):
        load_dotenv()
        self.csv_path = csv_path

    def run():
        pass


def main():
    csv_path = os.getenv("CSV_PATH")
    loader = DistributorLoader(csv_path)
    loader.run()


if __name__ == "__main__":
    main()
