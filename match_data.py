import numpy as np
import pandas as pd
import os 
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
#import seaborn as sb
from pathlib import Path
from pandas import *
from matplotlib.patches import Arc
from matplotlib.patches import Rectangle
import plotly.graph_objs as go
from plotly_football_pitch import make_pitch_figure, PitchDimensions, add_heatmap
import random
import base64
import plotly.graph_objs as go
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots



def importing_events(team1, team2):
  path = './EPL_2011_12/Events/'
  files = os.listdir(path)
  df = pd.DataFrame()
  n = '*' + team1 + ' v ' + team2 + ' - Events.csv'
  for f in Path(path).glob(n):
    df = pd.read_csv(f)
  #df.Time = df.Time  + (45*60 * df.Half)
  df.Time = df.Time / 60 + ( 45 * df.Half )
  return df[[
    "Match Name", "Team A", "Team B", "Half", "Time", "Event Name",
    "Player1 Name", "Player1 Team", "Player2 Name", "X", "Y", "Offensiveness",
    "Possession", "Active Team", "Player Transition", "Goal Difference",
    "Possession Number", "Move Number", "xG Score"
  ]]


def xG_Score(df, team1, team2):
    #df = importing_events(team1, team2)
    
    df1 = df[df["Player1 Team"] == team1]
    fig1 = go.Figure(data=go.Scatter(x=df1['Time'], y=df1['xG Score'], name=team1))
    fig1.update_layout(title_text=team1)
    
    df2 = df[df["Player1 Team"] == team2]
    fig2 = go.Figure(data=go.Scatter(x=df2['Time'], y=df2['xG Score'], name=team2))
    fig2.update_layout(title_text=team2)
    
    return fig1.show() , fig2.show()
    
 
 def Offensiveness(df, team1, team2):
    
    #df = importing_events(team1, team2)
    
    df1 = df[df["Player1 Team"] == team1]
    fig1 = px.line(df1, x="Time", y="Offensiveness", title=team1)
    
    df2 = df[df["Player1 Team"] == team2]
    fig2 = px.line(df2, x="Time", y="Offensiveness", title=team2)

    return fig1.show(), fig2.show()
    
    
    
def Nb_Pass_succ(df, team1, team2):    
    #df = importing_events(team1, team2)
    team_1 = 0
    team_2 = 0
    for (i,j,k) in zip(df["Event Name"], df["Player1 Team"], df["Player1 Team"][1::] ):
        
        if ( i == "Pass" ) & ( j == team1) & ( k == team1 ):
            team_1 += 1
            
    for (i,j,k) in zip(df["Event Name"], df["Player1 Team"], df["Player1 Team"][1::] ):
        
        if ( i == "Pass" ) & ( j == team2) & ( k == team2 ):
            team_2 += 1
    return team_1, team_2

def Nb_Pass_miss(df, team1, team2):    
    #df = importing_events(team1, team2)
    team_1 = 0
    team_2 = 0
    for (i,j,k) in zip(df["Event Name"], df["Player1 Team"], df["Player1 Team"][1::] ):
        
        if ( i == "Pass" ) & ( j == team1) & ( k != team1 ):
            team_1 += 1
            
    for (i,j,k) in zip(df["Event Name"], df["Player1 Team"], df["Player1 Team"][1::] ):
        
        if ( i == "Pass" ) & ( j == team2) & ( k != team2 ):
            team_2 += 1
    return team_1, team_2

def Pass(df, team1, team2):
    #df = importing_events(team1, team2)
    team_1_pass = len(df[ (df["Event Name"]=="Pass") & (df["Player1 Team"]== team1)])
    team_1_succ = Nb_Pass_succ(team1, team2)[0]
    team_1_miss = Nb_Pass_miss(team1, team2)[0]
    team_2_pass = len(df[ (df["Event Name"]=="Pass") & (df["Player1 Team"]== team2)])
    team_2_succ = Nb_Pass_succ(team1, team2)[1]
    team_2_miss = Nb_Pass_miss(team1, team2)[1]
    return (team_1_pass, team_1_succ, team_1_miss), (team_2_pass, team_2_succ, team_2_miss)


