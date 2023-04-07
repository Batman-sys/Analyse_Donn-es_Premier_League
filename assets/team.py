import numpy as np
import pandas as pd
import os
import plotly.graph_objs as go
import math
import copy as cp
from plotly_football_pitch import make_pitch_figure, PitchDimensions, add_heatmap,SingleColourBackground
###################################################""
def importing_team_events(team):
    path = ".\\EPL_2011_12\\Team_Events\\" + team + '.csv'
    df = pd.read_csv(path)
    return df
###################################################
def importing_team_players(team):
    df = pd.read_csv(".\\assets\\player_team.csv")
    path = ".\\EPL_2011_12\\Players"
    files = os.listdir(path)
    files = [f for f in files if np.str_(f).__contains__(team)]
    df = pd.DataFrame()
    for f in files:
        #f for the file's path
        '''We used concat to get a dataframe containing 
        all the matches in a single dataframe'''
        df = pd.concat([df,pd.read_csv(path + "\\" +f)])
    return df.reset_index()
#########################################################""
def xgoals(team, df_players):
    d = df_players[df_players['Team']==team][['Match Name', 'xGoals Shot']]
    groups = d.groupby('Match Name')
    return np.sum(groups.sum()['xGoals Shot'])
############################################""
def plot_shots(team,df_events,df_players):
    fig = go.Figure()
    fig = go.Figure(data=[go.Bar(
    x=['xGoals' , 'Goals scored', 'Goals conceded'],
    y=[xgoals(team,df_players) , goals(team,df_events)[1] , goals(team,df_events)[0] ],
    marker_color= ['lightblue', 'green', 'red']
    )])
    fig.update_layout(title = 'Nombre de buts réalisés, reçus et espérés par '+team)
    return fig
################################################
def goals(team,df):
    d = df.loc[(df['Event Name'] == 'Goal') | (df['Event Name'] == 'Own Goal')]
    received = d.loc[((d['Player1 Team'] != team) & (d['Event Name'] == 'Goal')) | ((d['Player1 Team'] == team) & (d['Event Name'] == 'Own Goal'))]
    return len(received) , len(d)-len(received) 
#####################################################
def shot( team ,shot, df_events):
    d = df_events.loc[(df_events['Team A'] == team) & (df_events['Event Name'] == shot)]
    return len(d)
###################################################
def plot_shots2(team,df_events):
    shots = df_events.loc[(df_events['Team A']==team) & (df_events['Event Name'].str.contains('Shot'))]['Event Name'].unique()
    fig = go.Figure()
    fig = go.Figure(go.Bar(
    x=shots,
    y=[shot(team,i,df_events) for i in shots ]
    ))
    fig.update_layout(title = 'Nombre des tirs réalisées par '+team)
    return fig
#####################################################
def match_result_season(team,df_players):
    d = df_players.loc[df_players['Team'] == team][['Match Name','Result']]
    groups = d.groupby('Match Name')
    result = groups['Result'].unique()
    l = np.where(result == "L")[0]
    w = np.where(result == "W")[0]
    n = np.where(result == "D")[0]
    
    return len(l) , len(w) , len(n)
#######################################################""
def pie_chart_match_result(team,df_players):
    distros = ['Matches perdus', 'Matches gagnés', 'Matches nuls']
    l,w,n = match_result_season(team,df_players)
    usage = [l,w,n]

    fig = go.Figure(data=[go.Pie(
        labels=distros,
        values=usage,
        textinfo='label+percent',
        hole=.5,
        insidetextorientation='radial'),],
        layout=go.Layout(
                annotations=[{'text': str(usage[1]*3 + usage[2]) + ' Points', 'x':0.50, 'y':0.5, 'font_size':12, 'showarrow':False}],
                showlegend=False
            ))
    return fig
########################################################
def heatmap_action_venues(df, team, minutes):
    dfr = cp.copy(df)
    minutes *= 60
    title = str(team) + " touch locations"
    data = Action_areas(df, team, minutes)
    # Création de la figure avec la carte de chaleur et l'image de terrain
    dimensions = PitchDimensions()
    fig = make_pitch_figure(
    dimensions,
    pitch_background=SingleColourBackground("#81B622"),
    )
        
    fig = add_heatmap(fig, np.array(data))
    fig.update_layout(
    title="Action Venues ",
    xaxis_title="X Axis Title",
    yaxis_title="Y Axis Title",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="Black"
        )
    )
    return fig
