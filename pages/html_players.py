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

dash.register_page(__name__, path='/Players')


names_crests =  pd.read_csv('./teams.csv')
team_list = names_crests['Team A'].values.tolist()
players =  pd.read_csv('./player_team&photo.csv')


layout = html.Div(className= "Mother_Div",children= [
	html.H1('Player Stats',style = {'text-align': 'center'}),
    
    html.Br(),
    html.Div(className="row", children=[
            html.Div(className='six columns', children=[
                dcc.Dropdown(options = team_list, value = team_list[0], id='playerteam1')], style=dict(width='50%'))
            , html.Div(className='six columns', children=[
                dcc.Dropdown(options = [], value = '', id='player')], style=dict(width='50%'))
        ], style=dict(display='flex')
        ),
    html.Div(className = 'foreground', children = [
    html.Div(className='teams', children=[
            html.Img(id='player_photo', className = 'player_photo',src=''),
        ], style = {'text-align': 'center'}),
    html.H2('Offense:'),
    


    html.H2('Distribution:'),



    html.H2('Defence:')
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