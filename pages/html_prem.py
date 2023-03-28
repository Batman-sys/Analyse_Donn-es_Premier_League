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
    df.Time = df.Time / 60
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
        minute *= 60
        stats = statistics(team1, team2, minute)
        pie_poss_teams = pie_poss(stats)
        lbars = bars(stats)
        crest1 = names_crests[(names_crests['Team A'] == team1)]['crest']
        crest2 = names_crests[(names_crests['Team A'] == team2)]['crest']
        return str(minute/60) + "'", *crest1, *crest2, *stats[1:], *pie_poss_teams, *lbars

#Offensiveness Graph
@callback(
    Output('offensiveness', 'figure'),
    [Input('team1', 'value'),
     Input('team2', 'value'),
     Input('drag', 'value')]

)
def update_output(team1, team2, minute):
        minute *= 60
        df = importing_events(team1, team2)
        df['Offensiveness'] = np.where(df['Player1 Team'] == team2, -df['Offensiveness'], df['Offensiveness'])
        team_off = df[df['Time'] <= minute]
        fig = px.line(team_off, x="Time", y="Offensiveness", color='Player1 Team')

        
        return fig

#Graphs

#ball possession per team
@callback(
      [Output('team1_ball_poss', 'figure'),
       Output('team1_touches', 'figure')
      ],
      [Input('team1', 'value'),
    Input('team2', 'value'),
     Input('drag', 'value'),]
)
def update_output(team1, team2, minute):
        minute *= 60
        title = str(team1) + " touch locations"
        df = importing_events(team1, team2)
        team_pos = df[(df['Time'] <= minute) & (df['Player1 Team'] == team1)]
        x=team_pos['X'].values.tolist()
        y=team_pos['Y'].values
        fig = go.Figure(data=[])
        pitch = base64.b64encode(open('pitch.jpg', 'rb').read())
        fig.add_trace(go.Scatter(x = x, y = y, mode='markers', marker_color = 'blue' ))
        fig.add_layout_image(dict(source='data:image/png;base64,{}'.format(pitch.decode()),
                            xref= "x",
                            yref= "y",
                            x=-55,
                            y=40,
                            sizex=55 * 2,
                            sizey=40 * 2,
                            sizing= "stretch",
                            opacity= 1,
                            layer= "below"))
        fig.update_layout(
            title=title,
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="RebeccaPurple"
            ),
            xaxis = dict(showgrid=False), 
            yaxis = dict(showgrid = False), 
            yaxis_range=[-40,40], 
            xaxis_range=[-55, 55]
        )
        team_pos["X"] += 53
        team_pos["Y"] += 35
        x=team_pos['X'].values.tolist()
        y=team_pos['Y'].values
        dimensions = PitchDimensions()
        fig1 = make_pitch_figure(
            dimensions,
            pitch_background=SingleColourBackground("#81B622"),
        )

        # define number of grid squares for heatmap data
        width_grid = 1
        length_grid = 2
        Mx = 53*2
        My = 35*2
        data = []
        for i in range(length_grid):
               l = []
               for j in range(width_grid):
                      k = i * Mx/length_grid
                      k_prev = (i-1) * Mx/length_grid
                      p = j * My/width_grid
                      p_prev = (j-1) * My/width_grid
                      l.append(len(team_pos[(team_pos['X'] <= Mx/length_grid + k) & (team_pos['X'] > Mx/length_grid + k_prev) &
                                   (team_pos['Y'] <= My/width_grid + p) & (team_pos['Y'] > My/width_grid + p_prev)]))
                      
               data.append(l)
        fig1.add_trace(go.Scatter(x = x, y = y, mode='markers', marker_color = 'blue' ))
        fig1 = add_heatmap(fig1, np.array(data))

        
        return fig, fig1







@callback(
      Output('team2_ball_poss', 'figure'),
      [Input('team1', 'value'),
    Input('team2', 'value'),
     Input('drag', 'value'),]
)

def update_output(team1, team2, minute):
        minute *= 60
        title = str(team2) + " touch locations"
        df = importing_events(team1, team2)
        team_pos = df[(df['Time'] <= minute) & (df['Player1 Team'] == team2)]
        x=team_pos['X'].values
        y=team_pos['Y'].values
        fig = go.Figure(data=[])
        pitch = base64.b64encode(open('pitch.jpg', 'rb').read())
        fig.add_trace(go.Scatter(x = x, y = y, mode='markers', marker_color = 'orange'))
        fig.add_layout_image(dict(source='data:image/png;base64,{}'.format(pitch.decode()),
                            xref= "x",
                            yref= "y",
                            x=-55,
                            y=40,
                            sizex=55 * 2,
                            sizey=40 * 2,
                            sizing= "stretch",
                            opacity= 0.8,
                            layer= "below"))
        fig.update_layout(
            title=title,
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="RebeccaPurple"
            ),
            xaxis = dict(showgrid=False), 
            yaxis = dict(showgrid = False), 
            yaxis_range=[-40,40], 
            xaxis_range=[-55, 55]
        )

        return fig



