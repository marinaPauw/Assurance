import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
import statistics
import scipy
from sklearn import decomposition as sd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import matplotlib.pyplot as plt
import re
import FileInput
import QuaMeter
import IndividualMetrics
import PCA
import PCAGraph
import DataPreparation
import RandomForest
import numpy as np
import pandas as pd
import SwaMe
import pepXMLReader
import RFSelectionPlots
import FeatureImportancePlot
import PDFWriter
import tempfile
import datetime
import OutlierTab
import indMetricsTab
import UI_MainWindow


class LongitudinalTab(QtWidgets.QTabWidget):

    def printModelResults(self):
        performance= RandomForest.RandomForest.performance
        results = RandomForest.RandomForest.results
        model = RandomForest.RandomForest.best_model
        UI_MainWindow.Ui_MainWindow.removeTab(self, self.sIndex)
        #self.TrainingOrTestSet.removeTab(self, UI_MainWindow.Ui_MainWindow.sIndex)
        self.setCurrentIndex(0)
        
        TrainingOrTestSet = QtWidgets.QTabWidget()
        LongitudinalTab.sIndex = self.addTab(TrainingOrTestSet,"Random Forest Results:")
        TrainingOrTestSet.setStyleSheet("background-color: gainsboro; ")
        
        # -------------------------Metrics Frame Layout ------------------------------------
        TrainingOrTestSet.MetricsFrame = QtWidgets.QFrame(TrainingOrTestSet)
        TrainingOrTestSet.MetricsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        TrainingOrTestSet.MetricsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        TrainingOrTestSet.MetricsFrame.setStyleSheet("background-color: rgb(245,245,245); margin:2px;")

        
        #Labels declare:
        TrainingOrTestSet.MetricsFrame.MainLabel = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.MainLabel.setText("Performance metrics:")
        TrainingOrTestSet.MetricsFrame.MainLabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
        if hasattr(performance, "F1"):
            TrainingOrTestSet.MetricsFrame.F1Label = QtWidgets.QLabel()
            TrainingOrTestSet.MetricsFrame.F1Label.setText("F1:")
            TrainingOrTestSet.MetricsFrame.F1Label.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
            TrainingOrTestSet.MetricsFrame.F1results = QtWidgets.QLabel()
            TrainingOrTestSet.MetricsFrame.F1results.setText(str(round(performance.F1()[0][0],4)))
        else:
            print("No F1!!!")
        if hasattr(performance, "accuracy"):
            TrainingOrTestSet.MetricsFrame.Accuracy = QtWidgets.QLabel()
            TrainingOrTestSet.MetricsFrame.Accuracy.setText("Accuracy:")
            TrainingOrTestSet.MetricsFrame.Accuracy.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
            TrainingOrTestSet.MetricsFrame.AccuracyResults = QtWidgets.QLabel()
            TrainingOrTestSet.MetricsFrame.AccuracyResults.setText(str(round(performance.accuracy()[0][0],4)))        
        if hasattr(performance, "mcc"):
            TrainingOrTestSet.MetricsFrame.MCCLabel = QtWidgets.QLabel()
            TrainingOrTestSet.MetricsFrame.MCCLabel.setText("MCC:")
            TrainingOrTestSet.MetricsFrame.MCCLabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
            TrainingOrTestSet.MetricsFrame.MCCresults = QtWidgets.QLabel()
            TrainingOrTestSet.MetricsFrame.MCCresults.setText(str(round(performance.mcc()[0][0],4)))        
        if hasattr(performance, "logloss"):
            TrainingOrTestSet.MetricsFrame.LLLabel = QtWidgets.QLabel()
            TrainingOrTestSet.MetricsFrame.LLLabel.setText("logloss:")
            TrainingOrTestSet.MetricsFrame.LLLabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
            TrainingOrTestSet.MetricsFrame.LLresults = QtWidgets.QLabel()
            TrainingOrTestSet.MetricsFrame.LLresults.setText(str(round(performance._metric_json["logloss"],4)))       
           
        #Layout within Frame:
        pvbox = QtWidgets.QVBoxLayout(TrainingOrTestSet.MetricsFrame)
        phbox1 = QtWidgets.QHBoxLayout(TrainingOrTestSet.MetricsFrame)
        phbox1.addWidget(TrainingOrTestSet.MetricsFrame.MainLabel)
        pvbox.addLayout(phbox1)
        phbox2 = QtWidgets.QHBoxLayout(TrainingOrTestSet.MetricsFrame)
        pgrid = QtWidgets.QGridLayout(TrainingOrTestSet.MetricsFrame)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.MainLabel,0,0,1,8)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.F1Label,1,0,1,1)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.F1results,1,1,1,1)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.Accuracy,1,3,1,1)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.AccuracyResults,1,4,1,1)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.MCCLabel,1,6,1,1)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.MCCresults,1,7,1,1)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.LLLabel,1,9,1,1)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.LLresults,1,10,1,1)
        try:
            if TrainingOrTestSet.MetricsFrame.AccuracyResults <0.5:
                accuracyWarning = QtWidgets.QLabel()
                accuracyWarning.setText("The low accuracy of this model may indicate that conclusions should be approached with caution.")
                pgrid.addWidget(accuracyWarning,2,3,1,1)
        except:
            print("Could not evaluate Accuracy/ add label.")
        phbox2.addLayout(pgrid)
        pvbox.addLayout(phbox2)
    
        # -------------------------Results Layout ------------------------------------
        #Frame declare:
         
        TrainingOrTestSet.ResultsFrame = QtWidgets.QFrame(TrainingOrTestSet)
        TrainingOrTestSet.ResultsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        TrainingOrTestSet.ResultsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        TrainingOrTestSet.ResultsFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")

        #Labels declare:
        TrainingOrTestSet.ResultsFrame.MainLabel = QtWidgets.QLabel()
        TrainingOrTestSet.ResultsFrame.MainLabel.setText("Random Forest results:")
        TrainingOrTestSet.ResultsFrame.MainLabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)        
        TrainingOrTestSet.ResultsFrame.predictedLabel = QtWidgets.QLabel()
        TrainingOrTestSet.ResultsFrame.predictedLabel.setText("The following samples were predicted by Random Forest to resemble the group labelled 'bad' quality:")
        TrainingOrTestSet.ResultsFrame.predictedLabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)        

        #Bad samples grid:
        badsamplesgrid = QtWidgets.QGridLayout()
        badlist = results[results['predict']=='B'].index
        currentrow = 0
        currentcolumn = 0
        for i in range(0,len(badlist)):
            label = QtWidgets.QLabel()
            label.setText(badlist[i])
            label.setMinimumHeight(30)
            if len(badlist[i])>20:
                 badsamplesgrid.addWidget(label,currentrow,0)
                 currentrow = currentrow+1
                 currentcolumn = 0
            else:
                if currentcolumn>4:
                    currentrow = currentrow +1
                    currentcolumn = 0
                badsamplesgrid.addWidget(label,currentrow,currentcolumn)
                currentcolumn = currentcolumn+1
            
        UI_MainWindow.Ui_MainWindow.badlist = badlist
                        
        #Layout within Frame:
        rvbox = QtWidgets.QVBoxLayout(TrainingOrTestSet.ResultsFrame)
        rhbox1 = QtWidgets.QHBoxLayout(TrainingOrTestSet.ResultsFrame)
        rhbox1.addWidget(TrainingOrTestSet.ResultsFrame.MainLabel)
        rvbox.addLayout(rhbox1) 
        rhbox15 = QtWidgets.QHBoxLayout(TrainingOrTestSet.ResultsFrame)
        rhbox15.addWidget(TrainingOrTestSet.ResultsFrame.predictedLabel)
        rvbox.addLayout(rhbox15)       
        rhbox2 = QtWidgets.QHBoxLayout(TrainingOrTestSet.ResultsFrame)
        rhbox2.addLayout(badsamplesgrid)
        rvbox.addLayout(rhbox2)

               
        #-------------------------plots---------------------------------
        TrainingOrTestSet.PlotFrame = QtWidgets.QFrame(TrainingOrTestSet)
        TrainingOrTestSet.PlotFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        TrainingOrTestSet.PlotFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        TrainingOrTestSet.PlotFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")


        # plot        
        RFPlot = RandomForest.RandomForest()
        FeaturePlot = FeatureImportancePlot.FeaturePlot(model)
        fgrid = QtWidgets.QGridLayout(TrainingOrTestSet.PlotFrame)
        fgrid.addWidget(FeaturePlot,0,0,1,1)          
        fgrid.addWidget(RFPlot,1,0,1,1)
        
        # -------------------------Complete Tab Layout ------------------------------------
        # Tab Layout
        scroll = QtWidgets.QScrollArea()
        placementwidget = QtWidgets.QWidget()
        placementwidget.setMinimumWidth(750)
        placementwidget.setMinimumHeight(2000)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(TrainingOrTestSet.MetricsFrame,0,0,1,1)   
        grid.addWidget(TrainingOrTestSet.ResultsFrame,1,0,2,1) 
        grid.addWidget(TrainingOrTestSet.PlotFrame,3,0,9,1)
        placementwidget.setLayout(grid)
        scroll.setWidget(placementwidget)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        scroll.setWidgetResizable(True)

        vLayout = QtWidgets.QVBoxLayout(TrainingOrTestSet)
        vLayout.addWidget(scroll)
     
        RandomForest.fig.canvas.mpl_connect("motion_notify_event", LongitudinalTab.RFonhover)                        
        self.setCurrentIndex(UI_MainWindow.Ui_MainWindow.sIndex)
        
    
    def RFonhover(event):
        vis = RandomForest.annot.get_visible()
        if event.inaxes == RandomForest.ax:
            cont, ind = RandomForest.fig.contains(event)
            if cont:
                LongitudinalTab.RFupdate_annot(event)
                RandomForest.annot.set_visible(True)
                RandomForest.fig.canvas.draw_idle()
                return
        if vis:
            RandomForest.annot.set_visible(False)
            RandomForest.fig.canvas.draw_idle()
            
    def RFupdate_annot(event):
        closestyIndex = np.abs(RandomForest.badset["B"] - event.ydata).argmin()
        closesty = RandomForest.badset["B"].loc[closestyIndex]
        badsetclosey = RandomForest.badset[RandomForest.badset['B']==closesty]
        closestxIndex = np.abs(badsetclosey['X'] - event.xdata).argmin()        
        closestx = RandomForest.badset["X"].loc[closestxIndex]
        RandomForest.annot.xyann = (closestx , closesty)
        RandomForest.annot.set_text(closestxIndex)
        