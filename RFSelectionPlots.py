import sys
import matplotlib as mpl
from matplotlib .backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib .figure import Figure
import matplotlib .pyplot as plt
import UI_MainWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math, sys
import statistics
import scipy
from sklearn.preprocessing import StandardScaler, RobustScaler
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import datetime
import numpy as np
import PCA
import FileInput
import re



class RFSelectionPlots(FigureCanvas):
    def __init__( self,table, parent=None, width=25, height=8, dpi=100):
        try:
            if "Dates" in table.columns:
                table.sort_values("Dates")
            RFSelectionPlots.fig = Figure(figsize=(width, height), dpi=dpi)
            RFSelectionPlots.ax = RFSelectionPlots.fig.add_subplot(1,1,1)
            RFSelectionPlots.fig.subplots_adjust(bottom=0.5)
            plt.grid(color ="ghostwhite")
            RFSelectionPlots.ax.bar(table["Filename"], table["scoreLow"])
            RFSelectionPlots.ax.bar(table["Filename"], table["scoreMed"], bottom=table["scoreLow"])
            RFSelectionPlots.ax.bar(table["Filename"], table["scoreHigh"], bottom=table["scoreLow"]+table["scoreMed"])
            FigureCanvas.__init__(self, RFSelectionPlots.fig)
            self.compute_initial_figure()
            
            
        except:
           a=10
       
               
    def compute_initial_figure(self):
        pass    
            