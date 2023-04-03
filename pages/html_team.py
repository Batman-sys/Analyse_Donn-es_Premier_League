import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import math
import copy as cp
#web
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html, callback
from dash.dependencies import Input, Output 
from dash import Dash, dash_table
import pandas as pd
from team import *




dash.register_page(__name__, path='/Team')


names_crests =  pd.read_csv('./teams.csv')
team_list = names_crests['Team A'].values.tolist()





layout = html.Div(className = "Mother_div",children=[
    
    html.H1("Team Statistics", style = {'text-align': 'center'}),
    
    html.Br(),
    html.Div(className="row", children=[
                html.Div(className='six columns', children=[
                dcc.Dropdown(options = team_list, value = team_list[1], id='team')], style=dict(width='50%'))
        ],
     style=dict(display='flex')),
   html.Div(className = 'foreground', children = [
        html.Div([dcc.Graph(id = 'xG_Goals_for_against', figure = {},  style={'display': 'inline-block'})], style={'textAlign': 'center'}),
        html.Div([dcc.Graph(id = 'plot_shots', figure = {},  style={'display': 'inline-block'})], style={'textAlign': 'center'}),
        html.Div([dcc.Graph(id = 'match_result', figure = {},  style={'display': 'inline-block'})], style={'textAlign': 'center'}),
   ]),

])

#Graphs
@callback(
    [Output('xG_Goals_for_against', 'figure'),
     Output('plot_shots', 'figure'),
     Output('match_result', 'figure'),
    ],
    Input('team', 'value')
)
def update_output(team):
    df_players = importing_team_players(team)
    df_events = importing_team_events(team)
    return plot_shots(team, df_events, df_players), plot_shots2(team, df_events), pie_chart_match_result(team, df_players)