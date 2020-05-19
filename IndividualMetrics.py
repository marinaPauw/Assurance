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
import indMetricsTab
from matplotlib.colors import hsv_to_rgb
from cycler import cycler
import os
import numbers
import decimal
from datetime import timedelta

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
        #try:
            
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
            if isinstance(tableContainingRownames.index[0], str):
                MyIndMetricsCanvas.fig, MyIndMetricsCanvas.ax = plt.subplots(constrained_layout=True)
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
            
            
            MyIndMetricsCanvas.fig = Figure(figsize=(width, height), dpi=dpi)
            MyIndMetricsCanvas.fig.subplots_adjust(bottom=0.2)
            sampleSize = range(0,len(table))
            MyIndMetricsCanvas.ax = MyIndMetricsCanvas.fig.add_subplot(1,1,1)
            MyIndMetricsCanvas.samplenames = []
            
            if isinstance(table[element].iloc[0], int) or isinstance(table[element].iloc[0], float)  or isinstance(table[element].iloc[0], np.float64) or isinstance(table[element].iloc[0],np.int64):
                tableContainingRownames = tableContainingRownames.sort_values(element)
                table = table.sort_values(element)
            
            if isinstance( tableContainingRownames.index[0], str):
                if "." in tableContainingRownames.index[0] :
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
            #Sorting out the axes
            MyIndMetricsCanvas.ax.get_yaxis().get_major_formatter().set_scientific(False)
            if type(element) =="int" or type(element) == "float" :
                Ymax = table[element].max()
                if Ymax > 10000:
                    MyIndMetricsCanvas.ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.0e'))
            if element == "runDate":
                MyIndMetricsCanvas.ax.yaxis_date()
                
                
            #Quartiles:
            if "Q1" in locals():
                if Q1 != Q3:
                    Q1Line = MyIndMetricsCanvas.ax.axhline(y=Q1, color='darkslateblue')
                    y = Q1Line.get_ydata()[-1]
                    Q1str = "Q1:" + str(round(Q1,2))
                    MyIndMetricsCanvas.ax.annotate(Q1str, xy=(1,Q1), xytext=(6,0), color=Q1Line.get_color(), 
                    xycoords = MyIndMetricsCanvas.ax.get_yaxis_transform(), textcoords="offset points",
                    size=8, va="center")
                    Q3Line = MyIndMetricsCanvas.ax.axhline(y=Q3, color="darkslateblue")
                    y = Q1Line.get_ydata()[-1]
                    Q3str = "Q3:" + str(round(Q3,2))
                    MyIndMetricsCanvas.ax.annotate(Q3str, xy=(1,Q3), xytext=(6,0), color=Q3Line.get_color(), 
                    xycoords = MyIndMetricsCanvas.ax.get_yaxis_transform(), textcoords="offset points",
                    size=8, va="center")
                    outOverLine = MyIndMetricsCanvas.ax.axhline(y=outlierOver, color='royalblue')
                    y = outOverLine.get_ydata()[-1]
                    outlierOverstr = "Out:" + str(round(outlierOver,2))
                    MyIndMetricsCanvas.ax.annotate(outlierOverstr, xy=(1,outlierOver), xytext=(6,0), color=outOverLine.get_color(), 
                    xycoords = MyIndMetricsCanvas.ax.get_yaxis_transform(), textcoords="offset points",
                    size=8, va="center")
                    outUnderLine = MyIndMetricsCanvas.ax.axhline(y=outlierUnder, color='royalblue')
                    y = outOverLine.get_ydata()[-1]
                    outlierUnderstr = "Out:" + str(round(outlierUnder,2))
                    MyIndMetricsCanvas.ax.annotate(outlierUnderstr, xy=(1,outlierUnder), xytext=(6,0), color=outUnderLine.get_color(), 
                    xycoords = MyIndMetricsCanvas.ax.get_yaxis_transform(), textcoords="offset points",
                    size=8, va="center")
                
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
                        MyIndMetricsCanvas.lines = MyIndMetricsCanvas.ax.plot(tableContainingRownames.iloc[rowNumList,1],  table[element].iloc[rowNumList], marker='o', color = "black",label = uniqueSamples[item])   
                    else:    
                        MyIndMetricsCanvas.lines = MyIndMetricsCanvas.ax.plot(tableContainingRownames.iloc[rowNumList,1],  table[element].iloc[rowNumList], marker='o', color = "black",label = uniqueSamples[item])   
                
            else:
                lines = MyIndMetricsCanvas.ax.plot(MyIndMetricsCanvas.samplenames,  table[element], linestyle="-",marker='o', markerfacecolor = "dimgrey",color = "black")
            if element == "runDate":
                MyIndMetricsCanvas.ax.yaxis_date()
            MyIndMetricsCanvas.ax.grid(True)
            MyIndMetricsCanvas.ax.set_facecolor('gainsboro')
            if UI_MainWindow.Ui_MainWindow.sampleSelected != "":
                if UI_MainWindow.Ui_MainWindow.sampleSelected in tableContainingRownames.index:
                    sIndex = tableContainingRownames.index.tolist().index(UI_MainWindow.Ui_MainWindow.sampleSelected)
                elif type(UI_MainWindow.Ui_MainWindow.sampleSelected) == int:
                    sIndex = int(UI_MainWindow.Ui_MainWindow.sampleSelected)
                
            if not forReport:
                if 'sIndex' in globals() or locals(): #It seems to sometimes be in locals and sometimes in globals
                    if sIndex in MyIndMetricsCanvas.samplenames:
                        MyIndMetricsCanvas.ax.plot(MyIndMetricsCanvas.samplenames[sIndex], table[element].loc[UI_MainWindow.Ui_MainWindow.sampleSelected], linestyle="none",linewidth=0, color = "black", marker='o', markerfacecolor='limegreen', markeredgecolor='darkgreen')
                    
                    elif isinstance(sIndex, int):
                        MyIndMetricsCanvas.ax.plot(MyIndMetricsCanvas.samplenames[sIndex], table[element].iloc[sIndex], linestyle="none",linewidth=0, color = "black", marker='o', markerfacecolor='limegreen', markeredgecolor='darkgreen')
                    line = MyIndMetricsCanvas.ax.lines[0]
                    yVal = line.get_ydata()
                if type(table[element].iloc[0])!= datetime.datetime:
                    xlim = MyIndMetricsCanvas.ax.get_xlim()
                    thisylim = MyIndMetricsCanvas.ax.get_ylim()
                    yaxrange = abs(thisylim[1])-abs(thisylim[0])
                    svalue = (MyIndMetricsCanvas.ax.get_xticks()[sIndex])
                    offsets = [svalue,table[element].iloc[sIndex]+(yaxrange/6)]
                    stringify = "x:" + str(MyIndMetricsCanvas.samplenames[sIndex]) + "\ny:" + str(table[element].iloc[sIndex])
                    MyIndMetricsCanvas.ann = MyIndMetricsCanvas.ax.annotate(stringify, xy=(svalue,table[element].iloc[sIndex]), xytext=(offsets[0], offsets[1]), color="k", 
                        size=10,ha = 'center', va="center", bbox=dict(facecolor='white', edgecolor='blue', pad=3.0))           
                else:
                    xlim = MyIndMetricsCanvas.ax.get_xlim()
                    diffBetweenDpAndMin = table[element].iloc[sIndex] - table[element].min()
                    diffinDays = diffBetweenDpAndMin.days
                    yaxmin = MyIndMetricsCanvas.ax.get_yticks().min()
                    yaxrange = MyIndMetricsCanvas.ax.get_yticks().max() -yaxmin 
                    ylabel = str(table[element].iloc[sIndex]).split(" ")[0]
                    yVal = yaxmin + diffinDays
                    svalue = (MyIndMetricsCanvas.ax.get_xticks()[sIndex])
                    offsets = [svalue,yVal+(yaxrange/6)]
                    stringify = "x:" + str(MyIndMetricsCanvas.samplenames[sIndex]) + "\ny:" + str(ylabel)
                    MyIndMetricsCanvas.ann = MyIndMetricsCanvas.ax.annotate(stringify, xy=(svalue,table[element].iloc[sIndex]), xytext=(offsets[0], offsets[1]), color="k", 
                        size=10,ha = 'center', va="center", bbox=dict(facecolor='white', edgecolor='blue', pad=3.0))           
               
                
            MyIndMetricsCanvas.ax.tick_params(labelrotation = 90, labelsize = 9)
            
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
            image_path = os.path.join(os.getcwd(), element +".pdf")
            MyIndMetricsCanvas.fig.subplots_adjust(bottom=0.5)
            if forReport:
                MyIndMetricsCanvas.fig.savefig(image_path)
            MyIndMetricsCanvas.table = table
            MyIndMetricsCanvas.element = element
            MyIndMetricsCanvas.fig.canvas.mpl_connect('button_press_event',
                                                        lambda event:MyIndMetricsCanvas.onClick(self, event))
            MyIndMetricsCanvas.fig.canvas.mpl_connect('scroll_event',MyIndMetricsCanvas.zoom_fun)
            self.compute_initial_figure()
      
    def compute_initial_figure(self):
        pass    

    def onClick(self,event):
        if event.button == 3:
            if event.inaxes == MyIndMetricsCanvas.ax:
                cont, ind = MyIndMetricsCanvas.fig.contains(event)
                if cont:
                    if hasattr(MyIndMetricsCanvas,"ann"):
                        MyIndMetricsCanvas.ann.remove()
                    if hasattr(MyIndMetricsCanvas,"lines"):
                        MyIndMetricsCanvas.lines.remove()
                    closestx = int(event.xdata)
                    UI_MainWindow.Ui_MainWindow.sampleSelected = MyIndMetricsCanvas.samplenames[closestx]
                    sIndex = int(closestx) 
                    MyIndMetricsCanvas.ax.plot(MyIndMetricsCanvas.samplenames,  MyIndMetricsCanvas.table[MyIndMetricsCanvas.element], linestyle="-",marker='o', markerfacecolor = "dimgrey",color = "black")
                    MyIndMetricsCanvas.ax.plot(MyIndMetricsCanvas.samplenames[sIndex], MyIndMetricsCanvas.table[MyIndMetricsCanvas.element].loc[UI_MainWindow.Ui_MainWindow.sampleSelected], linestyle="none", marker='o', markerfacecolor='limegreen', markeredgecolor='darkgreen')
                    if type(MyIndMetricsCanvas.table[MyIndMetricsCanvas.element].iloc[0])!= datetime.datetime:
                        xlim = MyIndMetricsCanvas.ax.get_xlim()
                        thisylim = MyIndMetricsCanvas.ax.get_ylim()
                        yaxrange = abs(thisylim[1])-abs(thisylim[0])
                        svalue = (MyIndMetricsCanvas.ax.get_xticks()[sIndex])
                        offsets = [svalue,MyIndMetricsCanvas.table[MyIndMetricsCanvas.element].iloc[sIndex]+(yaxrange/6)]
                        stringify = "x:" + str(MyIndMetricsCanvas.samplenames[sIndex]) + "\ny:" + str(MyIndMetricsCanvas.table[MyIndMetricsCanvas.element].iloc[sIndex])
                        MyIndMetricsCanvas.ann = MyIndMetricsCanvas.ax.annotate(stringify, xy=(svalue,MyIndMetricsCanvas.table[MyIndMetricsCanvas.element].iloc[sIndex]), xytext=(offsets[0], offsets[1]), color="k", 
                                size=10,ha = 'center', va="center", bbox=dict(facecolor='white', edgecolor='blue', pad=3.0))           
                    else:
                        xlim = MyIndMetricsCanvas.ax.get_xlim()
                        yvalue = event.ydata
                        ylabel = str(MyIndMetricsCanvas.table[MyIndMetricsCanvas.element].iloc[sIndex]).split(" ")[0]
                        thisylim = MyIndMetricsCanvas.ax.get_ylim()
                        yaxrange = abs(thisylim[1])-abs(thisylim[0])
                        svalue = (MyIndMetricsCanvas.ax.get_xticks()[sIndex])
                        offsets = [svalue,yvalue+(yaxrange/6)]
                        stringify = "x:" + str(MyIndMetricsCanvas.samplenames[sIndex]) + "\ny:" + str(ylabel)
                        MyIndMetricsCanvas.ann = MyIndMetricsCanvas.ax.annotate(stringify, xy=(svalue,yvalue), xytext=(offsets[0], offsets[1]), color="k", 
                            size=10,ha = 'center', va="center", bbox=dict(facecolor='white', edgecolor='blue', pad=3.0))           
                #Have to check if hide tick marks are selected:
                samples = list(MyIndMetricsCanvas.samplenames)
                tableIndex = list(UI_MainWindow.Ui_MainWindow.metrics[0].index)
                if indMetricsTab.IndMetricsTab.tickBox.isChecked():
                        #Find index of selected sample:
                        sIndex = samples.index(UI_MainWindow.Ui_MainWindow.sampleSelected)
                        labels = [""] * len(samples)
                        labels[sIndex] = UI_MainWindow.Ui_MainWindow.sampleSelected
                        MyIndMetricsCanvas.ax.set_xticklabels(labels)
            
                indMetricsTab.IndMetricsTab.sampleBox.setCurrentIndex(tableIndex.index(UI_MainWindow.Ui_MainWindow.sampleSelected)+1)                 
                        
                MyIndMetricsCanvas.fig.canvas.draw()
                
            
        
    def zoom_fun(event):
        # get the current x and y limits
            cur_xlim = MyIndMetricsCanvas.ax.get_xlim()
            cur_ylim = MyIndMetricsCanvas.ax.get_ylim()
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
                print (event.button)
            # set new limits
            MyIndMetricsCanvas.ax.set_xlim([xdata - cur_xrange*scale_factor,
                        xdata + cur_xrange*scale_factor])
            MyIndMetricsCanvas.ax.set_ylim([ydata - cur_yrange*scale_factor,
                        ydata + cur_yrange*scale_factor])
            MyIndMetricsCanvas.fig.canvas.draw()
            
        


