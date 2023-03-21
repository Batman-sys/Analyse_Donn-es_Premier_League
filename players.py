import numpy as np
import pandas as pd
import os

def importing_events():
    path = '.\\EPL\\Events'
    # list of file paths in directory called events
    files = os.listdir(path)
    df = pd.DataFrame()
    for f in files:
        #f for the file's path
        '''We used concat to get a dataframe containing 
        all the matches in a single dataframe'''
        df = pd.concat([df,pd.read_csv(path + "\\" +f)])
    return df


def importing_players():
    path = '.\\EPL\\Players'
    # list of file paths in directory called events
    files = os.listdir(path)
    df = pd.DataFrame()
    for f in files:
        #f for the file's path
        '''We used concat to get a dataframe containing 
        all the matches in a single dataframe'''
        
        df = pd.concat([df,pd.read_csv(path + "\\" +f )])
    return df




def event_season(p,event):
    d=df_events.loc[(df_events["Player1 Name"]== p)&(df_events['Event Name']==event)]
    return len(d)



def event_match(p,event):
    d={}
    data=df_players.loc[df_players["Player Name"]== p]['Match Name']
    for i in data.unique():
        data2=df_events.loc[(df_events["Player1 Name"]== p)& (df_events['Match Name']==i)&(df_events['Event Name']==event)]
        d[i]=len(data2)
    return d


def event_match2(p,m,event):
    data2=df_events.loc[(df_events["Player1 Name"]== p)& (df_events['Match Name']==m)&(df_events['Event Name']==event)]
    return len(data2)
event_match2('Victor MOSES','11.08.13 Wigan Athletic v Norwich City','Pass')



def succ_pass(p):#% of succesful pass of a player
    data=df_events.loc[(df_events["Player1 Name"]== p)&(df_events['Event Name']=='Pass')]#nbr de passes
    d=data.loc[data['Possession Loss']==False]# nbr de succesful passes
    return len(d)/len(data)
succ_pass('Stephen WARD')


def match_played(p):
        data=df_players.loc[df_players["Player Name"]== p]
        return len(data)
match_played("Martin OLSSON")



def decisive_pass(p):
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
decisive_pass("Mauro FORMICA")



def minutes_per_goal(p):
    data = event_match(p,'Goal')
    d= minutes_played(p)
    s={}
    for k,v in d.items():
        if data[k]!=0:
            s[k]= v/data[k]
        else:
            s[k]=0
    return s
minutes_per_goal("Mauro FORMICA")


def minutes_played(p):
    data = df_players.loc[(df_players['Player Name']==p),['Match Name','Minutes Played']]
    return {k:v for k,v in zip(data['Match Name'],data['Minutes Played'])} 
minutes_played("Martin OLSSON")

