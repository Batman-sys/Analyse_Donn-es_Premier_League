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
from dash import html, callback
from dash.dependencies import Input, Output 
from dash import Dash, dash_table
import pandas as pd
import copy as cp
from players import *
dash.register_page(__name__, path='/Players')


names_crests =  pd.read_csv('./teams.csv')
team_list = names_crests['Team A'].values.tolist()
players =  pd.read_csv('./player_team&photo.csv')


layout = html.Div(className= "Mother_Div",children= [
	html.H1('Player Stats',style = {'text-align': 'center'}),
    
    html.Br(),
    html.Div(className="row", children=[
            html.Div(className='six columns', children=[
                dcc.Dropdown(options = team_list, value = team_list[18], id='playerteam1')], style=dict(width='50%'))
            , html.Div(className='six columns', children=[
                dcc.Dropdown(options = [], value = 'Dimitar BERBATOV', id='player')], style=dict(width='50%'))
        ], style=dict(display='flex')
        ),
    html.Div(className = 'foreground', children = [
    html.Div(className='teams', children=[
            html.Img(id='player_photo', className = 'player_photo',src=''),
        ], style = {'text-align': 'center'}),
    html.H2('Offense:'),
    html.Div([dcc.Graph(id = 'goal_per_shots', figure = {},  style={'display': 'inline-block'})], style={'textAlign': 'center'}),
    html.Div([dcc.Graph(id = 'shot_types', figure = {},  style={'display': 'inline-block'})], style={'textAlign': 'center'}),
    html.Div([dcc.Graph(id = 'shot_direction', figure = {},  style={'display': 'inline-block'})], style={'textAlign': 'center'}),



    html.H2('Distribution:'),
    html.Div([dcc.Graph(id = 'succ_pass', figure = {},  style={'display': 'inline-block'})], style={'textAlign': 'center'}),
    html.Div([dcc.Graph(id = 'pass_per_assist', figure = {},  style={'display': 'inline-block'})], style={'textAlign': 'center'}),
    html.Div([dcc.Graph(id = 'pass_direction', figure = {},  style={'display': 'inline-block'})], style={'textAlign': 'center'}),
  

    html.H2('Defence:'),
    html.Div([dcc.Graph(id = 'blocks_tackles_fouls', figure = {},  style={'display': 'inline-block'})], style={'textAlign': 'center'}),
    html.Div([dcc.Graph(id = 'saves_per_goal', figure = {},  style={'display': 'inline-block'})], style={'textAlign': 'center'}),
    html.Div([dcc.Graph(id = 'yellow_red', figure = {},  style={'display': 'inline-block'})], style={'textAlign': 'center'}),
    
    ],
    ),

])

#Update team list
@callback(
    [Output('player', 'options')],
    [Input('playerteam1', 'value')]
)
def update_output(t1):
    return [players[players['Team'] == t1]['Player Name'].values.tolist()]

#Update Player Info
@callback(
    Output('player_photo', 'src'),
    Input('player', 'value')
)
def update_output(p):
    if p != '':
        return players[players['Player Name'] == p]['image_url'].values[0]
    else:
        return ''
    

#Update Attack
@callback(
    [
     Output('goal_per_shots', 'figure'),
     Output('shot_types', 'figure'),
     Output('shot_direction', 'figure')
    ],
    Input('player', 'value')
)
def update_output(p):
    df_events = importing_events(p)
    shots = ['Shot','Header Shot','Direct Free Kick Shot','Penalty Shot']
    d=len(df_events.loc[(df_events['Player1 Name']==p)&(df_events['Event Name'].isin(shots))])
    g = eventOfPlayerPerSeason(p,'Goal', df_events)
    fig = go.Figure(
        go.Pie(
                    title= 'Nombre de Buts et Tirs ratés',
                    labels = ['Goals', 'Unconverted Shots'],
                    values=[g, d-g],
                    pull=[0.1, 0.1],
                    marker_colors=['rgb(250, 100, 10)', 'rgb(240, 240, 240)'],
                    
                )
    )

    return fig, plot_shots(p, df_events), draw_player_shot(p, df_events)


#Update Playmaking

@callback(
    [
     Output('succ_pass', 'figure'),
     Output('pass_per_assist', 'figure'),
     Output('pass_direction', 'figure')
    ],
    Input('player', 'value')
)
def update_output(p):
    df_events = importing_events(p)
    pa = decisive_pass_season(p, df_events)
    p_total = len(df_events.loc[(df_events["Player1 Name"]== p)&(df_events['Event Name']=='Pass')])
    succ = succPassPerSeason(p,df_events)
    g = eventOfPlayerPerSeason(p,'Goal', df_events)
    fig = go.Figure(
        go.Pie(
                    title= 'Contributions',
                    labels = ['Assist', 'Goals'],
                    values=[pa, g],
                    pull=[0, 0],
                    marker_colors=['rgb(250, 100, 10)','rgb(240, 240, 240)'],
                    
                )
    )
    
    fig1 = go.Figure(
        go.Pie(
                    title= 'Nombre de Passes réussies / nombre totale de passes',
                    labels = ['Successful Pass', 'Missed Pass'],
                    values=[succ, p_total-succ],
                    pull=[0.1, 0.1],
                    marker_colors=['rgb(250, 100, 10)', 'rgb(240, 240, 240)'],
                    
                )
    )
    
    return  fig1, fig, draw_player_pass_season(p, df_events)


#Update Defending

@callback(
    [
     Output('blocks_tackles_fouls', 'figure'),
     Output('saves_per_goal', 'figure'),
     Output('yellow_red', 'figure')
    ],
    Input('player', 'value')
)
def update_output(p):
    df_events = importing_events(p)
    team = (df_events[(df_events['Player1 Name'] == p)]['Player1 Team'].values)[0]
    t = (eventOfPlayerPerSeason(p,'Tackle', df_events)), (eventOfPlayerPerSeason(p,'Block', df_events)), (eventOfPlayerPerSeason(p,'Foul', df_events))
    s = (eventOfPlayerPerSeason(p,'Goalkeeper Save', df_events)) + (eventOfPlayerPerSeason(p,'Goalkeeper Save Catch', df_events)) , len((df_events[((df_events['Player1 Team'] != team) & (df_events['Event Name'] == 'Goal')) | ((df_events['Player1 Team'] == team) & (df_events['Event Name'] == 'Own Goal'))]))
    yr = (eventOfPlayerPerSeason(p,'Yellow Card', df_events)), (eventOfPlayerPerSeason(p,'Red Card', df_events))
    fig = go.Figure(   
            go.Bar(
                x = ['Tackle', 'Block', 'Foul'],
                y = t
                )
            )
    fig.update_layout(title = 'Actions défensives par '+p)
    fig1 = go.Figure()  
    if s[0] > 0: 
        fig1 = go.Figure(
            go.Pie(
                        title= 'Nombre de tirs arretés / nombre de tirs concédés',
                        labels = ['Tirs Arretés', 'Buts encaissés'],
                        values=[s[0], s[1]],
                        pull=[0.1, 0.1],
                        marker_colors=['rgb(250, 100, 10)', 'rgb(240, 240, 240)'],
                        
                    )
        )
    
    
    fig2 = go.Figure(
        go.Pie(
                    title= 'Nombre de Cartons jaunes / nombre de Cartons rouges',
                    labels = ['Carton Jaune', 'Carton Rouge'],
                    values=[yr[0], yr[1]],
                    pull=[0.1, 0.1],
                    marker_colors=['rgb(250, 255, 10)', 'rgb(255,0,0)'],
                    
                )
        )

    
    return  fig, fig1, fig2