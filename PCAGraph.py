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
import Main
import PCA
import MainParser
import OutlierTab
import re
import os
import PDFWriter
import logging
import globalVars

class PCAGraph(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    global fig
    global annot
    global plotdata

    def __init__(self,  now, parent=None):
        globalVars.var.tab.showMaximized()
        loadings = globalVars.var.loadings 
        global fig
        fig = Figure()
        self.axes = fig.add_subplot(111)
        aaa = range(0,(len(globalVars.var.database.currentDataset.index)))
        logging.info(39)
        logging.info(aaa)
        global ax
        global annot
        ax = fig.add_subplot(1,1,1)
        ############Need to correctly calculate euc distance in N dimension
        for iii in aaa:
            ax.plot(PCA.plotdata[iii, 0],  PCA.plotdata[iii, 1], linestyle="-",linewidth=0, marker='o', markerfacecolor='dimgrey', markeredgecolor='k')
        for element in globalVars.var.outlierlist:
            outlierIndex = np.where([globalVars.var.database.currentDataset.index==element])
            ax.plot(PCA.plotdata[outlierIndex[1], 0],  PCA.plotdata[outlierIndex[1], 1], linestyle="none",linewidth=0, marker='o', markerfacecolor='red', markeredgecolor='k')
        for item in PCA.PCA.possOutlierList:
            outlierIndex = np.where([globalVars.var.database.currentDataset.index==item])
            ax.plot(PCA.plotdata[outlierIndex[1], 0],  PCA.plotdata[outlierIndex[1], 1], linestyle="none",linewidth=0, marker='o', markerfacecolor='blue', markeredgecolor='k')
        
            #if forReport:
            #    ax.annotate(element, xy=(PCA.plotdata[outlierIndex[1], 0],  PCA.plotdata[outlierIndex[1], 1]),color='green')
        ax.set_xlabel("PC1   "+ str(round(PCA.PCA.componentVariance[0]*100,4))+ "%")
        logging.info(PCA.PCA.componentVariance)
        ax.set_ylabel("PC2   "+ str(round(PCA.PCA.componentVariance[1]*100,4))+ "%")
        FigureCanvas.__init__(self, fig)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #if MainParser.Parser.datasetname.find("\\") > 0:
        #    throw,MainParser.Parser.datasetname = MainParser.Parser.datasetname.rsplit('\\',1)
        #if MainParser.Parser.datasetname.find("/") > 0:
        #    throw,MainParser.Parser.datasetname = MainParser.Parser.datasetname.rsplit('/',1)
        str1= "PCA of the comprehensive QC metrics"
        fig.suptitle(str1, fontsize=16)
        
        annot = ax.annotate("", xy=(0,0),color='green')
        self.compute_initial_figure()
        
    def compute_initial_figure(self):
        pass

    def loadingsToggledOn(self):
        dataset = globalVars.var.database.currentDataset
        OutlierTab.OutlierTab.LoadingsProgressBar.show()
        OutlierTab.OutlierTab.LoadingsProgressBar.setValue(10)
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
        middlex = [middlex]* len(PCA.loadings[0])
        middley = [middley]* len(PCA.loadings[0])
        global loadingsAnnot
        loadingsAnnot = ax.quiver(middlex, middley,
           PCA.loadings[0], PCA.loadings[1], angles='xy', scale_units='xy', scale=0.5, width = 0.001,color = "purple") 
        loadingsAnnot.set_visible(True)
        # Add labels based on feature names (here just numbers)
        global loadingsTextAnnot
        OutlierTab.OutlierTab.LoadingsProgressBar.setValue(30)
        loadingsTextAnnot = list()
        for i in range(PCA.loadings.shape[0]):
            xvalue = (middlex[0]+PCA.loadings[0,i]*20)
            #If the loadings fall outside the plot, bring it to the max/min

            if(xvalue < ax.get_xlim()[0]):
                xvalue = ax.get_xlim()[0]
            elif(xvalue > ax.get_xlim()[1]):
                xvalue = ax.get_xlim()[1]
         
            yvalue = (middley[0] + PCA.loadings[1,i]*20)
            #If the loadings fall outside the plot, bring it to the max/min
         
            if ( yvalue<ax.get_ylim()[0]):
                yvalue = ax.get_ylim()[0]
            elif (yvalue > ax.get_ylim()[1]):
                yvalue = ax.get_ylim()[1]
         
             
            OutlierTab.OutlierTab.LoadingsProgressBar.setValue(60)
            loadingsTextAnnot.append(ax.text(xvalue,yvalue , dataset.columns[i], color = 'purple', ha = 'center', va = 'center'))
        for ii in loadingsTextAnnot:
            ii.set_visible(True)
        

    def loadingsToggledOff(self):
         OutlierTab.OutlierTab.LoadingsProgressBar.hide() 
         if "loadingsAnnot" in globals():
            loadingsAnnot.set_visible(False)
            for ii in loadingsTextAnnot:
                ii.set_visible(False)
            
    def printForReport(self, now):
        for element in globalVars.var.outlierlist:
            outlierIndex = np.where([globalVars.var.database.currentDataset.index==element])
            ax.annotate(element, xy=(PCA.plotdata[outlierIndex[1], 0],  PCA.plotdata[outlierIndex[1], 1]),color='red')
        for element in PCA.PCA.possOutlierList:
            outlierIndex = np.where([globalVars.var.database.currentDataset.index==element])
            ax.annotate(element, xy=(PCA.plotdata[outlierIndex[1], 0],  PCA.plotdata[outlierIndex[1], 1]),color='blue')
        if "AssuranceReport" not in os.getcwd():
            dirName = str(now) +"_AssuranceReport"
            dirName = dirName.replace(" ", "_")
            dirName = dirName.replace(":", "-")
            PDFWriter.OutputWriter.createDir(self,dirName)
            PDFWriter.OutputWriter.changeDir(self,dirName)
        repeat = len(globalVars.var.database.numericMetrics[0].index)-len(globalVars.var.database.currentDataset.index)
        if repeat ==0:
            PCAGraph.loadingsToggledOff(self)
            fig.savefig("outlierDetection1.png", dpi=500)
            PCAGraph.loadingsToggledOn(self)
            fig.savefig("outlierDetection2.png", dpi=500)
            PCAGraph.loadingsToggledOff(self)
        elif os.path.exists("outlierDetection1.png") and not os.path.exists("outlierDetectionAfterReanlysis1.png"):
            PCAGraph.loadingsToggledOff(self)
            fig.savefig("outlierDetectionAfterReanlysis1.png", dpi=500)
            PCAGraph.loadingsToggledOn(self)
            fig.savefig("outlierDetectionAfterReanlysis2.png", dpi=500)
            PCAGraph.loadingsToggledOff(self)
        
