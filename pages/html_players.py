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

dash.register_page(__name__, path='/Players')


names_crests =  pd.read_csv('./teams.csv')
team_list = names_crests['Team A'].values.tolist()
crest = pd.read_csv('./teams.csv')['crest'].values.tolist()


layout = html.Div(className= "Mother_Div",children= [
	html.H1('Player Statss',style = {'text-align': 'center'}),

    html.Br(),
    html.Div(className="row", children=[
            html.Div(className='six columns', children=[
                dcc.Dropdown(options = [], value = team_list[0], id='team1')], style=dict(width='50%'))
            , html.Div(className='six columns', children=[
                dcc.Dropdown(options = [], value = team_list[1], id='team2')], style=dict(width='50%'))
        ]),

])