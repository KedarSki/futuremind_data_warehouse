import oracledb
import os
from dotenv import load_dotenv 

class OracleConnector:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv("ORACLE_USERNAME")
        self.password = os.getenv("ORACLE_PASSWORD")
        self.dsn = os.getenv("ORACLE_DSN")
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = oracledb.connect(
                user = self.username,
                password = self.password,
                dsn = self.dsn
            )
            self.cursor = self.connection.cursor()
            return self
        except oracledb.Error as e:
            print(f"[ORACLE ERROR] Connection failed: {e}")
            raise

    def __exit__(self, exc_type, exc_value, exc_tb):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.commit()
                self.connection.close()
        except oracledb.Error as e:
            print(f"[ORACLE ERROR] Cleanup failed: {e}")
            raise

    def execute(self, query: str, params: tuple = None):
        try:
            self.cursor.execute(query, params or ())
        except oracledb.Error as e:
            print(f"[ORACLE ERROR] Execute failed: {e}")
            raise
    
    def executemany(self, query: str, data: list[tuple]):
        try:
            self.cursor.executemany(query, data)
        except oracledb.Error as e:
            print(f"[ORACLE ERROR] Batch insert failed: {e}")
            raise 
    
def main():
    with OracleConnector() as db:
        db.execute("SELECT table_name FROM user_tables")
        for row in db.cursor:
            print(row)

if __name__ == "__main__":
    main()

    
