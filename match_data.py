import numpy as np
import pandas as pd
import os
import plotly.express as px
import matplotlib.pyplot as plt
#import seaborn as sb
from pathlib import Path
#from pandas import *
#from matplotlib.patches import Arc


def importing_events(team1, team2):
  path = './EPL_2011_12/Events/'
  files = os.listdir(path)
  df = pd.DataFrame()
  #team = "Blackburn Rovers"
  #team2 = "Wolverhampton Wanderers"
  n = '*' + team1 + ' v ' + team2 + ' - Events.csv'
  for f in Path(path).glob(n):
    df = pd.read_csv(f)
  df.Time = df.Time  + (45*60 * df.Half)
  return df[[
    "Match Name", "Team A", "Team B", "Half", "Time", "Event Name",
    "Player1 Name", "Player1 Team", "Player2 Name", "X", "Y", "Offensiveness",
    "Possession", "Active Team", "Player Transition", "Goal Difference",
    "Possession Number", "Move Number", "xG Score"
  ]]


def Nb_Pass_succ(team):    
    
    #df = importing_events(team1, team2)
    
    a = 0
    for (i,j,k) in zip(df["Event Name"], df["Player1 Team"], df["Player1 Team"][1::] ):
        
        if ( i == "Pass" ) & ( j == team) & ( k == team ):
            a += 1
    return a

def Nb_Pass_miss(team):    
    a = 0
    for (i,j,k) in zip(df["Event Name"], df["Player1 Team"], df["Player1 Team"][1::] ):
        
        if ( i == "Pass" ) & ( j == team) & ( k != team ):
            a += 1
    return a

def Pass(team):
    Nb_Pass = len(df[ (df["Event Name"]=="Pass") & (df["Player1 Team"]== team)])
    NbPass_succ = Nb_Pass_succ(team)
    NbPass_miss = Nb_Pass_miss(team)
    return Nb_Pass, NbPass_succ, NbPass_miss
    
#passes("Manchester United")

Pass("Chelsea")


def offensiveness(Team1, Team2):
  df = importing_events(Team1, Team2)

  #offensive_team1 = len(df[ (df["Time"] < minutes) & ((df["Offensiveness"] != 0) & (df["Player1 Team"] == Team1)) ] )
  #offensive_team2 = len(df[ (df["Time"] < minutes) & (df["Event Name"].str.contains("Shot") ) & (df["Player1 Team"] == Team2 )])
  lteam1 = df[df["Player1 Team"] == Team1][['Player1 Team', 'Offensiveness']]
  lteam2 = df[df["Player1 Team"] == Team2][['Player1 Team', 'Offensiveness']]

  return lteam1, lteam2


def match_stats(Team1, Team2, minutes):
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

def côtés_Utilisés(team1, team2, minutes):
    df = importing_events(team1, team2)
    total1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) ])
    total2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) ])
    print(total1,total2)
    Côté_Gauche1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] > 12)  ])
    Côté_Gauche1 = Côté_Gauche1 / total1
    Milieu = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] < 12) & (df["Y"] > -12) ])
    Milieu = Milieu / total1
    Côté_Droit1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] < -12)  ])
    Côté_Droit1 = Côté_Droit1 / total1
    
    Côté_Gauche2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & (df["Y"] < -12)  ])
    Côté_Gauche2 = Côté_Gauche2 / total2
    Milieu2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & (df["Y"] < 12) & (df["Y"] > -12) ])
    Milieu2 = Milieu2 / total2
    Côté_Droit2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & (df["Y"] > 12)  ])
    Côté_Droit2 = Côté_Droit2 / total2
    
    
    
    #Milieu = (df[ ( df["Player1 Team"] == team ) & (df["Time"] < minutes) ]["X"]).values
    #Côté_Droit = (df[ ( df["Player1 Team"] == team ) & (df["Time"] < minutes) ]["Y"]).values
    return (Côté_Gauche1, Milieu, Côté_Droit1), (Côté_Gauche2, Milieu2, Côté_Droit2)
            
            
            
# partie du terrain correspondant à l'équipe adverse découpé en 3 parties ( sur la longueur )
            
