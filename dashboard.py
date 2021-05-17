import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_initiate import *

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


with Database("discgolf.db") as db:
    try:
        df = db.query_to_df("SELECT * FROM averages")

    except:
        print("Failed to load data to dataframe")


def plot_avg_scores(df):
    '''
    Function to plot average scores for each hole

    :param df: dataframe for plotting average scores
    :return: object fig for plotly to plot
    '''

    df["holeID"] = df["holeID"].astype(str)
    holes = list(df.holeID.unique())

    fig = px.bar(df, x="holeID", y="AVG(score.strokes)", title="Average strokes in each hole", hover_data=['length'], text="AVG(score.strokes)")
    fig.update_layout(
        xaxis_title="Average scores",
        yaxis_title="Hole number",
        xaxis=dict(
            tickmode='array',
            tickvals=holes,
            ticktext=["Hole " + i for i in holes]
        )
    )
    return fig



df["holeID"] = df["holeID"].astype(str)
holes = list(df.holeID.unique())

app = dash.Dash(__name__)

@app.callback(
    Output("putt_chart", "figure"),
    [Input("dropdown", "value")])
def update_avg_putts_chart(holes):
    mask = df["holeID"] == holes
    fig = px.bar(df[mask], x="holeID", y="AVG(score.putts)", barmode="group")

    return fig

app.layout = html.Div([
    html.Div([
        html.H1("""Hole Scoring Averages""",
                    style={'margin-right': '2em', 'textAlign': 'center'})
        ]),
    html.Div([

    dcc.Graph(id="bar-chart", figure=plot_avg_scores(df)),

    ]),
    html.Div([

        html.H1("""Hole Averages""",
                style={'margin-right': '2em', 'textAlign': 'center'})

    ]),

    html.Div([

        html.H5("""Select hole""", style={'margin-right': '2em', 'textAlign': 'center'}),

        dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x} for x in holes],
            value=holes[0],
            clearable=False,
        )
        ], style = {"width": "100%", "display": "flex", "align-items": "center", "justify-content": "center"}),

    html.Div([
        html.Div([

        dcc.Graph(id="putt_chart")

        ], className="box1", style={'width': '25%', 'display': 'inline-block'}),

        html.Div(children="Block 2", className="box2",
                 style={
                     'width': '50%',
                     'display': 'inline-block'
                 })
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)