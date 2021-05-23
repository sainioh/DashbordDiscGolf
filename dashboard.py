import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_initiate import *

import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output



def plot_avg_scores(df):
    '''
    Function to plot average scores for each hole

    :param df: dataframe for plotting average scores
    :return: object fig for plotly to plot
    '''

    df["holeID"] = df["holeID"].astype(str)
    holes = list(df.holeID.unique())

    fig = px.bar(df, x="holeID", y="AVG(score.strokes)", title="Average strokes in each hole", hover_data=['length'],
                 text="AVG(score.strokes)", color='length', color_continuous_scale="Mint")
    fig.update_layout(
        yaxis_title="Average scores",
        xaxis_title="Hole number",
        xaxis=dict(
            tickmode='array',
            tickvals=holes,
            ticktext=["Hole " + i for i in holes]
        )
    )
    return fig




with Database("discgolf.db") as db:
    try:
        df = db.query_to_df("SELECT * FROM averages")
        df_stats = db.query_to_df("SELECT * FROM course_stats")

    except:
        print("Failed to load data to dataframe")



df["holeID"] = df["holeID"].astype(str)
df_stats["holeID"] = df_stats["holeID"].astype(str)
holes = list(df.holeID.unique())




app = dash.Dash(__name__)


@app.callback(
    Output("putt_chart", "children"),
    [Input("dropdown", "value")])
def update_avg_putts_chart(holes):
    mask = df["holeID"] == holes

    op_string = f"{df[mask]['AVG(score.putts)'].values[0]}"

    return '{}'.format(df[mask]['AVG(score.putts)'].values[0])


@app.callback(
    Output("teeshot_chart", "figure"),
    [Input("dropdown", "value")])
def update_offthetee_chart(h):
    mask_b = df_stats["holeID"] == h
    fig_b = px.histogram(df_stats[mask_b], x='offTheTee', barmode='group', color_discrete_sequence=['lightseagreen'])
    fig_b.update_layout(
        yaxis=dict(
            tickmode='linear',
            tick0 = 0,
            dtick = 1
        )
    )

    return fig_b




app.layout = html.Div([
    html.Div([
        html.H1("""Hole Scoring Averages""",
                    style={'margin-right': '2em', 'textAlign': 'center'})
        ]),
    html.Div([

    dcc.Graph(id="bar-chart", figure=plot_avg_scores(df)),

    ]),
    html.Br(),
    html.Br(),
    html.Div([

        html.H1("""Hole Averages""",
                style={'margin-right': '2em', 'textAlign': 'center'})

    ]),

    html.Div([

        html.H3("""Select hole""", style={'margin-right': '2em', 'textAlign': 'center'}),

        dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x} for x in holes],
            value=holes[0],
            clearable=False,
        )
        ], style = {"width": "100%", "display": "flex", "align-items": "center", "justify-content": "center"}),

    html.Div([
        html.Div([
            html.H1("""Average putts for the hole"""),
            html.H2(id="putt_chart", style={'margin-right': '2em', 'textAlign': 'center'}),

            #dcc.Graph(id="putt_chart")

        ], className="box1", style={'width': '25%', 'display': 'inline-block', 'text-align': 'center', 'vertical-align':'top'}),


        html.Div([
            dcc.Graph(id="teeshot_chart")

        ], className="box2", style={'width': '50%', 'display': 'inline-block'})
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)