#########################################################""
def Action_areas(df, team , minutes):
    dfr = df[(df["Player1 Team"] == team)& (df["Time"] < minutes) ][["X",'Half','Y','Time']]
    dfr.X = (-1)**dfr.Half*dfr.X+52
    dfr.Y = (-1)**dfr.Half*dfr.Y  +34
    total = len(dfr)
    
    Tiers_gauche = len(dfr[   (dfr["X"] <= -18.4) ])
    Tiers_gauche = (Tiers_gauche / total) * 100
    Milieu = len(dfr[ (dfr["X"] >= -18.4) & (dfr["X"] <= 18.4) ])
    Milieu = (Milieu / total) * 100
    Tiers_droit = len(dfr[  (dfr["X"] >= 18.4) ])
    Tiers_droit = (Tiers_droit / total) * 100

    return [[math.ceil(Tiers_gauche) ,math.ceil(Milieu) ,math.ceil(Tiers_droit)]]
#################################################
def sides_used(df, team ,minutes):
    df = df.loc[( df["Player1 Team"] == team) ][["Time","X","Y","Half"]]
    df.X = (-1)**df.Half*df.X
    df.Y = (-1)**df.Half*df.Y  
    
    total1 = len(df[ (df["Time"] < minutes) & (df["X"] > 0) ])
    left_side1 = len(df[  (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] > 12)  ])
    left_side1 = left_side1 / total1
    middle1 = len(df[(df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] < 12) & (df["Y"] > -12) ])
    middle1 = middle1 / total1
    right_side1 = len(df[ (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] < -12)  ])
    right_side1 = right_side1 / total1
    
    return (left_side1, middle1, right_side1)
######################################################################
def plot_sides_used(df, team, minutes):
    df = cp.copy(df)
    # Obtenir les données des côtés utilisés pour chaque équipe
    side = sides_used(df, team, minutes)

    # Créer la figure et l'afficher
    fig = go.Figure(go.Bar(x=['Côté gauche', 'Milieu', 'Côté droit'], y = side, name = team))
    fig.update_layout(title=f'Côtés utilisés par {team} pendant les premières {minutes/60} minutes ', barmode='group')
    return fig
#########################################################################"
# ZONES DES TIRS
def Shooting_zones(df, team1, minutes):
    
    total1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["Half"] == 0) & (df["X"] < 0) & (df["Event Name"].str.contains("Shot") ) ])
    total1 += len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["Half"] == 1) & (df["X"] > 0) & (df["Event Name"].str.contains("Shot") )])
   
    six_meters1 = 0
    eighteen_meters1 = 0
    outside_area1 = 0
    six_meters2 = 0
    eighteen_meters2 = 0
    outside_area2 = 0
    
    if total1 == 0:
        total1 = 1
        six_meters1 = 0
        eighteen_meters1 = 0
        outside_area1 = 0
       
    
    six_meters1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["Half"] == 0) & (df["X"] <= 50) & ( df["Y"] < 7 ) & ( df["Y"] > -7) & (df["Event Name"].str.contains("Shot") )])
    six_meters1 += len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["Half"] == 1) & (df["X"] >= 50) & ( df["Y"] < 7) & ( df["Y"] > -7) & (df["Event Name"].str.contains("Shot") )])

        
    eighteen_meters1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["Half"] == 0) & (df["X"] <= 42) & (df["Y"] < 14) & (df["Y"] > -14) & (df["Event Name"].str.contains("Shot") )])
    eighteen_meters1 += len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["Half"] == 1) & (df["X"] >= 42) & (df["Y"] < 14) & (df["Y"] > -14) & (df["Event Name"].str.contains("Shot") )])
    eighteen_meters1 -= six_meters1

    outside_area1 = total1 - ( eighteen_meters1 + six_meters1 )

    
    six_meters1 = np.where(total1 > 0, six_meters1 / total1, 0) * 100
    eighteen_meters1 = np.where(total1 > 0, eighteen_meters1 / total1 , 0) * 100
    outside_area1 = np.where(total1 > 0, outside_area1 / total1 , 0) * 100
    
    return (six_meters1, eighteen_meters1, outside_area1) 
# #############################################################
def plot_shooting_zones(df, team, minutes):
    # Obtenir les données des côtés utilisés pour chaque équipe
    team_shot= Shooting_zones(df, team, minutes)

    # Créer les traces pour chaque équipe
    trace = go.Bar(x=['6 mètres', '18 mètres', 'Extérieur de la surface'], y = team_shot, name = team)

    # Créer la figure et l'afficher
    fig = go.Figure(data=[trace])
    fig.update_layout(title=f'Zones de tirs des équipes : {team} pendant les premières {minutes/60} minutes ', barmode='group')
    return fig
