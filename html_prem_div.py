import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd


crest = pd.read_csv('./teams.csv')['crest'].values.tolist()
def stats_div():
    return html.Div(className = 'foreground', children = [
        html.Div(className = 'time', children = html.H6('',id = 'minute', style = {'text-align': 'center'})),
        html.Div(className='teams', children=[
            html.Img(id='crest1', className = 'crest',src=crest[0]),
            html.H3(" - ", className = 'crest',  style = {'text-align': 'center'}),
            html.Img(id = 'crest2', className = 'crest', src=crest[1]),
        ]),
        html.Div(className = "Stats", children = [
            html.H3("0 Goals 0", id = 'Goals',  style = {'text-align': 'center'}),
            html.Div(className = 'goal_bar',id = 'goal_bar', children=[
            dbc.Progress(id = 'goal1_progress', value = 20, color = 'blue' , bar = True),
            dbc.Progress(id = 'goal2_progress', value = 40, color = 'red', bar = True)
            ]),
            html.Br(),
            html.Br(),

            html.H3('Possession',  style = {'text-align': 'center'}),
            
            html.Br(),
            html.Br(),

            html.H3('0 Shots 0', id = 'Shots',  style = {'text-align': 'center'}),
            html.Div(className = 'shot_bar', children=[
                dbc.Progress(id = 'shot1_progress', value = 20, color = 'blue' , bar = True),
                dbc.Progress(id = 'shot2_progress', value = 40, color = 'red', bar = True)
            ]),
            html.Br(),
            html.Br(),

            html.H3('0 Passes 0', id = 'Passes',  style = {'text-align': 'center'}),
            html.Div(className = 'pass_bar', children=[
            dbc.Progress(id = 'pass1_progress', value = 20, color = 'blue' , bar = True),
            dbc.Progress(id = 'pass2_progress', value = 40, color = 'red', bar = True)
            ]), 
            html.Br(),
            html.Br(),

            html.H3('0 Fouls 0', id = 'Fouls',  style = {'text-align': 'center'}),
            html.Div(className = 'foul_bar', children=[
                dbc.Progress(id = 'foul1_progress', value = 20, color = 'blue' , bar = True),
                dbc.Progress(id = 'foul2_progress', value = 40, color = 'red', bar = True)
            ]),
            html.Br(),
            html.Br(),

            html.H3('0 Reds 0', id = 'Reds',  style = {'text-align': 'center'}),
            html.Div(className = 'reds_bar', children=[
                dbc.Progress(id = 'red1_progress', value = 20, color = 'blue' , bar = True),
                dbc.Progress(id = 'red2_progress', value = 40, color = 'red', bar = True)
            ]),
            html.Br(),
            html.Br(),
                    
            html.H3('0 Yellows 0', id = 'Yellows',  style = {'text-align': 'center'}),
            html.Div(className = 'yellows_bar', children=[
                dbc.Progress(id = 'yellow1_progress', value = 20, color = 'blue' , bar = True),
                dbc.Progress(id = 'yellow2_progress', value = 40, color = 'red', bar = True)
            ]),
            html.Br(),
            html.Br(),

                            
            html.H3('0 Offsides 0', id = 'Offsides',  style = {'text-align': 'center'}),
            html.Div(className = 'offsides_bar', children=[
                dbc.Progress(id = 'offside1_progress', value = 20, color = 'blue' , bar = True),
                dbc.Progress(id = 'offside2_progress', value = 40, color = 'red', bar = True)
            ]),
            html.Br(),
            html.Br(),

                            
            html.H3('0 Corners 0', id = 'Corners',  style = {'text-align': 'center'}),
            html.Div(className = 'corners_bar', children=[
                dbc.Progress(id = 'corner1_progress', value = 20, color = 'blue' , bar = True),
                dbc.Progress(id = 'corner2_progress', value = 40, color = 'red', bar = True)
            ]),
            html.Br(),
            html.Br(),



        

        html.Div(className = "Pies", children = [
            dcc.Graph(id = 'pie_possession1', figure = {}),
            dcc.Graph(id = 'pie_possession2', figure = {}),
            ]),
        
        
        
        
    

    

    

    

    

    
    ], style=dict(display='grid'))
    
        ])