def Directions_des_tirs(team1, team2, minutes):
    df = importing_events(team1, team2)
    total1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    total2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    print(total1, total2)
    
    Côté_Gauche1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] > 12) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross")) ])
    Côté_Gauche1 = Côté_Gauche1 / total1
    Milieu = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] < 12) & (df["Y"] > -12) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    Milieu = Milieu / total1
    Côté_Droit1 = len(df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) & (df["X"] > 0) & (df["Y"] < -12) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross")) ])
    Côté_Droit1 = Côté_Droit1 / total1
    
    Côté_Gauche2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & (df["Y"] < -12)  & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    Côté_Gauche2 = Côté_Gauche2 / total2
    Milieu2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & (df["Y"] < 12) & (df["Y"] > -12) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    Milieu2 = Milieu2 / total2
    Côté_Droit2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & (df["Y"] > 12)  & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    Côté_Droit2 = Côté_Droit2 / total2
    
    return (Côté_Gauche1, Milieu, Côté_Droit1), (Côté_Gauche2, Milieu2, Côté_Droit2)
    
    

# partie du terrain correspondant à l'équipe adverse 
    
def Zones_des_tirs(team1, team2, minutes):
    df = importing_events(team1, team2)
    total2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] < 0) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    print(total2)
    SixMètres2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] <= -50) & ( df["Y"] <= 3.5 ) & ( df["Y"] >= -3.5) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    SixMètres2 = ( SixMètres2 / total2 ) * 100
    DixHuitMètres2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] <= -50) & ( df["Y"] <= -3.5 ) & ( df["Y"] >= -14.5) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    DixHuitMètres2 += len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] <= -50) & ( df["Y"] <= 14.5 ) & ( df["Y"] >= 3.5) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    DixHuitMètres2 += len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] >= -50) & (df["X"] <= -40) & ( df["Y"] >= -14.5 ) & ( df["Y"] <= 14.5) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))]) 
    DixHuitMètres2 = ( DixHuitMètres2 / total2 ) * 100
    ExtérieurSurface2 = len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] >= -40) & (df["X"] <= 0) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    ExtérieurSurface2 += len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] <= -40) & ( df["Y"] >= 14.5 ) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))])
    ExtérieurSurface2 += len(df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) & (df["X"] <= -40) & ( df["Y"] <= -14.5 ) & ((df["Event Name"] == "Shot") | (df["Event Name"] == "Direct Free Kick Cross"))]) 
    ExtérieurSurface2 = (ExtérieurSurface2 / total2) * 100
    
    #fig = px.bar(df, x='year', y='pop')
    #fig.show()
    return ( str(SixMètres2) + "%", str(DixHuitMètres2) + "%", str(ExtérieurSurface2) + "%")
    
    
    
# partie du terrain découpé en 3 parties (largeur) : Tiers_gauche, Milieu, Tiers_droit

def Zones_actions(team1, team2, minutes):
    df = importing_events(team1, team2)
    total = len(df[(df["Time"] < minutes)])
    Tiers_gauche = len(df[ ( ( df["Player1 Team"] == team1 ) | ( df["Player1 Team"] == team2 ) ) & (df["Time"] < minutes) & (df["X"] <= -18.4) ])
    Tiers_gauche = (Tiers_gauche / total) * 100
    Milieu = len(df[ ( ( df["Player1 Team"] == team1 ) | ( df["Player1 Team"] == team2 ) ) & (df["Time"] < minutes) & (df["X"] >= -18.4) & (df["X"] <= 18.4) ])
    Milieu = (Milieu / total) * 100
    Tiers_droit = len(df[ ( ( df["Player1 Team"] == team1 ) | ( df["Player1 Team"] == team2 ) ) & (df["Time"] < minutes) & (df["X"] >= 18.4) ])
    Tiers_droit = (Tiers_droit / total) * 100
    
    #fig = go.Figure(
    #data = [go.Bar(x=["Tiers_gauche","Milieu","Tiers_droit"],y=[ Tiers_gauche, Milieu, Tiers_droit])],
    #layout_title_text="Zones d'actions du match:   " + team1 + " vs " + team2
    # )
    #fig.show()
    return ( str(round(Tiers_gauche)) + " %",str(round(Milieu)) + "%", str(round(Tiers_droit)) + "%" )
    
    
    
    
    
def heatmap(team1, team2, minutes):
    
    df = importing_events(team1, team2)
    
    pos_x_team1 = (df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) ]["X"]).values
    pos_y_team1 = (df[ ( df["Player1 Team"] == team1 ) & (df["Time"] < minutes) ]["Y"]).values
    
    pos_x_team2 = (df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) ]["X"]).values
    pos_y_team2 = (df[ ( df["Player1 Team"] == team2 ) & (df["Time"] < minutes) ]["Y"]).values
    

    return pos_x_team1,pos_y_team1, pos_x_team2,pos_y_team2
    
    
