import pandas as pd
import numpy as np
import matplotlib as plt
#from bokeh.plotting import figure, curdoc
#from bokeh.palettes import Spectral6
#from bokeh.models import ColumnDataSource, HoverTool, Div
import argparse
import os,sys
from ROOT import TGraphAsymmErrors,TCanvas,TH1

sys.path.append('../DataTools/')

#load main data
df = pd.read_csv('../data/shot_logs.csv',header=0)
from CompositeFunctions import *
shotTotals = []

#test for steph curry
g = makeShotAccGraph(df,'stephen curry')
c = TCanvas()
g.Draw("apl")
gtot = makeShotAccGraphTotal(df)
gtot.SetLineColor(2)
gtot.SetFillColor(23)
gtot.Draw(" e4 same")
gcopy = (TGraph)
c.Print('Accuracy_v_Dist_StephCurry.pdf')
