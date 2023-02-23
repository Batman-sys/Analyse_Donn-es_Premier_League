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
from dash import html
from dash.dependencies import Input, Output 
from dash import Dash, dash_table
import pandas as pd
from Proj import *


def statistics(team1, team2, minute):
    stats = match_stats(team1, team2, minute)
    Goals = str(stats[0]) + "  Goals  " + str(stats[1])
    Shots = str(stats[2]) + "  Shots  " + str(stats[3])
    Passes = str(stats[8]) + "  Passes  " + str(stats[9])
    Fouls = str(stats[10]) + "  Fouls  " + str(stats[11])

    reds = str(stats[4]) + "  Reds  " + str(stats[5])
    yellows = str(stats[6]) + "  Yellows  " + str(stats[7])
    offsides = str(stats[12]) + "  Offsides  " + str(stats[13])
    corners = str(stats[14]) + "  Corners  " + str(stats[15])
    return stats, Goals, Shots, Passes, Fouls, reds, yellows, offsides, corners

def pie_poss(stats):
    
    pie_poss_team1 = go.Figure(
            data=[
                go.Pie(
                    values=[stats[0][16], stats[0][17]], 
                    hole=.5,
                    textinfo='none',
                    marker_colors=['rgb(30, 50, 240)', 'rgb(240, 240, 240)'],
                )
            ],
            layout=go.Layout(
                annotations=[{'text': str(round(stats[0][16])) + "%", 'x':0.50, 'y':0.5, 'font_size':11, 'showarrow':False}],
                showlegend=False
            )
        )
    pie_poss_team2 = go.Figure(
            data=[
                go.Pie(
                    values=[stats[0][16], stats[0][17]], 
                    hole=.5,
                    textinfo='none',
                    marker_colors=['rgb(240, 240, 240)', 'rgb(250, 100, 10)'],
                    
                )
            ],
            layout=go.Layout(
                annotations=[{'text': str(round(stats[0][17])) + "%", 'x':0.50, 'y':0.5, 'font_size':11, 'showarrow':False}],
                showlegend=False
            )
        )
    
    pie_poss_team1.layout.paper_bgcolor = 'rgb(221, 216, 216)'
    pie_poss_team2.layout.paper_bgcolor = 'rgb(221, 216, 216)'
    return pie_poss_team1, pie_poss_team2
    
def bars(stats):
    colors = 8 * ['gray', 'gray']
    all_shots = int(stats[0][2]) + int(stats[0][3])
    all_goals = int(stats[0][0]) + int(stats[0][1])
    all_passes = int(stats[0][8]) + int(stats[0][9])
    all_fouls = int(stats[0][10]) + int(stats[0][11])
    all_reds = int(stats[0][4]) + int(stats[0][5])
    all_yellows = int(stats[0][6]) + int(stats[0][7])
    all_offsides = int(stats[0][12]) + int(stats[0][13])
    all_corners = int(stats[0][14]) + int(stats[0][15])
    
    if all_shots != 0:
        all_shots = int(stats[0][2]) * 40 / all_shots
        colors[1] = 'blue'
        colors[9] = 'rgb(250, 100, 10)'
    
    if all_goals != 0:
        all_goals = int(stats[0][0]) * 40 / all_goals
        colors[0] = 'blue'
        colors[8] = 'rgb(250, 100, 10)'

    if all_passes != 0:
        all_passes = int(stats[0][8]) * 40 / all_passes
        colors[2] = 'blue'
        colors[10] = 'rgb(250, 100, 10)'

    if all_fouls != 0:
        all_fouls = int(stats[0][10]) * 40 / all_fouls
        colors[3] = 'blue'
        colors[11] = 'rgb(250, 100, 10)'
    
    if all_reds != 0:
        all_reds = int(stats[0][4]) * 40 / all_reds
        colors[4] = 'blue'
        colors[12] = 'rgb(250, 100, 10)'
    
    if all_yellows != 0:
        all_yellows = int(stats[0][6]) * 40 / all_yellows
        colors[5] = 'blue'
        colors[13] = 'rgb(250, 100, 10)'

    if all_offsides != 0:
        all_offsides = int(stats[0][12]) * 40 / all_offsides
        colors[6] = 'blue'
        colors[14] = 'rgb(250, 100, 10)'

    if all_corners != 0:
        all_corners = int(stats[0][14]) * 40 / all_corners
        colors[7] = 'blue'
        colors[15] = 'rgb(250, 100, 10)'
        

    return all_shots, all_goals, all_passes, all_fouls, all_reds, all_yellows, all_offsides, all_corners, *colors