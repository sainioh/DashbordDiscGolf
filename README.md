# Dash application for Disc Golf Statistics

This project uses sqlite3 to store disc golf round data in a database, which is used to query data and build visualizations with Plotly to a local Dash application.

The project is cut into two parts. First part includes visualizations about my personal game with more in-depth statistics and data, which I will have to gather myself.
This data is currently dummy data so it differs from the data for the second part of the project, which uses historical data.

Second part includes historical data from my home course in Finland, Puolarmaari with 3 other players that I regularly play with.
The visualizations are showing comparisons between our performances over time in each hole as well as showing the progression of total result from each round played in time-series chart.

#### General information

I 





## About Disc Golf

Disc Golf is similar in rules with regular golf, but it is played with a frisbee and the targets are metal baskets with chain links. The goal is to get the disc to rest inside the basked with as many strokes or throws as possible.


## Data

Data for the personal part of project has to be added manually, but a GUI application is in development to add the data more easily.

Data gathering for seocnd part is hovering in a gray area. I am inserting an URL to Upsiapp (application to record data of rounds) of that specific game and the date played to a program and it automatically scrapes the data to my database.


## Statistics

### Personal statistics

#### Hole scoring averages

Graph shows average scores over time for each hole in my home course, as well as show how long the hole is, indicating whether length affects the scores.

#### Hole averages

The graphs show more accurate data for each hole individually. User can select the hole to be viewed from the dropdown menu

### Group Statistics

#### Player average strokes per hole

The graph indicates for each player and hole, the average scores. This graph can be used to determine the best performers and collectively get insight how players should approach each hole.

#### Scoring progression

The time-series plot indicates how the players total round scores have been evolving. 


 