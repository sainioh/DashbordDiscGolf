# Dash application for Disc Golf Statistics

This project uses sqlite3 to store disc golf round data in a database, which is used to query data and build visualizations with Plotly to a local Dash application.

The project is cut into two parts. First part includes visualizations about my personal game with more in-depth statistics and data, which I will have to gather myself.
This data is currently dummy data so it differs from the data for the second part of the project, which uses historical data.
This is the original part of project, but I wanted to shift the focus more into analysing data within a certain player group instead of just one player.
The shift is mostly because to manual work that is required to enter more speficic data for single player rounds, and adding data manually is a nightmare.

I realized midway that most of the work did not include too much python programming beyond simple stuff so I extended the scope and created a web scraper.
I use application called Upsiapp to save scores from each player in the round and after the round you can share the results with friends through
a website i.e "http://www.upsiapp.com/games/<seriesofnumbers>". 
upsi_crawler.py asks the user to enter this URL and the date of the game played and automatically adds the round data to database.

The second part of this project includes historical data from my home course in Finland, Puolarmaari with three other players that I regularly play with.
The web scraper cannot add round statistics of those players who are not one of these four players, but the rounds of players in the same group that are already
in the database will get added.
The visualizations are showing comparisons between our performances over time in each hole as well as showing the progression of total result from each round played in time-series chart.


The project can be easily extended to accept new courses, new players and add functionalities in the Dash app to allow users to choose
which player/course data they want to analyse.

#### General information

Dependencies in requirements.txt

Use:
	pip install -r requirements.txt
	
	
##### !!!!	Important !!!!

To open the dashboard, run dashboard.py and click on the link it provides. (Dash is built on top of Flask)


I have included a few URLs to test the scraper in the file upsi_crawler.py documentation.






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


 