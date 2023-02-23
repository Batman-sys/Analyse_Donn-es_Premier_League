import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib as plt
import numpy as np
import math
#web
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output 
from dash import Dash, dash_table
import pandas as pd
from match_data import *
from htmlmatchlib import *


app = dash.Dash(__name__)


# ex match
Goals = "0      Goals       0"
Shots = "0      Shots       0"
Passes = "0      Passes       0"
Fouls = "0      Fouls       0"
Reds = "0      Red Cards       0"
names_crests =  pd.read_csv('.\\teams.csv')
team_list = pd.read_csv('.\\teams.csv')['Team A'].values.tolist()
crest = pd.read_csv('.\\teams.csv')['crest'].values.tolist()
df = pd.DataFrame()

app.layout = html.Div(className = "Mother_div",children=[
    html.Img(id = 'prem_logo', src='https://seeklogo.com/images/P/premier-league-new-logo-D22A0CE87E-seeklogo.com.png'),
    html.H1("Match Statistics", style = {'text-align': 'center'}),
    
    html.Br(),
    html.Div(className="row", children=[
            html.Div(className='six columns', children=[
                dcc.Dropdown(team_list, team_list[0], id='team1')], style=dict(width='50%'))
            , html.Div(className='six columns', children=[
                dcc.Dropdown(team_list, team_list[1], id='team2')], style=dict(width='50%'))
        ],
     style=dict(display='flex')),
    
    dcc.Slider(min = 0, max = 120, marks = None,
               value=45,
               id='drag'
    ),
    html.Div(className = 'foreground', children = [
    html.Div(className = 'time', children = html.H6('',id = 'minute', style = {'text-align': 'center'})),
    html.Div(className='teams', children=[
        html.Img(id='crest1', className = 'crest',src=crest[0]),
        html.H3(" - ", className = 'crest',  style = {'text-align': 'center'}),
        html.Img(id = 'crest2', className = 'crest', src=crest[1]),
    ]),
    html.Div(className = "Stats", children = [
        html.H3("0 Goals 0", id = 'Goals',  style = {'text-align': 'center'}),

        html.Br(),
        html.Br(),

        html.H3('Possession',  style = {'text-align': 'center'}),
        html.Br(),
        html.Br(),

        html.H3('0 Shots 0', id = 'Shots',  style = {'text-align': 'center'}),
        html.Br(),
        html.Br(),

        html.H3('0 Passes 0', id = 'Passes',  style = {'text-align': 'center'}),
        html.Br(),
        html.Br(),

        html.H3('0 Fouls 0', id = 'Fouls',  style = {'text-align': 'center'}),
        html.Br(),
        html.Br(),

        html.H3('0 Reds 0', id = 'Reds',  style = {'text-align': 'center'}),
        html.Br(),
        html.Br(),
                
        html.H3('0 Yellows 0', id = 'Yellows',  style = {'text-align': 'center'}),
        html.Br(),
        html.Br(),

                        
        html.H3('0 Offsides 0', id = 'Offsides',  style = {'text-align': 'center'}),
        html.Br(),
        html.Br(),

                        
        html.H3('0 Corners 0', id = 'Corners',  style = {'text-align': 'center'}),
        html.Br(),
        html.Br(),



    ], style=dict(display='grid')),

    html.Div(className = "Pies", children = [
        dcc.Graph(id = 'pie_possession1', figure = {}),
        dcc.Graph(id = 'pie_possession2', figure = {}),
        ]),

        
       
    
   
    
    

   html.Div(className = 'goal_bar', children=[
    dbc.Progress(id = 'goal1_progress', value = 20, color = 'blue' , bar = True),
    dbc.Progress(id = 'goal2_progress', value = 40, color = 'red', bar = True)
   ]
   ),
   html.Div(className = 'pass_bar', children=[
    dbc.Progress(id = 'pass1_progress', value = 20, color = 'blue' , bar = True),
    dbc.Progress(id = 'pass2_progress', value = 40, color = 'red', bar = True)
   ]
   ), 
   html.Div(className = 'foul_bar', children=[
    dbc.Progress(id = 'foul1_progress', value = 20, color = 'blue' , bar = True),
    dbc.Progress(id = 'foul2_progress', value = 40, color = 'red', bar = True)
   ]
   ),

   html.Div(className = 'shot_bar', children=[
    dbc.Progress(id = 'shot1_progress', value = 20, color = 'blue' , bar = True),
    dbc.Progress(id = 'shot2_progress', value = 40, color = 'red', bar = True)
   ]),

   html.Div(className = 'reds_bar', children=[
    dbc.Progress(id = 'red1_progress', value = 20, color = 'blue' , bar = True),
    dbc.Progress(id = 'red2_progress', value = 40, color = 'red', bar = True)
   ]),

   html.Div(className = 'yellows_bar', children=[
    dbc.Progress(id = 'yellow1_progress', value = 20, color = 'blue' , bar = True),
    dbc.Progress(id = 'yellow2_progress', value = 40, color = 'red', bar = True)
   ]),

   html.Div(className = 'offsides_bar', children=[
    dbc.Progress(id = 'offside1_progress', value = 20, color = 'blue' , bar = True),
    dbc.Progress(id = 'offside2_progress', value = 40, color = 'red', bar = True)
   ]),

   html.Div(className = 'corners_bar', children=[
    dbc.Progress(id = 'corner1_progress', value = 20, color = 'blue' , bar = True),
    dbc.Progress(id = 'corner2_progress', value = 40, color = 'red', bar = True)
   ])
    ]),
   html.Div(className = "Stats", children = [
            (dcc.Graph(id = 'offensiveness', figure = {},  style={'display': 'inline-block'}))
            
            ]),

    

])


