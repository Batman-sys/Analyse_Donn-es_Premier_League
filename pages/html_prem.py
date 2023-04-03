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
from match_data import *
from htmlmatchlib import *
from html_prem_div import *
from plotly_football_pitch import (
    make_pitch_figure,
    PitchDimensions,
    SingleColourBackground,
    add_heatmap
)



dash.register_page(__name__, path='/')


names_crests =  pd.read_csv('./teams.csv')
team_list = names_crests['Team A'].values.tolist()





layout = html.Div(className = "Mother_div",children=[
    
    html.H1("Match Statistics", style = {'text-align': 'center'}),
    
    html.Br(),
    html.Div(className="row", children=[
            html.Div(className='six columns', children=[
                dcc.Dropdown(options = [], value = team_list[0], id='team1')], style=dict(width='50%'))
            , html.Div(className='six columns', children=[
                dcc.Dropdown(options = [], value = team_list[1], id='team2')], style=dict(width='50%'))
        ],
     style=dict(display='flex')),
    dcc.Slider(min = 0.1, max = 120, marks = None,
               value=45,
               id='drag'
    ),
   html.Div(className = 'foreground', children = [
   *stats_div(),
   *graphs(),
   html.Div(className = "Stats", children = [
            (dcc.Graph(id = 'offensiveness', figure = {}))
            
            ], style={'text-align': 'center'}),
   ]),
   

    

])

#Update team list
@callback(
    [Output('team1', 'options'),Output('team2', 'options')],
    [Input('team2', 'value'), Input('team1', 'value')]
)
def update_output(t1, t2):
    new_list1 = cp.copy(team_list)
    new_list1.remove(t1)
    new_list = cp.copy(team_list)
    new_list.remove(t2)
    return new_list1, new_list

#Update Slider
@callback(
    Output('drag','max'),
    [Input('team1', 'value'),
     Input('team2', 'value')]
    
)
def update_output(team1, team2):
    df = importing_events(team1, team2)
    match_length = math.ceil(df.Time.values[-1:][0])
    return match_length


#Update stats
outputlist = [
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
@callback(
    outputlist
    ,
    [Input('team1', 'value'),
     Input('team2', 'value'),
     Input('drag', 'value')]
)

def update_output(team1, team2, minute):
        #update match stats
        df = importing_events(team1, team2)
        stats = statistics(df.copy(), team1, team2, minute)
        pie_poss_teams = pie_poss(stats)
        lbars = bars(stats)
        crest1 = names_crests[(names_crests['Team A'] == team1)]['crest']
        crest2 = names_crests[(names_crests['Team A'] == team2)]['crest']
        return str(minute) + "'", *crest1, *crest2, *stats[1:], *pie_poss_teams, *lbars

#Offensiveness Graph
@callback(
    Output('offensiveness', 'figure'),
    [Input('team1', 'value'),
     Input('team2', 'value'),
     Input('drag', 'value')]

)
def update_output(team1, team2, minute):
        df = importing_events(team1, team2)
        df['Offensiveness'] = np.where(df['Player1 Team'] == team2, -df['Offensiveness'], df['Offensiveness'])
        team_off = df[df['Time'] <= minute]
        fig = px.line(team_off, x="Time", y="Offensiveness", color='Player1 Team')

        
        return fig

#Graphs
@callback(
    [
     Output('shooting_zones', 'figure'),
     Output('action_venues', 'figure'),
     Output('xG_Goal', 'figure'),
     Output('team_shots', 'figure'),
     Output('heatmap', 'figure'),
     Output('sides_used', 'figure')
    ],
    [Input('team1', 'value'),
     Input('team2', 'value'),
     Input('drag', 'value')]
)
def update_output(team1, team2, minute):
    df = importing_events(team1, team2)
    return plot_shooting_zones(df, team1, team2, minute), heatmap_action_venues(df, team1, team2, minute), plot_xG_goal(df, team1, team2, minute), draw_team_shot(df, team1, team2, minute), heatmap(df, team1, team2, minute), plot_sides_used(df, team1, team2, minute)
       