def match_stats(df, Team1, Team2, minutes):
  df = importing_events(Team1, Team2)

  goal_team1 = len(
    df[(df["Time"] < minutes)
       & (((df["Event Name"] == "Goal") & (df["Player1 Team"] == Team1)) | (
         (df["Event Name"] == "Own Goal") & (df["Player1 Team"] == Team2)))])
  goal_team2 = len(
    df[(df["Time"] < minutes)
       & (((df["Event Name"] == "Goal") & (df["Player1 Team"] == Team2)) | (
         (df["Event Name"] == "Own Goal") & (df["Player1 Team"] == Team1)))])
  shot_team1 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Shot")) &
       (df["Player1 Team"] == Team1)])
  shot_team2 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Shot")) &
       (df["Player1 Team"] == Team2)])
  redCard_team1 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Red Card")) &
       (df["Player1 Team"] == Team1)])
  redCard_team2 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Red Card")) &
       (df["Player1 Team"] == Team2)])
  yellowCard_team1 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Yellow Card"))
       & (df["Player1 Team"] == Team1)])
  yellowCard_team2 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Yellow Card"))
       & (df["Player1 Team"] == Team2)])
  pass_team1 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Pass")) &
       (df["Player1 Team"] == Team1)])
  pass_team2 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Pass")) &
       (df["Player1 Team"] == Team2)])
  foul_team1 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Foul")) &
       (df["Player1 Team"] == Team1)])
  foul_team2 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Foul")) &
       (df["Player1 Team"] == Team2)])
  offSide_team1 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Offside")) &
       (df["Player1 Team"] == Team1)])
  offSide_team2 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Offside")) &
       (df["Player1 Team"] == Team2)])
  corners_team1 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Corner")) &
       (df["Player1 Team"] == Team1)])
  corners_team2 = len(
    df[(df["Time"] < minutes) & (df["Event Name"].str.contains("Corner")) &
       (df["Player1 Team"] == Team2)])

  total_possession = len(
    df[(df["Time"] < minutes)
       & ((df["Player1 Team"] == Team2) | (df["Player1 Team"] == Team1))])
  possession_team1 = len(
    df[(df["Time"] < minutes)
       & (df["Player1 Team"] == Team1)]) / total_possession * 100
  possession_team2 = len(
    df[(df["Time"] < minutes)
       & (df["Player1 Team"] == Team2)]) / total_possession * 100

  return goal_team1, goal_team2, shot_team1, shot_team2, redCard_team1, redCard_team2, yellowCard_team1, yellowCard_team2, pass_team1, pass_team2, foul_team1, foul_team2, offSide_team1, offSide_team2, corners_team1, corners_team2, possession_team1, possession_team2


# partie du terrain correspondant à l'équipe adverse découpé en 3 parties ( sur la longueur )
# cotés utilisés.

def sides_used(df, team1, team2, minutes):
    #df = importing_events(team1, team2)
    total1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) ])
    total2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) ])
    #print(total1,total2)
    left_side1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] > 12)  ])
    left_side1 = left_side1 / total1
    middle1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] < 12) & (df["Y"] > -12) ])
    middle1 = middle1 / total1
    right_side1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] < -12)  ])
    right_side1 = right_side1 / total1
    
    left_side2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & (df["Y"] < -12)  ])
    left_side2 = left_side2 / total2
    middle2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & (df["Y"] < 12) & (df["Y"] > -12) ])
    middle2 = middle2 / total2
    right_side2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & (df["Y"] > 12)  ])
    right_side2 = right_side2 / total2
    
    return (left_side1, middle1, right_side1), (left_side2, middle2, right_side2)
            
            
            
# partie du terrain correspondant à l'équipe adverse découpé en 3 parties ( sur la longueur )

def Directions_of_shots(df, team1, team2, minutes):
    #df = importing_events(team1, team2)
    total1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    total2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    print(total1, total2)
    
    left_side1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] > 12) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross")) ])
    left_side1 = left_side1 / total1
    middle1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] < 12) & (df["Y"] > -12) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    middle1 = middle1 / total1
    right_side1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] < -12) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross")) ])
    right_side1 = right_side1 / total1
    
    left_side2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & (df["Y"] < -12)  & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    left_side2 = left_side1 / total2
    middle2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & (df["Y"] < 12) & (df["Y"] > -12) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    middle2 = middle2 / total2
    right_side2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & (df["Y"] > 12)  & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    right_side2 = right_side2 / total2
    
    return (left_side1, middle1, right_side1), (left_side2, middle2, right_side2)
    
    
    

# partie du terrain correspondant à l'équipe adverse 
    
def Shooting_zones(df, team1, team2, minutes):
    #df = importing_events(team1, team2)
    total1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    total2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    #print(total1, total2)
    
    six_meters1 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] >= -50) & ( df["Y"] <= 3.5 ) & ( df["Y"] >= -3.5) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    six_meters1 = ( six_meters1 / total1 ) * 100
    eighteen_meters1 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] >= -50) & ( df["Y"] <= -3.5 ) & ( df["Y"] >= -14.5) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    eighteen_meters1 += len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] >= -50) & ( df["Y"] <= 14.5 ) & ( df["Y"] >= 3.5) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    eighteen_meters1 += len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] <= -50) & (df["X"] <= -40) & ( df["Y"] >= -14.5 ) & ( df["Y"] <= 14.5) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))]) 
    eighteen_meters1 = ( eighteen_meters1 / total1 ) * 100
    outside_area1 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] <= -40) & (df["X"] <= 0) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    outside_area1 += len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] >= -40) & ( df["Y"] >= 14.5 ) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    outside_area1 += len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] >= -40) & ( df["Y"] <= -14.5 ) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))]) 
    outside_area1 = (outside_area1 / total1) * 100
    
    six_meters2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] <= -50) & ( df["Y"] <= 3.5 ) & ( df["Y"] >= -3.5) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    six_meters2 = ( six_meters2 / total2 ) * 100
    eighteen_meters2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] <= -50) & ( df["Y"] <= -3.5 ) & ( df["Y"] >= -14.5) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    eighteen_meters2 += len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] <= -50) & ( df["Y"] <= 14.5 ) & ( df["Y"] >= 3.5) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    eighteen_meters2 += len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] >= -50) & (df["X"] <= -40) & ( df["Y"] >= -14.5 ) & ( df["Y"] <= 14.5) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))]) 
    eighteen_meters2 = ( eighteen_meters2 / total2 ) * 100
    outside_area2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] >= -40) & (df["X"] <= 0) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    outside_area2 += len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] <= -40) & ( df["Y"] >= 14.5 ) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    outside_area2 += len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] <= -40) & ( df["Y"] <= -14.5 ) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))]) 
    outside_area2 = (outside_area2 / total2) * 100
    
    return ( str(six_meters1) + "%", str(eighteen_meters1) + "%", str(outside_area1) + "%"),( str(six_meters2) + "%", str(eighteen_meters2) + "%", str(outside_area2) + "%") 
    
    
    
