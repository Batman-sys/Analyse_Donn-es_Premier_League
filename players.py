#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os

def importing_events():
    path = 'C:\\Users\\PC\\Desktop\\projet_annuel\\EPL 2011-12\\Events'
    # list of file paths in directory called events
    files = os.listdir(path)
    df = pd.DataFrame()
    for f in files:
        #f for the file's path
        '''We used concat to get a dataframe containing 
        all the matches in a single dataframe'''
        df = pd.concat([df,pd.read_csv(path + "\\" +f)])
    return df


# In[2]:


# function that allows us to display the max number of columns
pd.set_option("display.max_columns",100)
#pd.set_option("display.max_rows",100)
df_events = importing_events()


# In[3]:


# full dataframe
df_events.loc[df_events['Event Name']=='Goal']


# In[4]:


#pd.set_option("display.max_rows",1000)
data = pd.DataFrame(df_events['Event Name'])
df_events.loc[pd.isna(df_events['Player2 Name'])==False]['Event Name'].unique()


# In[5]:


#df_events.loc[df_events['xG Score']!=0]


# In[6]:


pd.set_option("display.max_rows",1000)
data.drop_duplicates()


# In[7]:


def importing_players():
    path = 'C:\\Users\\PC\\Desktop\\projet_annuel\\EPL 2011-12\\Players'
    # list of file paths in directory called events
    files = os.listdir(path)
    df = pd.DataFrame()
    for f in files:
        #f for the file's path
        '''We used concat to get a dataframe containing 
        all the matches in a single dataframe'''
        
        df = pd.concat([df,pd.read_csv(path + "\\" +f )])
    return df


# In[8]:


pd.set_option("display.max_columns",68)
df_players = importing_players()


# In[9]:


df_players


# ##### event_season:
# fonction qui prend deux arguments: p (pour joueur) et event (pour événement).
# 
# Elle retourne ensuite la longueur de l'objet filtré d, qui correspond au nombre d'occurrences de l'événement donné pour le joueur donné pendant toue la saison.

# In[10]:


def event_season(p,event):
    d=df_events.loc[(df_events["Player1 Name"]== p)&(df_events['Event Name']==event)]
    return len(d)
event_season('Victor MOSES','Clearance')


# ##### event_match:
# fonction qui prend deux arguments: p (pour joueur) et event (pour événement).
# 
# Elle retourne un dictionnaire d, où chaque clé est le nom d'un match et chaque valeur est le nombre d'occurrences de l'événement donné dans ce match pour le joueur donné.

# In[11]:


def event_match(p,event):
    d={}
    data=df_players.loc[df_players["Player Name"]== p]['Match Name']
    for i in data.unique():
        data2=df_events.loc[(df_events["Player1 Name"]== p)& (df_events['Match Name']==i)&(df_events['Event Name']==event)]
        d[i]=len(data2)
    return d
event_match('Victor MOSES','Block')


# ##### event_match2:
# qui prend trois arguments: p (pour joueur), m (pour nom du match) et event (pour événement).
# 
# Elle retourne ensuite la longueur de l'objet filtré data2, qui correspond au nombre d'occurrences de l'événement donné pour le joueur donné dans le match donné.

# In[12]:


def event_match2(p,m,event):
    data2=df_events.loc[(df_events["Player1 Name"]== p)& (df_events['Match Name']==m)&(df_events['Event Name']==event)]
    return len(data2)
event_match2('Victor MOSES','11.08.13 Wigan Athletic v Norwich City','Pass')


# ##### succ_pass:
# Prend un argument p (pour joueur). 
# 
# Calcul d'abord les passes réussies, c'est-à-dire celles qui n'ont pas conduit à une perte de possession, et stocke le nombre de ces passes réussies dans la variable d.
# 
# Enfin, la fonction calcule le pourcentage de passes réussies en divisant le nombre de passes réussies par le nombre total de passes et retourne cette valeur.

# In[13]:


def succ_pass(p):#% of succesful pass of a player
    data=df_events.loc[(df_events["Player1 Name"]== p)&(df_events['Event Name']=='Pass')]#nbr de passes
    d=data.loc[data['Possession Loss']==False]# nbr de succesful passes
    return len(d)/len(data)
succ_pass('Stephen WARD')


# ##### match_played:
# Prend un argument p (pour joueur).
# 
# Elle retourne le nombre total de matchs dans lesquels le joueur p a joué, en renvoyant simplement la longueur de l'objet filtré data

# In[15]:


def match_played(p):
        data=df_players.loc[df_players["Player Name"]== p]
        return len(data)
match_played("Martin OLSSON")


# ##### decisive_pass :
# Prend un argument p (pour joueur). 
# 
# Elle retourne le nombre total de passes décisives effectuées par le joueur p.

# In[14]:


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


# ###### minutes_per_goal:
# Prend un argument p (pour joueur).
# 
# Elle retourne le dictionnaire s, qui contient les nombre de minutes par but pour chaque match dans lequel le joueur p a marqué un but.
# 
# Si le joueur n'a pas marqué durant le match s[k] est nul
# 
# Sinon s[k] vaut le quotient de minutes jouées par but

# In[103]:


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


# ##### minutes_played :
# Prend un argument p (pour joueur). 
# 
# Retourne un dictionnaire à partir de data, pour associer chaque nom de match à sa durée de jeu correspondante. Le dictionnaire résultant est de la forme {'nom du match': durée de jeu}.

# In[85]:


def minutes_played(p):
    data = df_players.loc[(df_players['Player Name']==p),['Match Name','Minutes Played']]
    return {k:v for k,v in zip(data['Match Name'],data['Minutes Played'])} 
minutes_played("Martin OLSSON")

