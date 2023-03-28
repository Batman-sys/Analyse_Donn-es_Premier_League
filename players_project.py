import numpy as np
import pandas as pd
import os
import base64
import plotly.graph_objects as go
from auxi import eventOfPlayerPerMatch_auxi
def importing_events(player):
    df = pd.read_csv("C:\\Users\\PC\\Downloads\\Analyse_Donn-es_Premier_League-main\\player_team.csv")
    path = "C:\\Users\\PC\\Desktop\\projet_annuel\\EPL 2011-12\\Events"
    s= (df.loc[df['Player Name']==player]['Team']).astype("string")[0]
    files = os.listdir(path)
    files = [f for f in files if np.str_(f).__contains__(s)]
    df = pd.DataFrame()
    for f in files:
        #f for the file's path
        '''We used concat to get a dataframe containing 
        all the matches in a single dataframe'''
        df = pd.concat([df,pd.read_csv(path + "\\" +f)])
    return df
def importing_players(player):
    df = pd.read_csv("C:\\Users\\PC\\Downloads\\Analyse_Donn-es_Premier_League-main\\player_team.csv")
    path = 'C:\\Users\\PC\\Desktop\\projet_annuel\\EPL 2011-12\\Players'
    s= (df.loc[df['Player Name']==player]['Team']).astype("string")[0]
    files = os.listdir(path)
    files = [f for f in files if np.str_(f).__contains__(s)]
    df = pd.DataFrame()
    for f in files:
        #f for the file's path
        '''We used concat to get a dataframe containing 
        all the matches in a single dataframe'''
        df = pd.concat([df,pd.read_csv(path + "\\" +f)])
    return df
###############################################
def eventOfPlayerPerSeason(p,event,df_events):
    d=df_events.loc[(df_events["Player1 Name"]== p)&(df_events['Event Name']==event)]
    return len(d)
###############################################
def eventOfPlayerPerMatch(p,m,event,df_events):
    data2=df_events.loc[(df_events["Player1 Name"]== p)& (df_events['Match Name']==m)&(df_events['Event Name']==event)]
    return len(data2)
############################################
def Percentage_succPassPerSeason(p,df_events):#% of succesful pass of a player per season
    data=df_events.loc[(df_events["Player1 Name"]== p)&(df_events['Event Name']=='Pass')]#nbr de passes
    d=data.loc[data['Possession Loss']==False]
    return len(d)/len(data)
############################################
def Percentage_succPassPerMatch(p,m,df_events):#% of succesful pass of a player per match
    data=df_events.loc[(df_events["Player1 Name"]== p)&(df_events['Event Name']=='Pass')&(df_events["Match Name"]== m)]#nbr de passes
    d=data.loc[data['Possession Loss']==False]
    return len(d)/len(data)
############################################
def succPassPerMatch(p,m,df_events):#nbr of succesful pass of a player per season
    data=df_events.loc[(df_events["Player1 Name"]== p)&(df_events['Event Name']=='Pass')&(df_events["Match Name"]== m)]#nbr de passes
    d=data.loc[data['Possession Loss']==False]
    return len(d)
############################################
def match_played(p,df_players):
        data=df_players.loc[df_players["Player Name"]== p]
        return len(data)
###########################################
def decisive_pass_season(p,df_events):
    index = df_events[(df_events['Event Name']=='Pass')&(df_events['Player1 Name']==p)].index
    s = 0
    for i in index:
        if(i<len(df_events)-1):
            f1 = df_events.iloc[i]['Player1 Team']
            f2 = df_events.iloc[i+1]['Player1 Team']
            f3 = df_events.iloc[i+1]['Event Name']
            if((f1 == f2) & (f3 =="Goal")):
                s+=1
    return s
###########################################
def decisive_pass_match(p,m,df_events):
    index = df_events[(df_events['Event Name']=='Pass')&(df_events['Player1 Name']==p)&(df_events['Match Name']==m)].index
    s = 0
    for i in index:
        if(i<len(df_events)-1):
            f1 = df_events.iloc[i]['Player1 Team']
            f2 = df_events.iloc[i+1]['Player1 Team']
            f3 = df_events.iloc[i+1]['Event Name']
            if((f1 == f2) & (f3 =="Goal")):
                s+=1
    return s

###########################################
def minutes_per_goal_season(p,df_events,df_players):
    data = eventOfPlayerPerMatch_auxi(p,'Goal',df_players,df_events)
    data2 = df_players.loc[(df_players['Player Name']==p),['Match Name','Minutes Played']]
    d = {k:v for k,v in zip(data2['Match Name'],data2['Minutes Played'])} 
    s={}
    for k,v in d.items():
        if data[k]!=0:
            s[k]= v/data[k]
    return sum(s.values())

###########################################
def minutes_played_season(p,df_players):
    data = df_players.loc[(df_players['Player Name']==p)]['Minutes Played']
    return sum(i for i in data )
###########################################
def minutes_played_match(p,m,df_players):
    data = df_players.loc[(df_players['Player Name']==p)&(df_players['Match Name']==m)]['Minutes Played']
    return sum(i for i in data )
##########################################
def draw_player_pass(p,m):
        title = str(p) + " touch locations"
        df_events = importing_events(p)
        d=df_events.loc[(df_events['Player1 Name']==p)&(df_events['Match Name']==m)&(df_events['Event Name']=='Pass')&(df_events['Possession Loss']==False),['X','Y']]
        h = df_events['Half']
        x=df_events['X']
        y = df_events['Y']
        l=[]
        fig = go.Figure()
        pitch = base64.b64encode(open('C:\\Users\\PC\\Downloads\\Analyse_Donn-es_Premier_League-main\\pitch.jpg', 'rb').read())
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
                        arrowwidth=1.5,
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