# partie du terrain découpé en 3 parties (largeur) : Tiers_gauche, Milieu, Tiers_droit

def Action_areas(df, team1, team2, minutes):
    #df = importing_events(team1, team2)
    total = len(df[(df["Time"] < minutes)])
    Tiers_gauche = len(df[ ( ( df["Player1 Team"] == team1 ) | ( df["Player1 Team"] == team2 ) ) & (df["Time"] < minutes) & (df["X"] <= -18.4) ])
    Tiers_gauche = (Tiers_gauche / total) * 100
    Milieu = len(df[ ( ( df["Player1 Team"] == team1 ) | ( df["Player1 Team"] == team2 ) ) & (df["Time"] < minutes) & (df["X"] >= -18.4) & (df["X"] <= 18.4) ])
    Milieu = (Milieu / total) * 100
    Tiers_droit = len(df[ ( ( df["Player1 Team"] == team1 ) | ( df["Player1 Team"] == team2 ) ) & (df["Time"] < minutes) & (df["X"] >= 18.4) ])
    Tiers_droit = (Tiers_droit / total) * 100

    return ( str(round(Tiers_gauche)) + " %",str(round(Milieu)) + "%", str(round(Tiers_droit)) + "%" )
    
    
def plot_cotes_utilises(df, team1, team2, minutes):
    # Obtenir les données des côtés utilisés pour chaque équipe
    side1, side2 = sides_used(df, team1, team2, minutes)

    # Créer les traces pour chaque équipe
    trace1 = go.Bar(x=['Côté gauche', 'Milieu', 'Côté droit'], y = side1, name = team1)
    trace2 = go.Bar(x=['Côté gauche', 'Milieu', 'Côté droit'], y = side2, name = team2)

    # Créer la figure et l'afficher
    fig = go.Figure(data=[trace1, trace2])
    fig.update_layout(title=f'Côtés utilisés par {team1} et {team2} pendant les premières {minutes} minutes', barmode='group')
    return fig
    

def draw_team_pass(df_events, team, minutes):
        title = str(team) + " pass locations"
        d = df_events.loc[(df_events['Player1 Team']==team)&(df_events['Event Name']=='Pass'),['X','Y']]
        h = df_events['Half']
        x=df_events['X']
        y = df_events['Y']
        l=[]
        fig = go.Figure()
        pitch = base64.b64encode(open('./pitch.jpeg', 'rb').read())
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
        for i in d.index:
            x1 = x.iloc[i]
            y1 = y.iloc[i]
            x2 = x.iloc[i+1]
            y2 = y.iloc[i+1]
            if(h.iloc[i]==1):
                x1=-x1
                x2=-x2
                y1=-y1
                y2=-y2
            arrow = go.layout.Annotation(dict(
                        x= x2,
                        y= y2,
                        xref="x", yref="y",
                        text="",
                        axref = "x", ayref='y',
                        ax= x1,
                        ay= y1,
                        arrowhead = 3,
                        arrowwidth= 1.5,
                        arrowcolor='rgb(255,51,0)',)
                    )
            l.append(arrow)
        fig.update_layout(annotations= l)

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
        
        
        
 
    
def heatmap(df, team1, team2, minutes):
    df = df.copy()
    df["X"] += 55
    df["Y"] += 40
    
    dimensions = PitchDimensions()
    fig = make_pitch_figure(
    dimensions,
    pitch_background=SingleColourBackground("#81B622"),
    )

    # define number of grid squares for heatmap data
    width_grid = 10
    length_grid = 10

    data = np.array([
        [len(df.loc[(df['Player1 Team']=='Manchester United') & (df['Y']<=68/width_grid + 68/width_grid*i ) & (df['Y']>68/width_grid + 68/width_grid*(i-1)) & (df['X']<=105/length_grid + 105/length_grid*j)& (df['X']>105/length_grid + 105/length_grid*(j-1)) ,['X','Y']]) for i in range(length_grid)]
        for j in range(width_grid)
    ])
    fig = add_heatmap(fig, data)
    return fig.show()
    
    
n
