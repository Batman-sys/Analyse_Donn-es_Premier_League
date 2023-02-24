import numpy as np
import pandas as pd
import os
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn as sb
from pathlib import Path
from pandas import *
from matplotlib.patches import Arc



#-------------------------------------
def importing_events(team1, team2):
  path = '.\\EPL_2011_12\\Events\\'
  files = os.listdir(path)
  df = pd.DataFrame()
  #team = "Blackburn Rovers"
  #team2 = "Wolverhampton Wanderers"
  n = '*' + team1 + ' v ' + team2 + ' - Events.csv'
  for f in Path(path).glob(n):
    df = pd.read_csv(f)
  df.Time = df.Time / 60 + (45 * df.Half)
  return df[[
    "Match Name", "Team A", "Team B", "Half", "Time", "Event Name",
    "Player1 Name", "Player1 Team", "Player2 Name", "X", "Y", "Offensiveness",
    "Possession", "Active Team", "Player Transition", "Goal Difference",
    "Possession Number", "Move Number", "xG Score"
  ]]



# "Player Transition", "Goal Difference","Possession Number", "Move Number"

# Tirs Cadrés :
# df["Event Name"] == shot et ( event suivant ) : goal, Goalkeeper Catch, Goalkeeper Save
# (Direct Free Kick Shot et event suivant arret, goal), Goalkeeper Save Catch, Goalkeeper Pick Up
# (Header Shot et event suivant arret, goal ), Goalkeeper Punch ...

# Positions moyenne des Joueurs durant le match



#-------------------------------------
def xG_Score(team1,team2):
    
    df = importing_events(team1, team2)
    
    x1 = df[df["Player1 Team"] == team1][["Time"]].values
    y1 = df[df["Player1 Team"] == team1][["xG Score"]].values
    df1 = df[df["Player1 Team"] == team1]
    
    x2 = df[df["Player1 Team"] == team2][["Time"]].values
    y2 = df[df["Player1 Team"] == team2][["xG Score"]].values
    df2 = df[df["Player1 Team"] == team2]
    
    fig = px.line(df1, x = "Time", y = "xG Score", title=team1)
    fig2 = px.line(df2, x = "Time", y = "xG Score", title=team2)

    fig.show()
    fig2.show()




#-------------------------------------
# à modifier, tout faire en une fonction.
def Nb_Pass_succ(team):    
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




#-------------------------------------
def Offensiveness(team1,team2):
    
    df = importing_events(team1, team2)
    
    x1 = df[df["Player1 Team"] == team1][["Time"]].values
    y1 = df[df["Player1 Team"] == team1][["Offensiveness"]].values
    df1 = df[df["Player1 Team"] == team1]
    
    x2 = df[df["Player1 Team"] == team2][["Time"]].values
    y2 = df[df["Player1 Team"] == team2][["Offensiveness"]].values
    df2 = df[df["Player1 Team"] == team2]
    
    fig = px.line(df1, x = "Time", y = "Offensiveness", title=team1)
    fig2 = px.line(df2, x = "Time", y = "Offensiveness", title=team2)

    fig.show()
    fig2.show()



#-------------------------------------
# à modifier pour afficher la heatmap des 2 équipes simultanément.
def heatmap(team, minutes):
    
    #Create figure
    fig=plt.figure()
    fig.set_size_inches(7, 5)
    ax=fig.add_subplot(1,1,1)
    
    pos_x_team = (df[ ( df["Player1 Team"] == team ) & (df["Time"] < minutes) ]["X"]).values
    pos_y_team = (df[ ( df["Player1 Team"] == team ) & (df["Time"] < minutes) ]["Y"]).values
    
    rec = Rectangle((-60,-40), 120, 80, color = "green", fill = True )
    ax.add_patch(rec)

    sns.kdeplot(pos_x_team,pos_y_team, shade=True, color = "green", n_levels=10)
    
    

    #Pitch Outline & Centre Line
    plt.plot([-56,-56],[-36,36], color="white")
    plt.plot([-56,55],[36,36], color="white")
    plt.plot([55,55],[-36,36], color="white")
    plt.plot([-56,55],[-36,-36], color="white")
    plt.plot([0,0],[-36,36], color="white")


    #Left Penalty Area
    plt.plot([-42,-42],[14,-14],color="white")
    plt.plot([-56,-42],[14,14],color="white")
    plt.plot([-56,-42],[-14,-14],color="white")


    #Right Penalty Area
    plt.plot([41,55],[14,14],color="white")
    plt.plot([41,41],[14,-14],color="white")
    plt.plot([41,55],[-14,-14],color="white")


    #Left 6-yard Box
    plt.plot([-56,-51.5],[7,7],color="white")
    plt.plot([-51.5,-51.5],[-7,7],color="white")
    plt.plot([-56,-51.5],[-7,-7],color="white")


    #Right 6-yard Box
    plt.plot([50,55],[7,7],color="white")
    plt.plot([50,50],[-7,7],color="white")
    plt.plot([50,55],[-7,-7],color="white")


    #Prepare Circles
    centreCircle = plt.Circle((0,0),9.15,color="white",fill=False)
    centreSpot = plt.Circle((0,0),1,color="white")
    #leftPenSpot = plt.Circle((-38,40),0.8,color="black")
    leftPenSpot = plt.Circle((-47,0),0.8,color="white")
    rightPenSpot = plt.Circle((47,0),0.8,color="white")

    #Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)


    #Prepare Arcs
    leftArc = Arc((-48,0),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color="white")
    rightArc = Arc((47,0),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color="white")


    #Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)


    #Tidy Axes
    plt.axis('off')
    plt.title("Carte de chaleur de l'équipe: " + team)


    #Display Pitch
    plt.show()
    
    
    
    
    
#-------------------------------------
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
  
  
  
  
  
  
#-------------------------------------
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
    

    
    
    
#-------------------------------------
#def Directions_des_passes(team1, team2, minutes)

            
#-------------------------------------
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
    return ( str(SixMètres2) + "%", str(DixHuitMètres2) + "%", str(ExtérieurSurface2) + "%")
 


#-------------------------------------
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
    return ( str(SixMètres2) + "%", str(DixHuitMètres2) + "%", str(ExtérieurSurface2) + "%")
    
    

            
#-------------------------------------
def Zones_actions(team1, team2, minutes):
    df = importing_events(team1, team2)
    total = len(df)
    Tiers_gauche = len(df[ ( ( df["Player1 Team"] == team1 ) | ( df["Player1 Team"] == team2 ) ) & (df["Time"] < minutes) & (df["X"] <= -18.4) ])
    Tiers_gauche = (Tiers_gauche / total) * 100
    Milieu = len(df[ ( ( df["Player1 Team"] == team1 ) | ( df["Player1 Team"] == team2 ) ) & (df["Time"] < minutes) & (df["X"] >= -18.4) & (df["X"] <= 18.4) ])
    Milieu = (Milieu / total) * 100
    Tiers_droit = len(df[ ( ( df["Player1 Team"] == team1 ) | ( df["Player1 Team"] == team2 ) ) & (df["Time"] < minutes) & (df["X"] >= 18.4) ])
    Tiers_droit = (Tiers_droit / total) * 100
    return ( str(round(Tiers_gauche)) + " %",str(round(Milieu)) + "%", str(round(Tiers_droit)) + "%" )
    




#-------------------------------------
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



