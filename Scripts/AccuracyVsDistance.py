import pandas as pd
import numpy as np
import matplotlib as plt
from bokeh.plotting import figure, curdoc
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource, HoverTool, Div , Select
from bokeh.layouts import row, column
import argparse
import os,sys
from scipy.signal import savgol_filter
#from ROOT import TGraphAsymmErrors,TCanvas,TH1, kGreen, kViolet

sys.path.append('../DataTools/')

from CompositeFunctions import *

#function to get player info
def getPlayerSource(df,player):
    player_df= getPlayerMadeShotsVDistance(df,player)
    player_df['MADE_INT'] = savgol_filter(player_df['MADE_INT'],5,3)
    source = ColumnDataSource(data=dict(accuracy=player_df['MADE_INT'],dist=player_df['SHOT_DIST']))
    return source


#define function to make figure
def makePlot(source,playersource):
    p= figure(plot_width=600,plot_height=600,title='Accuracy vs. Distance from Hoop', tools="", toolbar_location=None,y_range=(0,1),background_fill_color='grey')
    p.line(x='dist',y='accuracy',source=source,line_width=2,line_color='blue',line_alpha=0.7)
    p.line(x='dist',y='accuracy',source=playersource,line_width=2,line_color='red')
    p.xaxis.axis_label='Feet from Basket'
    p.yaxis.axis_label='Shooting Percentage'
    p.xgrid.grid_line_alpha=0.0
    p.ygrid.grid_line_alpha=0.0
    return p


#load main data
df = pd.read_csv('../data/shot_logs.csv',header=0)
acc_df = getMadeShotsVDistance(df)
acc_df['MADE_INT'] = savgol_filter(acc_df['MADE_INT'],5,3)
std_df = getMadeShotsVDistance_std(df)

#define source and player source
source = ColumnDataSource(data=dict(accuracy=acc_df['MADE_INT'],dist=acc_df['SHOT_DIST']))

#make list of players
listOfPlayers = getListOfPlayers(df)

#default player is stephen curry and add selector for player name
player = 'stephen curry'
playersource= getPlayerSource(df,player)
player_select = Select(value=player, title='Player', options=sorted(listOfPlayers))

#define update function
def update_plot(attrname, old, new):
    player = player_select.value
    player_source = getPlayerSource(df,player)
    playersource.data.update(player_source.data)


#make plot
plot = makePlot(source,playersource)
#define behavior on player change
player_select.on_change('value', update_plot)



controls = column(player_select)

curdoc().add_root(row(plot, controls))

#test for steph curry - ROOT VERSION
'''g = makeShotAccGraph(df,'stephen curry')
c = TCanvas()
g.SetTitle("Accuracy vs. Shot Distance; Distance from basket (ft.); Accuracy")
g.Draw("pla")
gtot = makeShotAccGraphTotal(df)
gtot.SetLineColor(2)
gtot.SetFillColor(23)
gtot.Draw("e4 same")
gtot.Draw("c X0")
c.Print('Accuracy_v_Dist_StephCurry.pdf')


gDef = makeShotAccGraphVDefDist(df,'stephen curry')
gDefTot,hnum,hden = makeShotAccGraphVDefDistTotal(df)
gDef.Draw("c X0 a")
gDefTot.SetLineColor(2)
gDefTot.SetFillColor(23)
gDefTot.Draw("e4 same")
gDefTot.Draw("c X0")
c.Print("Accuracy_v_DistanceToClosestDefender_StephCurry.pdf")

hnum.Scale(1 / hnum.Integral())
hden.Scale(1 / hden.Integral())
hnum.SetLineColor(kViolet)
hnum.Draw("")
hden.SetLineColor(kGreen)
hden.Draw("same")
c.SetLogy()
c.Print("Closest_Defender_Dist.pdf")
'''
