import pandas as pd
from db_initiate import *
#pip install lxml


def create_dataframe(url):
    df = pd.read_html(url, attrs={'class': 'scores'})
    df = df[0]

    a = ['Player', 'Score']
    a.extend([str(i) for i in range(1, len(df.columns) - 1)])

    return df

def create_rows(df):

    rows = []
    for index, row in df.iterrows():
        to_input = []
        for obj in row:
            to_input.append(obj)
        rows.append(to_input)

    return rows



print(f"\n{'*'*75}")
print("Here you can automatically add scores to database from Upsi round URL's")
print(f"{'*'*75}\n")


try:
    url = str(input("Insert URL:\t"))
    date = str(input("Insert Date (YYYY-MM-DD):\t"))
except ValueError:
    print("Failed")
    raise

df = create_dataframe(url)
rows = create_rows(df)

print(df)

with Database("discgolf.db") as db:
    try:
        for row in rows:

            _id, p_id = db.add_round(date, row)  # calling method to add a round with parameters for date and playerID, returns roundID

            holes = [i for i in range(1, len(df.columns) - 1)]

            for i in range(2, len(row)):
                db.add_score(1, row[i], holes[i - 2], p_id, _id) # calling method to add a score with parameters

    except:
        print("Failed to load data to database")