#Update Slider
@app.callback(
    Output('drag','max'),
    [Input('team1', 'value'),
     Input('team2', 'value')]
    
)
def update_output(team1, team2):
    df = importing_events(team1, team2)
    match_length = math.ceil(df.Time.values[-1:][0])
    return match_length


#Update stats
@app.callback(
    [
    Output('minute', 'children'),
    Output('crest1','src'),
    Output('crest2','src'),
    Output('Goals', 'children'),
    Output('Shots', 'children'),
    Output('Passes', 'children'),
    Output('Fouls', 'children'),
    Output('Reds', 'children'),
    Output('Yellows', 'children'),
    Output('Offsides', 'children'),
    Output('Corners', 'children'),
    Output('pie_possession1', 'figure'),
    Output('pie_possession2', 'figure'),
    Output('shot1_progress','value'),
    Output('goal1_progress','value'),
    Output('pass1_progress','value'),
    Output('foul1_progress','value'),
    Output('red1_progress','value'),
    Output('yellow1_progress','value'),
    Output('offside1_progress','value'),
    Output('corner1_progress','value'),

    Output('goal1_progress','color'),
    Output('shot1_progress','color'),
    Output('pass1_progress','color'),
    Output('foul1_progress','color'),
    Output('red1_progress','color'),
    Output('yellow1_progress','color'),
    Output('offside1_progress','color'),
    Output('corner1_progress','color'),

    Output('goal2_progress','color'),
    Output('shot2_progress','color'),
    Output('pass2_progress','color'),
    Output('foul2_progress','color'),
    Output('red2_progress','color'),
    Output('yellow2_progress','color'),
    Output('offside2_progress','color'),
    Output('corner2_progress','color')]
    ,
    [Input('team1', 'value'),
     Input('team2', 'value'),
     Input('drag', 'value')]
)

def update_output(team1, team2, minute):
    
    #update match stats
    stats = statistics(team1, team2, minute)
    pie_poss_teams = pie_poss(stats)
    lbars = bars(stats)
    crest1 = names_crests[(names_crests['Team A'] == team1)]['crest']
    crest2 = names_crests[(names_crests['Team A'] == team2)]['crest']
    return str(minute) + "'", *crest1, *crest2, *stats[1:], *pie_poss_teams, *lbars

#Offensiveness Graph
@app.callback(
    Output('offensiveness', 'figure'),
    [Input('team1', 'value'),
     Input('team2', 'value'),
     Input('drag', 'value')]

)
def update_output(team1, team2, minute):
    
    df = importing_events(team1, team2)
    team_off = df[df['Time'] <= minute]
    fig = px.line(team_off, x="Time", y="Offensiveness", color='Player1 Team')

    
    return fig



if __name__ == '__main__':
    app.run_server(debug = True)