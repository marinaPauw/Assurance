import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math, sys
import statistics
import scipy
from sklearn import decomposition as sd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, RobustScaler
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets  import RectangleSelector
import matplotlib.pyplot as plt
import numpy as np
import datetime
import UI_MainWindow
import re

class MyIndMetricsCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def line_select_callback(eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        UI_MainWindow.Ui_MainWindow.predictionArea = [x1, y1, x2, y2]
        UI_MainWindow.Ui_MainWindow.spectralCounts.goodbtn.setEnabled(True)
        UI_MainWindow.Ui_MainWindow.spectralCounts.badbtn.setEnabled(True)

    def toggle_selector(event):
        print(' Key pressed.')
        if event.key in ['Q', 'q'] and MyIndMetricsCanvas.toggle_selector.RS.active:
            print(' RectangleSelector deactivated.')
            MyIndMetricsCanvas.toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not MyIndMetricsCanvas.toggle_selector.RS.active:
            print(' RectangleSelector activated.')
            MyIndMetricsCanvas.toggle_selector.RS.set_active(True)

    
    def unique(list1): 
        # intilize a null list 
        unique_list = [] 
      
        # traverse for all elements 
        for x in list1: 
            # check if exists in unique_list or not 
            if x not in unique_list: 
                unique_list.append(x) 

        return unique_list

    def __init__(self, tableContainingRownames, table,element, rectangleSelection,parent=None, width=25, height=5, dpi=100):
        MyIndMetricsCanvas.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = MyIndMetricsCanvas.fig.add_subplot(111)
        sampleSize = range(len(table))
        MyIndMetricsCanvas.ax = MyIndMetricsCanvas.fig.add_subplot(1,1,1)
        plt.grid(color ="ghostwhite")
        manager = plt.get_current_fig_manager()
        manager.resize(*manager.window.maxsize())
        MyIndMetricsCanvas.samplenames = []
        counter = tableContainingRownames.iloc[0,0].count('.') 
        if(counter==1):# .mzML
             for iii in sampleSize:
                        temp,throw = tableContainingRownames.iloc[iii,0].split('.')
                        MyIndMetricsCanvas.samplenames.append(temp)
        elif(counter==2):#For example .wiff.scan
             for iii in sampleSize:
                        temp,throw,throw = tableContainingRownames.iloc[iii,0].split('.')
                        MyIndMetricsCanvas.samplenames.append(temp)
        elif(counter==3):
             for iii in sampleSize:
                        temp,throw,throw = tableContainingRownames.iloc[iii,0].split('.')
                        MyIndMetricsCanvas.samplenames.append(temp)
        else:
            MyIndMetricsCanvas.samplenames = tableContainingRownames.iloc[:,0]

        #Find if there are duplicates in MyIndMetricsCanvas.samplenames (like n a swath/RT file for SwaMe)
        if(len(MyIndMetricsCanvas.samplenames) != len(set(MyIndMetricsCanvas.samplenames))):#duplicates present
            for iii in sampleSize:#If they are numeric values they should be strings
                tableContainingRownames.iloc[iii,1] = str(tableContainingRownames.iloc[iii,1])
            uniqueSamples = MyIndMetricsCanvas.unique(tableContainingRownames.iloc[:,0])
            for item in range(len(uniqueSamples)):
                rowNumList = []
                xAxis = []
                for ii in sampleSize:
                    if(tableContainingRownames.iloc[ii,0]==uniqueSamples[item]):
                        rowNumList.append(ii)
                #if(len(rowNumList)>0):
                MyIndMetricsCanvas.ax.plot(tableContainingRownames.iloc[rowNumList,1],  table.iloc[rowNumList,element], marker='o', label = uniqueSamples[item])   #(np.random.choice(range(256)),np.random.choice(range(256)),np.random.choice(range(256))))
                #else:
                    #MyIndMetricsCanvas.ax.plot(MyIndMetricsCanvas.samplenames,  table.iloc[:,element], linestyle="-",marker='o', markerfacecolor='dimgrey', markeredgecolor='k')
        else:
            MyIndMetricsCanvas.ax.plot(MyIndMetricsCanvas.samplenames,  table.iloc[:,element], linestyle="-",marker='o', markerfacecolor='dimgrey', markeredgecolor='k')
        if(len(MyIndMetricsCanvas.samplenames)<=32):
            MyIndMetricsCanvas.ax.legend(loc="upper left", ncol = 1)
        

        MyIndMetricsCanvas.ax.tick_params(labelrotation = 90, labelsize = 9)
        for tick in MyIndMetricsCanvas.ax.get_xticklabels():
            tick.set_rotation(90)
            tick.set_size(8)
        FigureCanvas.__init__(self, MyIndMetricsCanvas.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # drawtype is 'box' or 'line' or 'none'
        if(rectangleSelection):
            MyIndMetricsCanvas.toggle_selector.RS = RectangleSelector(MyIndMetricsCanvas.ax,  MyIndMetricsCanvas.line_select_callback,
                                           drawtype='box', useblit=True,
                                           button=[1, 3],  # don't use middle button
                                           minspanx=5, minspany=5,
                                           spancoords='pixels',
                                           interactive=True)
            plt.connect('key_press_event', MyIndMetricsCanvas.toggle_selector)

        self.compute_initial_figure()
        if (len(MyIndMetricsCanvas.samplenames)>32):#If there are too many items for the legend to display next to the graph, we make a checkbox for the legend:
            UI_MainWindow.Ui_MainWindow.indMetrics.Checkbox.setVisible(True)
            UI_MainWindow.Ui_MainWindow.indMetrics.Checkboxlabel.setVisible(True)

    def ShowLegend(metric):
        if(len(MyIndMetricsCanvas.samplenames)>32 and len(MyIndMetricsCanvas.samplenames)<=64):
            MyIndMetricsCanvas.ax.legend(loc="upper left", ncol = 2)
        elif(len(MyIndMetricsCanvas.samplenames)>64 and len(MyIndMetricsCanvas.samplenames)<=96):
            MyIndMetricsCanvas.ax.legend(loc="upper left", ncol = 3)
        elif(len(MyIndMetricsCanvas.samplenames)>96 and len(MyIndMetricsCanvas.samplenames)<=128):
            MyIndMetricsCanvas.ax.legend(loc="upper left", ncol = 4)
        else:
            MyIndMetricsCanvas.ax.legend(loc="upper left", ncol = 5)
        MyIndMetricsCanvas.draw(MyIndMetricsCanvas)

    def HideLegend(metric):
        MyIndMetricsCanvas.ax.get_legend().remove()
      
    def compute_initial_figure(self):
        pass    
