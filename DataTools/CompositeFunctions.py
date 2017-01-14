#helper functions to get new data from the existing data (i.e. composite data) generally returns data frames holding just the high-level info made by each function

import pandas as pd
import numpy as np
from ROOT import TH1F,TGraphAsymmErrors

def getPlayerShotDistHist(df,player):
    shots = df[(df['player_name']==player)].SHOT_DIST.values
    hist = TH1F("hist","hist",50,0,50)
    for shot in shots:
        hist.Fill(shot)
    return hist

def makeShotAccGraph(df,player):
    shotsmade = df[ (df['player_name']==player) & ( df['SHOT_RESULT']=='made') ].SHOT_DIST.values
    shots = df[ (df['player_name']==player)].SHOT_DIST.values
    numhist = TH1F("numhist","Accuracy vs. Shot Distance",25,0,50)
    denhist = TH1F("denhist","Accuracy vs. Shot Distance",25,0,50)
    for shot in shotsmade:
        numhist.Fill(shot)
    for shot in shots:
        denhist.Fill(shot)
    graph = TGraphAsymmErrors(numhist,denhist)
    return graph

def makeShotAccGraphTotal(df):
    shotsmade = df[ ( df['SHOT_RESULT']=='made') ].SHOT_DIST.values
    shots = df.SHOT_DIST.values
    numhist = TH1F("numhist","Accuracy vs. Shot Distance",25,0,50)
    denhist = TH1F("denhist","Accuracy vs. Shot Distance",25,0,50)
    for shot in shotsmade:
        numhist.Fill(shot)
    for shot in shots:
        denhist.Fill(shot)
    graph = TGraphAsymmErrors(numhist,denhist)
    return graph

def getPlayerAccuracy(df,player):
    nmade = len(df[ (df['player_name']==player) & ( df['SHOT_RESULT']=='made') ])
    ntot = len(df[ (df['player_name']==player)])
    accuracy = float(nmade)/ float(ntot)    
    return accuracy


def getListOfPlayers(df):
    names = df['player_name'].unique()
    return names

#def makePlayerTeamDict(df):
#    names = getListOfPlayers(df)
    #now need to loop through original and find via the matchup the common team for more than one matchup for a given player and take this team as the one for which they play
 #   playerDF = df[

def getPlayerAccuracyDF(df):
    namesdf = getListOfPlayers(df)
    acc = []
    dists=[]
    shots=[]
    for name in namesdf:
        acc.append(getPlayerAccuracy(df,name))
        distarr = df[(df['player_name']==name)].SHOT_DIST.values
        dists.append( np.mean(distarr))
        shots.append(len(df[df['player_name']==name]))

    retDF = pd.DataFrame(namesdf,columns=['player_name'])
    retDF['AVG_SHOT_DIST']=dists
    retDF['ACCURACY']=acc
    retDF['N_SHOTS']=shots
#    print retDF.head()
    return retDF


def makeShotArrays(df,player):
    shotsmade = df[ (df['player_name']==player) & ( df['SHOT_RESULT']=='made') ].SHOT_DIST.values
    shots = df[ (df['player_name']==player)].SHOT_DIST.values



    




