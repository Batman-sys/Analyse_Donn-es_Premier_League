def eventOfPlayerPerMatch_auxi(p,event,df_players,df_events):
    d={}
    data=df_players.loc[df_players["Player Name"]== p]['Match Name']
    for i in data.unique():
        data2=df_events.loc[(df_events["Player1 Name"]== p)& (df_events['Match Name']==i)&(df_events['Event Name']==event)]
        d[i]=len(data2)
    return d