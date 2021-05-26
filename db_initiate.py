import sqlite3
import pandas as pd


class Database():
    '''
    Class used to open and close database as well as perform queries and inserts to the database.

    Attributes:

        connection :    connection object to the database

        c :     database/connection cursor


    Methods:

        commit_changes():

                Used to commit changes made in the database (inserts)

        query_to_df(q):

                Used to execute queries to database and
                converting the results to pandas dataframes.

                q (str): query to be performed


        add_round(date, data):

                Used to insert a new row to round -table in database.

                date(str):      date of the round (YYYY-MM-DD)
                data(list):     list of observations (data about a player round)


        add_score(c_ID, strokes, h_ID, p_id, _id):

                Used to insert the actual round data to player_scores -table.

                c_ID:      ID of the course (always 1 but included for future extension where we can add other courses)
                strokes:   number of strokes taken in the specific hole
                h_ID:      holeID (refers to holeID in database) to know which hole we are adding data to
                p_id:      playerID (refers to players ID in database) to know whose score we are adding
                _id:       roundID(refers to playerRoundID in database) to know to which round is this score being added to


        __exit()__:

            When we are exiting the use of Database class, we are using "connection.close()" to close the connection to
            the database.
    '''

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

        # making sure the name in database matches to one in our database
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




