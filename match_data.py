import numpy as np
import pandas as pd
import os
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
#import seaborn as sb
from pathlib import Path
#from pandas import *
#from matplotlib.patches import Arc


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


def Nb_Pass_succ(team, df):
  a = 0
  for (i, j, k) in zip(df["Event Name"], df["Player1 Team"],
                       df["Player1 Team"][1::]):

    if (i == "Pass") & (j == team) & (k == team):
      a += 1
  return a


def Nb_Pass_miss(team, df):
  a = 0
  for (i, j, k) in zip(df["Event Name"], df["Player1 Team"],
                       df["Player1 Team"][1::]):

    if (i == "Pass") & (j == team) & (k != team):
      a += 1
  return a


def Pass(team, df):
  Nb_Pass = len(df[(df["Event Name"] == "Pass")
                   & (df["Player1 Team"] == team)])
  b = Nb_Pass_succ(team)
  c = Nb_Pass_miss(team)
  return Nb_Pass, b, c


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
