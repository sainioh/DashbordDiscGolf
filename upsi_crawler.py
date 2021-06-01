import pandas as pd
from db_initiate import *
#pip install lxml
import datetime
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

"""
I am not sure on ethical aspect of crawlers but the website I am crawling, the robots.txt and their legal text does not
mention anything about automatic retrieval of the data. 


I have included some of my actual round URLs below so the script can be tested in practise.
You have to manually add the URL and date to variables at the end of this file. Using user inputs 
were giving me an error and a headache in pytests,so had to opt for this solution in the project. 


URL1 : http://www.upsiapp.com/games/913162
Date1: 2020-06-06


URL2 : http://www.upsiapp.com/games/1200712
Date2: 2020-06-15


"""


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



def validate_information(date, url):
    '''
    Input function for URL of the round and the date of the round played.

    :return: stringa "url" and "date"
    '''
    validate = URLValidator(regex="upsiapp+")  # URL validator to only accept from site Upsiapp

    try:
        validate(url)
    except ValidationError:
        print("Not valid URL or not from Upsiapp")
        raise ValidationError

    date_validation(date)




def insert_data(rows, dbpath, date):
    with Database(dbpath) as db:

        # iterating over rows(each containing results for a player round) we want to add
        for row in rows:
            try:
                # calling method to add a round with parameters for date and playerID, returns roundID
                _id, p_id = db.add_round(date, row)
            except:
                print("Adding a round failed.")

            holes = [i for i in range(1, len(df.columns) - 1)]

            try:

                for i in range(2, len(row)):
                    db.add_score(1, row[i], holes[i - 2], p_id, _id)  # calling method to add a score with parameters
            except:
                print("Adding score failed")



print(f"\n{'*'*55}")
print("Upsi crawler starting...")
print(f"{'*'*55}\n")


######### ENTER URL AND DATE HERE ##########

url = "http://www.upsiapp.com/games/1200712"
date = "2020-06-15"


validate_information(date, url) #validate url and date
df = create_dataframe(url)  # read table from url, convert to pandas dataframe
rows = create_rows(df)
insert_data(rows, "discgolf.db", date)  # run inserts to database