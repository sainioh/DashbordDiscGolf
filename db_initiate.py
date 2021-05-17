import sqlite3
import pandas as pd


class Database():
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.c = self.connection.cursor()

    def query_to_df(self, q):
        self.c.execute(q)
        temp_df = pd.read_sql_query(q, self.connection)
        # TEST HERE IF GOOD QUERY
        return temp_df

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()



with Database("discgolf.db") as db:
    try:
        testdf = db.query_to_df("SELECT * FROM averages")
    except:
        print("Failed to load data to dataframe")


