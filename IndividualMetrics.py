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
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets  import RectangleSelector
import matplotlib.pyplot as plt
import numpy as np
import datetime
import UI_MainWindow
import re
import Legend
import FileInput
import pylab
from matplotlib.colors import hsv_to_rgb
from cycler import cycler
import os

class MyIndMetricsCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def unique(list1): 
        # intilize a null list 
        unique_list = [] 
      
        # traverse for all elements 
        for x in list1: 
            # check if exists in unique_list or not 
            if x not in unique_list: 
                unique_list.append(x) 

        return unique_list

    def __init__(self, tableContainingRownames, table,element, forReport, parent=None, width=25, height=15, dpi=100):
        try:
            if element == "StartTimeStamp":
                table = UI_MainWindow.Ui_MainWindow.metrics[0]
                tableContainingRownames = UI_MainWindow.Ui_MainWindow.metrics[0]
                if "dates" in UI_MainWindow.Ui_MainWindow.metrics[0]:
                    table["runDate"]= "Default"
                    for x in range(0,len(UI_MainWindow.Ui_MainWindow.metrics[0]["dates"])):
                        table["runDate"].iloc[x] = datetime.datetime.strptime(table["dates"].iloc[x], '%Y-%m-%d')
                    tableContainingRownames["runDate"] = table["runDate"]
                    tableContainingRownames = tableContainingRownames.sort_values("runDate")
                    table = table.sort_values("runDate")
                    element = "runDate"
            MyIndMetricsCanvas.fig = Figure(figsize=(width, height), dpi=dpi)
            if forReport:
                MyIndMetricsCanvas.fig.suptitle(element, fontsize=20)
            else:
                MyIndMetricsCanvas.fig.suptitle(element, fontsize=16)
            #self.axes = MyIndMetricsCanvas.fig.add_subplot(111)
            #MyIndMetricsCanvas.fig.subplots_adjust(bottom=0.5)
            sampleSize = range(0,len(table))
            MyIndMetricsCanvas.ax = MyIndMetricsCanvas.fig.add_subplot(1,1,1)
            if type(table[element][0]) == int or type(table[element][0]) == float or type(table[element][0]) == np.float64:
                tableContainingRownames = tableContainingRownames.sort_values(element)
                table = table.sort_values(element)
            
            MyIndMetricsCanvas.samplenames = []
            if isinstance( tableContainingRownames.index[0], str) and "." in tableContainingRownames.index[0] :
                counter = tableContainingRownames.index[0].count('.') 
                if(counter==1):# .mzML
                    for iii in sampleSize:
                                temp,throw = tableContainingRownames.index[iii].split('.')
                                MyIndMetricsCanvas.samplenames.append(temp)
                elif(counter==2):#For example .wiff.scan
                    for iii in sampleSize:
                                temp,throw,throw = tableContainingRownames.index[iii].split('.')
                                MyIndMetricsCanvas.samplenames.append(temp)
                elif(counter==3):
                    for iii in sampleSize:
                                temp,throw,throw = tableContainingRownames.index[iii].split('.')
                                MyIndMetricsCanvas.samplenames.append(temp)
            else:
                MyIndMetricsCanvas.samplenames = tableContainingRownames.index
            MyIndMetricsCanvas.ax.get_yaxis().get_major_formatter().set_scientific(False)
            if type(element) =="int" or type(element) == "float" :
                Ymax = table[element].max()
                if Ymax > 10000:
                    MyIndMetricsCanvas.ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.0e'))
            #Find if there are duplicates in MyIndMetricsCanvas.samplenames (like n a swath/RT file for SwaMe)
            if(len(MyIndMetricsCanvas.samplenames) != len(set(MyIndMetricsCanvas.samplenames))):#duplicates present
                for iii in sampleSize:#If they are numeric values they should be strings
                    tableContainingRownames.iloc[iii,1] = str(tableContainingRownames.iloc[iii,1])
                uniqueSamples = MyIndMetricsCanvas.unique(tableContainingRownames.iloc[:,0])
                for item in range(len(uniqueSamples)):
                    rowNumList = []
                    xAxis = []
                    for ii in sampleSize:
                        if tableContainingRownames.iloc[ii,0]==uniqueSamples[item]:
                            rowNumList.append(ii)
                    if element == "runDate":
                        lines = MyIndMetricsCanvas.ax.plot(tableContainingRownames.iloc[rowNumList,1],  table[element].iloc[rowNumList], marker='o', color = "black",label = uniqueSamples[item])   
                    else:    
                        lines = MyIndMetricsCanvas.ax.plot(tableContainingRownames.iloc[rowNumList,1],  table[element].iloc[rowNumList], marker='o', color = "black",label = uniqueSamples[item])   
                
            else:
                lines = MyIndMetricsCanvas.ax.plot(MyIndMetricsCanvas.samplenames,  table[element], linestyle="-",marker='o', markerfacecolor = "dimgrey",color = "black")
            MyIndMetricsCanvas.ax.grid(True)
            MyIndMetricsCanvas.ax.set_facecolor('gainsboro')
            sIndex = tableContainingRownames.index.tolist().index(UI_MainWindow.Ui_MainWindow.sampleSelected)
            MyIndMetricsCanvas.ax.plot(MyIndMetricsCanvas.samplenames[sIndex], table[element].loc[UI_MainWindow.Ui_MainWindow.sampleSelected], linestyle="none",linewidth=0, color = "black", marker='o', markerfacecolor='b', markeredgecolor='b')
           
            
            MyIndMetricsCanvas.ax.tick_params(labelrotation = 90, labelsize = 9)
            if element == "runDate":
                #MyIndMetricsCanvas.ax.set_yticklabels(set(table["dates"]))
                MyIndMetricsCanvas.ax.yaxis_date()
            for tick in MyIndMetricsCanvas.ax.get_xticklabels():
                tick.set_rotation(90)
                if forReport:
                    tick.set_size(10)
                else:
                    tick.set_size(8)
            for tick in MyIndMetricsCanvas.ax.get_yticklabels():
                if forReport:
                    tick.set_size(12)
                tick.set_rotation(360)
            FigureCanvas.__init__(self, MyIndMetricsCanvas.fig)
        #  MyIndMetricsCanvas.setParent(parent)

            FigureCanvas.setSizePolicy(self,
                                    QtWidgets.QSizePolicy.Expanding,
                                    QtWidgets.QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)
            self.compute_initial_figure()
            image_path = os.path.join(os.getcwd(), element +".pdf")
            MyIndMetricsCanvas.fig.savefig(image_path)
            
        except:
            if UI_MainWindow.Ui_MainWindow.metrics[0].columns.tolist().index(element) < len(UI_MainWindow.Ui_MainWindow.metrics[0].columns):
                UI_MainWindow.Ui_MainWindow.element = UI_MainWindow.Ui_MainWindow.metrics[0].columns[ UI_MainWindow.Ui_MainWindow.metrics[0].columns.tolist().index(element)+1]
            MyIndMetricsCanvas(tableContainingRownames, table, element, False)

      
    def compute_initial_figure(self):
        pass    





