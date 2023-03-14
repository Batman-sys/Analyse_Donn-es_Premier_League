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

dash.register_page(__name__)


names_crests =  pd.read_csv('./teams.csv')
team_list = pd.read_csv('./teams.csv')['Team A'].values.tolist()
crest = pd.read_csv('./teams.csv')['crest'].values.tolist()


layout = html.Div([
	html.H1('Multi-page app with Dash Pages'),

    html.Div(
        [
            html.Div(
            )
        ]
    ),

])