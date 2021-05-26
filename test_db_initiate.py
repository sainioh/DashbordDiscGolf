import pytest
from db_initiate import *
from upsi_crawler import insert_data, create_rows


@pytest.fixture()
def dummy_data():
    '''
    Dummy data is from actual historical disc golf round records, straight in the format that it is pulled in
    by "pd.read_html()" in module test_crawler. Since we are moving in gray area in scraping data from their website,
    out of respect to Upsiapp I'd rather do tests with saved data instead of doing html requests.
    '''

    return [(pd.read_csv("test_data/test_input.csv", index_col=0), '2020-05-27'),
            (pd.read_csv("test_data/test_input2.csv", index_col=0), '2020-05-28')]




def test_df_integrity(dummy_data):
    dd1 = dummy_data[0][0]
    dd2 = dummy_data[1][0]

    assert 0 < dd1.shape[0] <= 4
    assert dd1.shape[1] == 22    # we know we should have 22 columns

    # assert all necessary values to be integers
    for i in range(2,len(dd1)):
        assert dd1.iloc[:,i].dtype == 'int64'

        # all larger than 0
        assert all(dd1.iloc[:,i] > 0)

        # all smaller than 10, because that is largest amount per hole and we want to avoid outliers
        assert all(dd1.iloc[:,i] <= 10)


    assert 0 < dd2.shape[0] <= 4
    assert dd2.shape[1] == 22    # we know we should have 22 columns

    # assert all necessary values to be integers
    for i in range(2,len(dd2)):
        assert dd2.iloc[:,i].dtype == 'int64'

        # all larger than 0
        assert all(dd2.iloc[:,i] > 0)

        # all smaller than 10, because that is largest amount per hole and we want to avoid outliers
        assert all(dd2.iloc[:,i] <= 10)



def test_create_rows(dummy_data):

    dd1 = dummy_data[0][0]
    dd2 = dummy_data[1][0]
    rows1 = create_rows(dd1)
    rows2 = create_rows(dd2)

    # there cannot be 0 or less or more than 4 rows per one insert
    assert len(rows1[0]) > 0
    assert len(rows1) > 0 and len(rows1) <= 4

    assert len(rows2[0]) > 0
    assert len(rows2) > 0 and len(rows2) <= 4



# TESTING THE INTEGRITY OF DATA INSERT


def test_add_data(dummy_data):

    dd1, dd2 = dummy_data[0][0], dummy_data[1][0]
    date1, date2 = dummy_data[0][1], dummy_data[1][1]
    rows1, rows2 = create_rows(dd1),create_rows(dd2)


    # testing rows1

    insert_data(rows1, "ptest_discgolf.db", date1)

    with Database("ptest_discgolf.db") as db:
        try:
            df = db.query_to_df("SELECT * FROM player_scores")
            df_round = db.query_to_df("SELECT * FROM player_round")

        except:
            print("Failed to load data to dataframe")
            raise


    l_rows1 = len(rows1) * 20
    df_test1 = df.tail(l_rows1)    # last 20 added rows
    l_added = list(df_test1.strokes)    # storing added strokes to a list
    row1_strokelist = [i for s in rows1 for i in s[2:]] # actual input list of strokes


    assert l_added == row1_strokelist   # asserting that we are inserting the exact values that as used as input

    assert list(df_round.tail(len(rows1)).date)[0] == date1 # make sure the date added is right



    #testing rows2

    insert_data(rows2, "ptest_discgolf.db", date2)

    with Database("ptest_discgolf.db") as db:
        try:
            df = db.query_to_df("SELECT * FROM player_scores")
            df_round = db.query_to_df("SELECT * FROM player_round")

        except:
            print("Failed to load data to dataframe")
            raise


    l_rows2 = len(rows2) * 20
    df_test2 = df.tail(l_rows2)    # last 20 added rows
    l_added = list(df_test2.strokes)    # storing added strokes to a list
    row2_strokelist = [i for s in rows2 for i in s[2:]] # actual input list of strokes


    assert l_added == row2_strokelist   # asserting that we are inserting the exact values that as used as input

    assert list(df_round.tail(len(rows2)).date)[0] == date2 # make sure the date added is right



# TESTING DATABASE INTEGRITY

@pytest.fixture()
def dataframe():
    '''
    Using a testing database "ptest_discgolf.db", a copy of main database from 14.05.2021.
    This way we are avoiding adding redundant data to actual database.
    '''

    with Database("ptest_discgolf.db") as db:
        try:
            df = db.query_to_df("SELECT * FROM averages")
            df_stats = db.query_to_df("SELECT * FROM course_stats")
            df_team_avgs = db.query_to_df("SELECT * FROM team_averages")
            df_team_results = db.query_to_df("SELECT * FROM team_scores")

        except:
            print("Failed to load data to dataframe")
            raise

    return [df, df_stats, df_team_avgs, df_team_results]


def test_df(dataframe):

    df_avg, df_stats, df_t_avg, df_t_results = dataframe[0],dataframe[1],dataframe[2],dataframe[3]

    #validate df_avg
    cols1 = ['courseID','holeID','holeNumber','AVG(score.strokes)','AVG(score.putts)', 'length']
    assert list(df_avg.columns) == cols1

    # 8 is max for throws per hole, so avg has to be less or equal. Cannot be negative
    assert 0 <= all(list(df_avg["AVG(score.strokes)"])) <= 8
    assert 0 <= all(list(df_avg["AVG(score.putts)"])) <= 8


    # validate df_stats
    vals = ['Fairway', 'Off the fairway', 'Circle 1', 'OB', 'Circle 2']
    assert all(s in vals for s in list(df_stats.offTheTee.values))
    assert 0 <= all(list(df_stats["strokes"])) <= 8
    assert 0 <= all(list(df_stats["putts"])) <= 8

