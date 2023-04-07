import numpy as np
import pandas as pd
import os
import base64
import plotly.graph_objects as go
from assets.auxi import eventOfPlayerPerMatch_auxi
from plotly_football_pitch import make_pitch_figure, PitchDimensions, add_heatmap,SingleColourBackground

def importing_events(t):
    path = ".\\EPL_2011_12\\Team_Events\\" + t + '.csv'
    df = pd.read_csv(path)
    return df


########################################################
def importing_players(player):
    df = pd.read_csv(".\\assets\\player_team.csv")
    path = '.\\EPL_2011_12\\Players'
    s= (df.loc[df['Player Name']==player]['Team']).values
    files = os.listdir(path)
    files = [f for f in files if np.str_(f).__contains__(s[0])]
    df = pd.DataFrame()
    for f in files:
        #f for the file's path
        '''We used concat to get a dataframe containing 
        all the matches in a single dataframe'''
        df = pd.concat([df,pd.read_csv(path + "\\" +f)])
    return df.reset_index()
###############################################
def eventOfPlayerPerSeason(p,event,df_events):
    d=df_events.loc[(df_events["Player1 Name"]== p)&(df_events['Event Name']==event)]
    return len(d)
###############################################
def oppositeeventOfPlayerPerSeason(p,event,df_events):
    d=df_events.loc[(df_events["Player2 Name"]== p)&(df_events['Event Name']==event)]
    return len(d)
###############################################
def eventOfPlayerPerMatch(p,m,event,df_events):
    data2=df_events.loc[(df_events["Player1 Name"]== p)& (df_events['Match Name']==m)&(df_events['Event Name']==event)]
    return len(data2)
############################################
def succPassPerSeason(p,df_events):# number of succesful passes of a player per season
    data=df_events.loc[(df_events["Player1 Name"]== p)&(df_events['Event Name']=='Pass')]#nbr de passes
    d=data.loc[data['Possession Loss']==False]
    return len(d)
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
    team = (df_events[(df_events['Player1 Name'] == p)]['Player1 Team'].values)[0]
    index = df_events[(df_events['Player1 Name']==p)].index
    s = 0
    for i in index:
        if(i<len(df_events)-1):
            k = 1
            while k <= 4 and df_events.iloc[i+k]['Player1 Name'] != p and df_events.iloc[i+k]['Event Name'] != 'Pass' and df_events.iloc[i+k]['Player1 Team'] == team and i+k < len(df_events) - 1:
                f3 = df_events.iloc[i+k]['Event Name']
                k += 1
                if f3 =="Goal":
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
def draw_player_pass(p,m,df_events):   
        d=df_events.loc[(df_events['Player1 Name']==p)&(df_events['Match Name']==m)&(df_events['Event Name']=='Pass')&(df_events['Possession Loss']==False),['X','Y']]
        x= (-1)**df_events.Half*df_events.X
        y = (-1)**df_events.Half*df_events.Y
        x=x+ 52.5
        y =y+34
        l=[]
        fig = go.Figure()
        fig = make_pitch_figure(PitchDimensions(),pitch_background=SingleColourBackground("#81B623"))
        for i in d.index:
            x1 = x.iloc[i]
            y1 = y.iloc[i]
            x2 = x.iloc[i+1]
            y2 = y.iloc[i+1]
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
        fig.update_layout(annotations= l,title="Directions de passes de "+p)

        
        return fig
##########################################
def draw_player_pass_season(p,df_events):
        team = (df_events[(df_events['Player1 Name'] == p)]['Player1 Team'].values)[0]
        index = df_events[(df_events['Player1 Name']==p)].index
        s = []
        for i in index:
            if(i<len(df_events)-1):
                k = 1
                while k <= 4 and df_events.iloc[i+k]['Player1 Name'] != p and df_events.iloc[i+k]['Event Name'] != 'Pass' and df_events.iloc[i+k]['Player1 Team'] == team and i+k < len(df_events) - 1:
                    f3 = df_events.iloc[i+k]['Event Name']
                    k += 1
                    if f3 =="Goal":
                        s.append(i)

        x = (-1)**df_events.Half  * df_events.X
        y =(-1)**df_events.Half  * df_events.Y
        x= x + 52.5
        y = y + 34
        l=[]
        fig = go.Figure()
        fig = make_pitch_figure(PitchDimensions(),pitch_background=SingleColourBackground("#81B623"))
        for i in s:
            x1 = x.iloc[i]
            y1 = y.iloc[i]
            x2 = x.iloc[i+1]
            y2 = y.iloc[i+1]
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
        fig.update_layout(annotations= l,title="Direction des passes décisives de " + p)

        
        return fig
#####################################################
def draw_player_shot(p, df_events):
    shots = ['Shot','Header Shot','Direct Free Kick Shot','Penalty Shot']
    colors = {'Shot':'purple', 'Header Shot':'yellow','Penalty Shot':'gold','Direct Free Kick Shot':'cyan'}
    d=df_events.loc[(df_events['Player1 Name']==p)&(df_events['Event Name'].isin(shots))]
    fig = go.Figure()
    fig = make_pitch_figure(PitchDimensions(),pitch_background=SingleColourBackground("#81B623"))
    ## Add Z variable for xG
    z = d ['xG Score'].tolist()
    data=[i for i in d['Event Name'].values if i in colors.keys()]
    z1 = [20 * i+10 for i in z] # This is to scale the "xG" values for plotting
    groups = d.groupby('Event Name')
    for name, group in groups:
        fig.add_trace(go.Scatter(x=(-1)**group.Half*group.X+52.5, y=(-1)**group.Half*group.Y+34,
                             mode='markers', 
                             marker=dict(size=z1, 
                                         opacity=1, 
                                         color=colors[name]),
                             name=name))
    fig.update_layout(legend=dict(
    orientation="h"),title='Les tirs de '+p)
    return fig
#################################################
def plot_shots(p,df_events):
    shots = df_events.loc[(df_events['Player1 Name']==p) & (df_events['Event Name'].str.contains('Shot'))]['Event Name'].unique()
    fig = go.Figure()
    fig = go.Figure(go.Bar(
    x=shots,
    y=[eventOfPlayerPerSeason(p,i,df_events) for i in shots ]
    ))
    fig.update_layout(title = 'Nombre des tirs réalisées par '+p)
    return fig