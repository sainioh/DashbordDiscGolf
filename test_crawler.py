'''import pytest
from db_initiate import *
import pandas as pd
from upsi_crawler import *


@pytest.fixture()
def dummy_data():
    return pd.read_csv("test_input.csv")


@pytest.fixture()
def dataframe():
    with Database("discgolf.db") as db:
        try:
            df = db.query_to_df("SELECT * FROM averages")
            df_stats = db.query_to_df("SELECT * FROM course_stats")
            df_team_avgs = db.query_to_df("SELECT * FROM team_averages")
            df_team_results = db.query_to_df("SELECT * FROM team_scores")

        except:
            print("Failed to load data to dataframe")
            raise

    return [df, df_stats, df_team_avgs, df_team_results]

def test_df_integrity(dummy_data):
    assert 0 < dummy_data.shape[0] <= 4
    assert dummy_data.shape[1] == 23    # we know we should have 23 columns

    # assert all necessary values to be integers
    for i in range(2,len(dummy_data)):
        assert dummy_data.iloc[:,i].dtype == 'int64'

        # all larger than 0
        assert all(dummy_data.iloc[:,i] > 0)

        # all smaller than 10, because that is largest amount per hole and we want to avoid outliers
        assert all(dummy_data.iloc[:,i] >= 10)



def test_create_rows(dummy_data):
    rows = create_rows(dummy_data)

    assert len(rows[0]) > 0
    assert len(rows) > 0 and len(rows) <= 4





'''