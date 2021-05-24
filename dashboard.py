import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_initiate import *

import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output
from itertools import cycle



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


def plot_player_avgs(df):
    palette = cycle(px.colors.qualitative.Plotly)



    fig_3 = go.Figure()
    holes = list(df["holeID"].unique())

    fig_3.add_trace(go.Bar(x=holes,
                         y=list(df[df["playerID"] == 1].hole_average.values),
                         name='Hemmo',
                         marker_color=next(palette)
                         ))
    fig_3.add_trace(go.Bar(x=holes,
                         y=list(df[df["playerID"] == 2].hole_average.values),
                         name='Sami',
                         marker_color=next(palette)
                         ))
    fig_3.add_trace(go.Bar(x=holes,
                         y=list(df[df["playerID"] == 3].hole_average.values),
                         name='Daniel',
                         marker_color=next(palette)
                         ))
    fig_3.add_trace(go.Bar(x=holes,
                         y=list(df[df["playerID"] == 4].hole_average.values),
                         name='Joonas',
                         marker_color=next(palette)
                         ))

    fig_3.update_layout(
        title='Puolarmaari, player average strokes per hole',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Average strokes',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis=dict(
            title='Hole number',
            titlefont_size=16,
            tickfont_size=14,
            tickmode='array',
            tickvals=holes,
            ticktext=["Hole " + str(i) for i in holes]

        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1,
        height=600
    )

    return fig_3


def plot_team_results(df2):

    df2["Date"] = pd.to_datetime(df2["Date"])
    df2 = df2.sort_values("Date")

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=df2[df2["playerID"] == 1]["Date"], y=list(df2[df2["playerID"] == 1]["result"]),
                             mode='lines+markers',
                             name='Hemmo'))
    fig4.add_trace(go.Scatter(x=df2[df2["playerID"] == 2]["Date"], y=list(df2[df2["playerID"] == 2]["result"]),
                             mode='lines+markers',
                             name='Sami'))
    fig4.add_trace(go.Scatter(x=df2[df2["playerID"] == 3]["Date"], y=list(df2[df2["playerID"] == 3]["result"]),
                             mode='lines+markers',
                             name='Daniel'))
    fig4.add_trace(go.Scatter(x=df2[df2["playerID"] == 4]["Date"], y=list(df2[df2["playerID"] == 4]["result"]),
                             mode='lines+markers',
                             name='Joonas'))

    fig4.update_layout(
        title='Scoring progression for each player',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Scores compared to par',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis=dict(
            title='Date',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        height=600,
        width=1600)


    return fig4





with Database("discgolf.db") as db:
    try:
        df = db.query_to_df("SELECT * FROM averages")
        df_stats = db.query_to_df("SELECT * FROM course_stats")
        df_team_avgs = db.query_to_df("SELECT * FROM team_averages")
        df_team_results = db.query_to_df("SELECT * FROM team_scores")

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
    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
        html.H1("""Player comparisons"""),
        dcc.Graph(id="team_avgs", figure=plot_player_avgs(df_team_avgs))


    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
        html.H1("""Player result progression"""),
        html.Br(),
        html.Br(),
        dcc.Graph(id="team_results", figure=plot_team_results(df_team_results))


    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)