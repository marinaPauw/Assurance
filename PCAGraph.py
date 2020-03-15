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
import datetime
import numpy as np
import UI_MainWindow
import PCA
import FileInput
import re

class PCAGraph(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    global fig
    global annot
    global plotdata

    def __init__(self, parent=None, width=25, height=10, dpi=80):
        UI_MainWindow.Ui_MainWindow.tab.showMaximized()
        loadings = UI_MainWindow.Ui_MainWindow.loadings 
        global fig
        fig = Figure()#figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        aaa = range(0,(len(FileInput.BrowseWindow.currentDataset.index)))
        global ax
        global annot
        ax = fig.add_subplot(1,1,1)
        ############Need to correctly calculate euc distance in N dimension
        for iii in aaa:
            ax.plot(PCA.plotdata[iii, 0],  PCA.plotdata[iii, 1], linestyle="-",linewidth=0, marker='o', markerfacecolor='dimgrey', markeredgecolor='k')
        for element in UI_MainWindow.Ui_MainWindow.outlierlist:
            outlierIndex = np.where([FileInput.BrowseWindow.currentDataset.index==element])
            ax.plot(PCA.plotdata[outlierIndex[1], 0],  PCA.plotdata[outlierIndex[1], 1], linestyle="none",linewidth=0, marker='o', markerfacecolor='r', markeredgecolor='k')
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        FigureCanvas.__init__(self, fig)
        #self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #if FileInput.BrowseWindow.datasetname.find("\\") > 0:
        #    throw,FileInput.BrowseWindow.datasetname = FileInput.BrowseWindow.datasetname.rsplit('\\',1)
        #if FileInput.BrowseWindow.datasetname.find("/") > 0:
        #    throw,FileInput.BrowseWindow.datasetname = FileInput.BrowseWindow.datasetname.rsplit('/',1)
        str1= "PCA of the comprehensive QC metrics"
        fig.suptitle(str1, fontsize=16)
        
        self.compute_initial_figure()
        annot = ax.annotate("", xy=(0,0),color='green')

   
        
    def compute_initial_figure(self):
        pass

    def loadingsToggledOn(self):
        dataset = FileInput.BrowseWindow.currentDataset
        UI_MainWindow.Ui_MainWindow.PCA.LoadingsProgressBar.show()
        UI_MainWindow.Ui_MainWindow.PCA.LoadingsProgressBar.setValue(10)
        minx = min(a for (a,c) in PCA.plotdata)
        miny = min(c for (a,c) in PCA.plotdata)
        maxx = max(a for (a,c) in PCA.plotdata)
        maxy = max(c for (a,c) in PCA.plotdata)
        middlex = minx+((maxx-minx)/2)
        middley = miny+((maxy-miny)/2)
        
        for i in PCA.loadings:
            if(i[0]>maxx):
                i[0]=maxx
            elif(i[0]<minx):
                i[0]=minx
            if(i[1]>maxy):
                i[1]=maxy
            elif(i[1]<miny):
                i[1]=miny
        
        global loadingsAnnot
        loadingsAnnot = ax.quiver(middlex, middley,
           PCA.loadings[0], PCA.loadings[1], angles='xy', scale_units='xy', scale=0.5, width = 0.001,color = "b") 
        loadingsAnnot.set_visible(True)
        # Add labels based on feature names (here just numbers)
        global loadingsTextAnnot
        UI_MainWindow.Ui_MainWindow.PCA.LoadingsProgressBar.setValue(30)
        loadingsTextAnnot = list()
        for i in range(UI_MainWindow.Ui_MainWindow.loadings.shape[0]):
         xvalue = (middlex+UI_MainWindow.Ui_MainWindow.loadings[0,i]*20)
         #If the loadings fall outside the plot, bring it to the max/min

         if(xvalue <min(a for (a,c) in PCA.plotdata)):
             xvalue = min(a for (a,c) in PCA.plotdata)
         elif(xvalue > max(a for (a,c) in PCA.plotdata)):
             xvalue = max(a for (a,c) in PCA.plotdata)
         
         yvalue = (middley + UI_MainWindow.Ui_MainWindow.loadings[1,i]*20)
         #If the loadings fall outside the plot, bring it to the max/min
         
         if ( yvalue>max(c for (a,c) in PCA.plotdata)):
             yvalue = max(c for (a,c) in PCA.plotdata)
         elif (yvalue < min(c for (a,c) in PCA.plotdata)):
             yvalue = min(c for (a,c) in PCA.plotdata)
         
             
         UI_MainWindow.Ui_MainWindow.PCA.LoadingsProgressBar.setValue(60)
         loadingsTextAnnot.append(ax.text(xvalue,yvalue , dataset.columns[i], color = 'b', ha = 'center', va = 'center'))
        for ii in loadingsTextAnnot:
         ii.set_visible(True)

    def loadingsToggledOff():
         UI_MainWindow.Ui_MainWindow.PCA.LoadingsProgressBar.hide() 
         loadingsAnnot.set_visible(False)
         for ii in loadingsTextAnnot:
            ii.set_visible(False)

   
