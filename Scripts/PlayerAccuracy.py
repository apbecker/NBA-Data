

import pandas as pd
import numpy as np
import matplotlib as plt
from bokeh.plotting import figure, curdoc
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource, HoverTool, Div
import argparse
import os,sys
sys.path.append('../DataTools/')

parser = argparse.ArgumentParser(description = 'Script to return a players total accuracy for the 2014-2015 season. By default does all players, but you can specify single player if so desired')

parser.add_argument('--player',help='the name of the player', required = False, nargs=1)

args = parser.parse_args()

#load main data
df = pd.read_csv('../data/shot_logs.csv',header=0)

from CompositeFunctions import *
shotTotals = []
shotAccuracy = []
COLORS = Spectral6

if args.player:
    player = args.player[0]
    acc = getPlayerAccuracy(df,player)

    print 'Accuracy for %s is: %.2f' % (player,100*acc)
else:
    accDF = getPlayerAccuracyDF(df)

#new column data source
source = ColumnDataSource(data=dict(TotalShots=[], accuracy=[],name=[],avg_dist=[]))
def update(p):
    groups = pd.qcut(accDF['AVG_SHOT_DIST'].values, len(COLORS))
    c = [COLORS[xx] for xx in groups.codes]
    source.data=dict(TotalShots=accDF['N_SHOTS'],accuracy=accDF['ACCURACY'],name=accDF['player_name'],avg_dist=accDF['AVG_SHOT_DIST'])
    p.circle(x='TotalShots',y='accuracy',source=source,size=4,color=c)

hover = HoverTool(tooltips=[
    ("Player", "@name"),
])

p = figure(plot_width=600,plot_height=600,title='Accuracy vs. Number of Shots Taken',toolbar_location=None,tools=[hover],background_fill_color='black')
p.xaxis.axis_label = 'Total Shots Taken'
p.yaxis.axis_label = 'Shooting Accuracy'
p.xgrid.grid_line_alpha=0.5
p.ygrid.grid_line_alpha=0.5

update(p)

curdoc().add_root(p)
