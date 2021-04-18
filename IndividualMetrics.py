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
import Main
import re
import Legend
import MainParser
import Main
import pylab
import indMetricsTab
from matplotlib.colors import hsv_to_rgb
from cycler import cycler
import os
import numbers
import decimal
from datetime import timedelta
import globalVars
import logging

class MyIndMetricsCanvas(FigureCanvas):
    def __init__(self, tableContainingRownames, table,element, forReport, parent=None, width=25, height=15, dpi=100):
                 

            if element == "StartTimeStamp":
                table = globalVars.var.database.metrics[0]
                tableContainingRownames = globalVars.var.database.metrics[0]
                logging.info(globalVars.var.database.metrics[0])
                if "dates" in globalVars.var.database.metrics[0]:
                    table["runDate"]= "Default"
                    for x in range(0,len(globalVars.var.database.metrics[0]["dates"])):
                        table["runDate"].iloc[x] = datetime.datetime.strptime(table["dates"].iloc[x], '%Y-%m-%d')
                    tableContainingRownames["runDate"] = table["runDate"]
                    tableContainingRownames = tableContainingRownames.sort_values("runDate")
                    table = table.sort_values("runDate")
                    element = "runDate"
            if isinstance(tableContainingRownames.index[0], str):
                self.fig, self.ax = plt.subplots(constrained_layout=True)
            else:
               
                tableContainingRownames["sampleNames"] = "sample0"
                for this in range(0,len(tableContainingRownames.index)):
                        tableContainingRownames["sampleNames"][this] = "sample"+str(tableContainingRownames.index[this])
                
                tableContainingRownames.set_index("sampleNames", inplace=True, drop = True)
            
            #Quantiles
            if  [isinstance(table[element].iloc[0], numbers.Number) for x in (0, 0.0, 0j, decimal.Decimal(0))]:
                    if type(table[element].iloc[0]) != datetime.datetime:
                        Q1 = table[element].quantile(0.25)
                        Q3 = table[element].quantile(0.75)
                        outlierOver = Q3 + 1.5*(Q3-Q1)
                        outlierUnder = Q1 - 1.5*(Q3-Q1)
            
            
            self.fig = Figure(figsize=(width, height), dpi=dpi)
            self.fig.subplots_adjust(bottom=0.2)
            sampleSize = range(0,len(table))
            self.ax = self.fig.add_subplot(1,1,1)
            self.samplenames = []
            
            if isinstance(table[element].iloc[0], int) or isinstance(table[element].iloc[0], float)  or isinstance(table[element].iloc[0], np.float64) or isinstance(table[element].iloc[0],np.int64):
                tableContainingRownames = tableContainingRownames.sort_values(element)
                table = table.sort_values(element)
            
            if isinstance( tableContainingRownames.index[0], str):
                if "." in tableContainingRownames.index[0] :
                    counter = tableContainingRownames.index[0].count('.') 
                    if(counter==1):# .mzML
                        for iii in sampleSize:
                                    temp,throw = tableContainingRownames.index[iii].split('.')
                                    self.samplenames.append(temp)
                    elif(counter==2):#For example .wiff.scan
                        for iii in sampleSize:
                                    temp,throw,throw = tableContainingRownames.index[iii].split('.')
                                    self.samplenames.append(temp)
                    elif(counter==3):
                        for iii in sampleSize:
                                    temp,throw,throw = tableContainingRownames.index[iii].split('.')
                                    self.samplenames.append(temp)
                else:
                    self.samplenames = tableContainingRownames.index
            #Sorting out the axes
            self.ax.get_yaxis().get_major_formatter().set_scientific(False)
            if type(element) =="int" or type(element) == "float" :
                Ymax = table[element].max()
                if Ymax > 10000:
                    self.ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.0e'))
            if element == "runDate":
                self.ax.yaxis_date()
                
                
            #Quartiles:
            if "Q1" in locals():
                if Q1 != Q3:
                    Q1Line = self.ax.axhline(y=Q1, color='darkslateblue')
                    y = Q1Line.get_ydata()[-1]
                    Q1str = "Q1:" + str(round(Q1,2))
                    self.ax.annotate(Q1str, xy=(1,Q1), xytext=(6,0), color=Q1Line.get_color(), 
                    xycoords = self.ax.get_yaxis_transform(), textcoords="offset points",
                    size=8, va="center")
                    Q3Line = self.ax.axhline(y=Q3, color="darkslateblue")
                    y = Q1Line.get_ydata()[-1]
                    Q3str = "Q3:" + str(round(Q3,2))
                    self.ax.annotate(Q3str, xy=(1,Q3), xytext=(6,0), color=Q3Line.get_color(), 
                    xycoords = self.ax.get_yaxis_transform(), textcoords="offset points",
                    size=8, va="center")
                    outOverLine = self.ax.axhline(y=outlierOver, color='royalblue')
                    y = outOverLine.get_ydata()[-1]
                    outlierOverstr = "Out:" + str(round(outlierOver,2))
                    self.ax.annotate(outlierOverstr, xy=(1,outlierOver), xytext=(6,0), color=outOverLine.get_color(), 
                    xycoords = self.ax.get_yaxis_transform(), textcoords="offset points",
                    size=8, va="center")
                    outUnderLine = self.ax.axhline(y=outlierUnder, color='royalblue')
                    y = outOverLine.get_ydata()[-1]
                    outlierUnderstr = "Out:" + str(round(outlierUnder,2))
                    self.ax.annotate(outlierUnderstr, xy=(1,outlierUnder), xytext=(6,0), color=outUnderLine.get_color(), 
                    xycoords = self.ax.get_yaxis_transform(), textcoords="offset points",
                    size=8, va="center")
                
            if(len(self.samplenames) != len(set(self.samplenames))):#duplicates present
                for iii in sampleSize:#If they are numeric values they should be strings
                    tableContainingRownames.iloc[iii,1] = str(tableContainingRownames.iloc[iii,1])
                uniqueSamples = self.unique(tableContainingRownames.iloc[:,0])
                for item in range(len(uniqueSamples)):
                    rowNumList = []
                    xAxis = []
                    for ii in sampleSize:
                        if tableContainingRownames.iloc[ii,0]==uniqueSamples[item]:
                            rowNumList.append(ii)
                    if element == "runDate":
                        self.lines = self.ax.plot(tableContainingRownames.iloc[rowNumList,1],  table[element].iloc[rowNumList], marker='o', color = "black",label = uniqueSamples[item])   
                    else:    
                        self.lines = self.ax.plot(tableContainingRownames.iloc[rowNumList,1],  table[element].iloc[rowNumList], marker='o', color = "black",label = uniqueSamples[item])   
                
            else:
                lines = self.ax.plot(self.samplenames,  table[element], linestyle="-",marker='o', markerfacecolor = "dimgrey",color = "black")
            if element == "runDate":
                self.ax.yaxis_date()
            self.ax.grid(True)
            self.ax.set_facecolor('gainsboro')
            if globalVars.var.sampleSelected != "":
                if globalVars.var.sampleSelected in tableContainingRownames.index:
                    sIndex = tableContainingRownames.index.tolist().index(globalVars.var.sampleSelected)
                elif type(globalVars.var.sampleSelected) == int:
                    sIndex = int(globalVars.var.sampleSelected)
                
            if not forReport:
                if 'sIndex' in globals() or locals(): #It seems to sometimes be in locals and sometimes in globals
                    if sIndex in self.samplenames:
                        self.ax.plot(self.samplenames[sIndex], table[element].loc[globalVars.var.sampleSelected], linestyle="none",linewidth=0, color = "black", marker='o', markerfacecolor='limegreen', markeredgecolor='darkgreen')
                    
                    elif isinstance(sIndex, int):
                        self.ax.plot(self.samplenames[sIndex], table[element].iloc[sIndex], linestyle="none",linewidth=0, color = "black", marker='o', markerfacecolor='limegreen', markeredgecolor='darkgreen')
                    line = self.ax.lines[0]
                    yVal = line.get_ydata()
                if type(table[element].iloc[0])!= datetime.datetime:
                    xlim = self.ax.get_xlim()
                    thisylim = self.ax.get_ylim()
                    yaxrange = abs(thisylim[1])-abs(thisylim[0])
                    svalue = (self.ax.get_xticks()[sIndex])
                    offsets = [svalue,table[element].iloc[sIndex]+(yaxrange/6)]
                    stringify = "x:" + str(self.samplenames[sIndex]) + "\ny:" + str(table[element].iloc[sIndex])
                    self.ann = self.ax.annotate(stringify, xy=(svalue,table[element].iloc[sIndex]), xytext=(offsets[0], offsets[1]), color="k", 
                        size=10,ha = 'center', va="center", bbox=dict(facecolor='white', edgecolor='blue', pad=3.0))           
                else:
                    xlim = self.ax.get_xlim()
                    diffBetweenDpAndMin = table[element].iloc[sIndex] - table[element].min()
                    diffinDays = diffBetweenDpAndMin.days
                    yaxmin = self.ax.get_yticks().min()
                    yaxrange = self.ax.get_yticks().max() -yaxmin 
                    ylabel = str(table[element].iloc[sIndex]).split(" ")[0]
                    yVal = yaxmin + diffinDays
                    svalue = (self.ax.get_xticks()[sIndex])
                    offsets = [svalue,yVal+(yaxrange/6)]
                    stringify = "x:" + str(self.samplenames[sIndex]) + "\ny:" + str(ylabel)
                    self.ann = self.ax.annotate(stringify, xy=(svalue,table[element].iloc[sIndex]), xytext=(offsets[0], offsets[1]), color="k", 
                        size=10,ha = 'center', va="center", bbox=dict(facecolor='white', edgecolor='blue', pad=3.0))           
               
                
            self.ax.tick_params(labelrotation = 90, labelsize = 9)
            
            for tick in self.ax.get_xticklabels():
                tick.set_rotation(90)
                if forReport:
                    tick.set_size(10)
                else:
                    tick.set_size(8)
            for tick in self.ax.get_yticklabels():
                if forReport:
                    tick.set_size(12)
                tick.set_rotation(360)
            FigureCanvas.__init__(self, self.fig)
        #  self.setParent(parent)

            FigureCanvas.setSizePolicy(self,
                                    QtWidgets.QSizePolicy.Expanding,
                                    QtWidgets.QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)
            image_path = os.path.join(os.getcwd(), element +".pdf")
            self.fig.subplots_adjust(bottom=0.5)
            if forReport:
                self.ax.set_title(element)
                self.fig.savefig(image_path)
            globalVars.var.indMetricsTab.table = table
            self.element = element
            self.fig.canvas.mpl_connect('button_press_event',
                                                        lambda event:MyIndMetricsCanvas.onClick(self, event))
            self.fig.canvas.mpl_connect('scroll_event',self.zoom_fun)
            self.compute_initial_figure()
      
    def compute_initial_figure(self):
        pass    

    def onClick(self,event):
        if event.button == 3:
            if event.inaxes == self.ax:
                cont, ind = self.fig.contains(event)
                if cont:
                    if hasattr(self,"ann"):
                        self.ann.remove()
                    if hasattr(self,"lines"):
                        self.lines.remove()
                    closestx = int(event.xdata)
                    globalVars.var.sampleSelected = self.samplenames[closestx]
                    sIndex = int(closestx) 
                    self.ax.plot(self.samplenames,  globalVars.var.indMetricsTab.table[self.element], linestyle="-",marker='o', markerfacecolor = "dimgrey",color = "black")
                    self.ax.plot(self.samplenames[sIndex], globalVars.var.indMetricsTab.table[self.element].loc[globalVars.var.sampleSelected], linestyle="none", marker='o', markerfacecolor='limegreen', markeredgecolor='darkgreen')
                    if type(globalVars.var.indMetricsTab.table[self.element].iloc[0])!= datetime.datetime:
                        xlim = self.ax.get_xlim()
                        thisylim = self.ax.get_ylim()
                        yaxrange = abs(thisylim[1])-abs(thisylim[0])
                        svalue = (self.ax.get_xticks()[sIndex])
                        offsets = [svalue,globalVars.var.indMetricsTab.table[self.element].iloc[sIndex]+(yaxrange/6)]
                        stringify = "x:" + str(self.samplenames[sIndex]) + "\ny:" + str(globalVars.var.indMetricsTab.table[self.element].iloc[sIndex])
                        self.ann = self.ax.annotate(stringify, xy=(svalue, globalVars.var.indMetricsTab.table[self.element].iloc[sIndex]), xytext=(offsets[0], offsets[1]), color="k", 
                                size=10,ha = 'center', va="center", bbox=dict(facecolor='white', edgecolor='blue', pad=3.0))           
                    else:
                        xlim = self.ax.get_xlim()
                        yvalue = event.ydata
                        ylabel = str(self.table[self.element].iloc[sIndex]).split(" ")[0]
                        thisylim = self.ax.get_ylim()
                        yaxrange = abs(thisylim[1])-abs(thisylim[0])
                        svalue = (self.ax.get_xticks()[sIndex])
                        offsets = [svalue,yvalue+(yaxrange/6)]
                        stringify = "x:" + str(self.samplenames[sIndex]) + "\ny:" + str(ylabel)
                        self.ann = self.ax.annotate(stringify, xy=(svalue,yvalue), xytext=(offsets[0], offsets[1]), color="k", 
                            size=10,ha = 'center', va="center", bbox=dict(facecolor='white', edgecolor='blue', pad=3.0))           
                #Have to check if hide tick marks are selected:
                samples = list(self.samplenames)
                tableIndex = list(globalVars.var.database.metrics[0].index)
                if globalVars.var.indMetricsTab.tickBox.isChecked():
                        #Find index of selected sample:
                        sIndex = samples.index(globalVars.var.sampleSelected)
                        labels = [""] * len(samples)
                        labels[sIndex] = globalVars.var.sampleSelected
                        self.ax.set_xticklabels(labels)
            
                globalVars.var.indMetricsTab.sampleBox.setCurrentIndex(tableIndex.index(globalVars.var.sampleSelected)+1)                 
                self.fig.canvas.draw()
    
    def unique(list1): 
        # intilize a null list 
        unique_list = [] 
      
        # traverse for all elements 
        for x in list1: 
            # check if exists in unique_list or not 
            if x not in unique_list: 
                unique_list.append(x) 

        return unique_list        
        
    def zoom_fun(event):
        # get the current x and y limits
            cur_xlim = self.ax.get_xlim()
            cur_ylim = self.ax.get_ylim()
            cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
            cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location
            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1/1.5
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = 1.5
            else:
                # deal with something that should never happen
                scale_factor = 1
                logging.info(event.button)
            # set new limits
            self.ax.set_xlim([xdata - cur_xrange*scale_factor,
                        xdata + cur_xrange*scale_factor])
            self.ax.set_ylim([ydata - cur_yrange*scale_factor,
                        ydata + cur_yrange*scale_factor])
            self.fig.canvas.draw()
            
        


