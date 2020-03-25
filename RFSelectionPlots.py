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
import math
import statistics
import scipy
from sklearn.preprocessing import StandardScaler, RobustScaler
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import datetime
import numpy as np
import PCA
import FileInput
import re
from matplotlib.widgets  import RectangleSelector



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
            for tick in RFSelectionPlots.ax.get_xticklabels():
                tick.set_rotation(90)
                tick.set_size(8)
            throw, RFSelectionPlots.Ymax =  RFSelectionPlots.ax.get_ylim()
            RFSelectionPlots.ax.legend(loc="upper left", ncol = 1)
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
        print(' Key pressed.')
        if event.key in ['Q', 'q'] and RFSelectionPlots.toggle_selector.RS.active:
            print(' RectangleSelector deactivated.')
            RFSelectionPlots.toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not RFSelectionPlots.toggle_selector.RS.active:
            print(' RectangleSelector activated.')
            RFSelectionPlots.toggle_selector.RS.set_active(True)

    def line_select_callback(eclick, erelease):
        'eclick and erelease are the press and release events'
        x1 = eclick.xdata
        x2 = erelease.xdata
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, 0, x2, RFSelectionPlots.Ymax))
        UI_MainWindow.Ui_MainWindow.predictionArea = [math.ceil(x1), math.ceil(x2)]
        UI_MainWindow.Ui_MainWindow.TrainingSet.goodbtn.setEnabled(True)
        UI_MainWindow.Ui_MainWindow.TrainingSet.badbtn.setEnabled(True)
            