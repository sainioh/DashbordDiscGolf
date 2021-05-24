import sqlite3
import pandas as pd


class Database():
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.c = self.connection.cursor()

    def commit_changes(self):
        self.connection.commit()

    def query_to_df(self, q):
        self.c.execute(q)
        temp_df = pd.read_sql_query(q, self.connection)
        return temp_df

    def add_round(self, date, data):

        name = data[0]
        self.c.execute("""SELECT playerID FROM player WHERE playerName = ?;""", (name,))
        p_id = self.c.fetchall()[0][0]

        self.c.execute('''
                        INSERT INTO player_round ('playerID','date') VALUES(?,?);
                        ''', (p_id, date))

        _id = self.c.lastrowid
        self.commit_changes()
        return _id, p_id

    def add_score(self, c_ID, strokes, h_ID, p_id, _id):

        self.c.execute('''
                            INSERT INTO player_scores ('courseID','strokes','holeID', 'playerID', 'playerRoundID') VALUES(?,?,?,?,?)
                            ''', (c_ID, strokes, h_ID, p_id, _id))
        self.commit_changes()
        print(f"Added a score for playerID {p_id} for hole {h_ID}.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()




