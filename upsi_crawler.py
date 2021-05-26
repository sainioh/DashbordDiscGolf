import pandas as pd
from db_initiate import *
#pip install lxml
import datetime
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError



def create_dataframe(url):
    '''
    Creates a pandas dataframe from table in the website specified with url-parameter

    :param url: url of the website we want to crawl
    :return: returns dataframe
    '''
    try:
        df = pd.read_html(url, attrs={'class': 'scores'})
        df = df[0]
    except:
        print("Could not read dataframe from url")
        raise

    # fixing dataframe column names

    return df


def create_rows(df):
    '''
    Creates easily accessible rows (list of lists) from dataframe

    :param df: dataframe scraped from website
    :return: rows, a list of lists
    '''

    rows = []
    for index, row in df.iterrows():
        to_input = []
        for obj in row:
            to_input.append(obj)
        rows.append(to_input)

    return rows


def date_validation(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Wrong date format! Insert (YYYY-MM-DD)")


def input_information():
    validate = URLValidator(regex="upsiapp+")  # URL validator to only accept from upsiapp

    url = "http://www.upsiapp.com/games/543499"
    try:
        validate(url)
    except ValidationError:
        print("Not valid URL or not from Upsiapp")
        raise ValidationError

    date = "2020-04-28"
    date_validation(date)

    return url, date



def insert_data(rows, dbpath, date):
    with Database(dbpath) as db:

        # iterating over rows(each containing results for a player round) we want to add
        for row in rows:
            try:
                # calling method to add a round with parameters for date and playerID, returns roundID
                _id, p_id = db.add_round(date, row)
            except:
                print("add_round failed")

            holes = [i for i in range(1, len(df.columns) - 1)]

            try:

                for i in range(2, len(row)):
                    db.add_score(1, row[i], holes[i - 2], p_id, _id)  # calling method to add a score with parameters
            except:
                print("add_score failed")




print(f"\n{'*'*75}")
print("Here you can automatically add scores to database from Upsi round URL's")
print(f"{'*'*75}\n")


url, date = input_information()
df = create_dataframe(url)
rows = create_rows(df)
insert_data(rows, "discgolf.db", date)