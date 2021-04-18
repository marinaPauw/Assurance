import sys
import matplotlib as mpl
from matplotlib .backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib .figure import Figure
import matplotlib .pyplot as plt
import Main
import globalVars
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
import statistics
import scipy
from sklearn.preprocessing import StandardScaler, RobustScaler
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import datetime
import numpy as np
import PCA
import MainParser
import re
from matplotlib.widgets  import RectangleSelector
import logging



class RFSelectionPlots(FigureCanvas):
    def __init__( self,table, trainingortest, parent=None):
        try:
            RFSelectionPlots.fig = Figure()
            RFSelectionPlots.ax = RFSelectionPlots.fig.add_subplot(1,1,1)
            RFSelectionPlots.fig.subplots_adjust(bottom=0.2)
            RFSelectionPlots.ax.set_facecolor("gainsboro")
            RFSelectionPlots.ax.grid(True)
            RFSelectionPlots.ax.set_ylim(0, table.loc[:, table.columns != 'Filename'].max().max() + table.loc[:, table.columns != 'Filename'].max().max()/10)
            RFSelectionPlots.ax.set_ylabel("Number of peptides identified")
            table = table.sort_values("Number of spectra identified")
            colour1 = "maroon"
            colour2 = "blue"
            RFSelectionPlots.fig.suptitle("Please draw a rectangle over suboptimal quality data, the unselected samples are considered optimal:", fontsize=10)
            if len(table["Filename"][0]) >20:
                RFSelectionPlots.fig.subplots_adjust(bottom=0.2)
                
            p1 = RFSelectionPlots.ax.plot(table["Filename"], table["Number of distinct peptides"], linestyle = 'None' , marker='o', color = colour1)
            p2 = RFSelectionPlots.ax.plot(table["Filename"], table["Number of spectra identified"], linestyle = 'None', marker = 'o', color = colour2)
            for tick in RFSelectionPlots.ax.get_xticklabels():
                tick.set_rotation(90)
                tick.set_size(8)
            throw, RFSelectionPlots.Ymax =  RFSelectionPlots.ax.get_ylim()
            RFSelectionPlots.ax.legend((p1[0], p2[0]), ("Number of distinct peptides", "Number of spectra identified"),loc='lower right')
            FigureCanvas.__init__(self, RFSelectionPlots.fig)
            RFSelectionPlots.toggle_selector.RS = RectangleSelector( RFSelectionPlots.ax,  RFSelectionPlots.line_select_callback, drawtype='box', useblit=True, button=[1, 3], minspanx=5, minspany=5,spancoords='pixels',
                                            interactive=True)
            plt.connect('key_press_event', RFSelectionPlots.toggle_selector)
            self.compute_initial_figure()
            
            
        except:
           a=10
       
               
    def compute_initial_figure(self):
        pass    

    def toggle_selector(event):
        if event.key in ['Q', 'q'] and RFSelectionPlots.toggle_selector.RS.active:
            logging.info(' RectangleSelector deactivated.')
            RFSelectionPlots.toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not RFSelectionPlots.toggle_selector.RS.active:
            logging.info(' RectangleSelector activated.')
            RFSelectionPlots.toggle_selector.RS.set_active(True)

    def line_select_callback(eclick, erelease):
        'eclick and erelease are the press and release events'
        x1 = eclick.xdata
        x2 = erelease.xdata
        logging.info("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, 0, x2, RFSelectionPlots.Ymax))
        globalVars.var.predictionArea = [math.ceil(x1), math.ceil(x2)]
        globalVars.var.TrainingOrTestSet.badbtn.setEnabled(True)
            