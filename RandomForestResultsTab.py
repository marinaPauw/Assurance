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

    def printModelResults(self, performance, results, model):
        UI_MainWindow.Ui_MainWindow.removeTab(self, self.sIndex)
        UI_MainWindow.Ui_MainWindow.setCurrentIndex(self,0)
        
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
        TrainingOrTestSet.MetricsFrame.MainLabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.MainLabel.setText("Performance metrics:")
        TrainingOrTestSet.MetricsFrame.MainLabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
        TrainingOrTestSet.MetricsFrame.F1Label = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.F1Label.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.F1Label.setText("F1:")
        TrainingOrTestSet.MetricsFrame.F1Label.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
        TrainingOrTestSet.MetricsFrame.F1results = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.F1results.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.F1results.setText(str(round(performance.F1()[0][1],4)))
        TrainingOrTestSet.MetricsFrame.Accuracy = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.Accuracy.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.Accuracy.setText("RMSE:")
        TrainingOrTestSet.MetricsFrame.Accuracy.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
        TrainingOrTestSet.MetricsFrame.AccuracyResults = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.AccuracyResults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.AccuracyResults.setText(str(round(performance.accuracy()[0][1],4)))        
        TrainingOrTestSet.MetricsFrame.MCCLabel = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.MCCLabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.MCCLabel.setText("MCC:")
        TrainingOrTestSet.MetricsFrame.MCCLabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
        TrainingOrTestSet.MetricsFrame.MCCresults = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.MCCresults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.MCCresults.setText(str(round(performance.mcc()[0][1],4)))        
        TrainingOrTestSet.MetricsFrame.LLLabel = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.LLLabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.LLLabel.setText("logloss:")
        TrainingOrTestSet.MetricsFrame.LLLabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
        TrainingOrTestSet.MetricsFrame.LLresults = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.LLresults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.LLresults.setText(str(round(performance._metric_json["logloss"],4)))       
        TrainingOrTestSet.MetricsFrame.AUCLabel = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.AUCLabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.AUCLabel.setText("AUC:")
        TrainingOrTestSet.MetricsFrame.AUCLabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
        TrainingOrTestSet.MetricsFrame.AUCresults = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.AUCresults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.AUCresults.setText(str(round(performance._metric_json["AUC"],4)))            
        TrainingOrTestSet.MetricsFrame.GINILabel = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.GINILabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.GINILabel.setText("GINI:")
        TrainingOrTestSet.MetricsFrame.GINILabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
        TrainingOrTestSet.MetricsFrame.GINIresults = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.GINIresults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.GINIresults.setText(str(round(performance._metric_json["Gini"],4)))     
        TrainingOrTestSet.MetricsFrame.MPCELabel = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.MPCELabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.MPCELabel.setText("Mean per class error:")
        TrainingOrTestSet.MetricsFrame.MPCELabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
        TrainingOrTestSet.MetricsFrame.MPCEresults = QtWidgets.QLabel()
        TrainingOrTestSet.MetricsFrame.MPCEresults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.MetricsFrame.MPCEresults.setText(str(round(performance._metric_json["mean_per_class_error"],4)))    
 
                
        #Layout within Frame:
        pvbox = QtWidgets.QVBoxLayout(TrainingOrTestSet.MetricsFrame)
        phbox1 = QtWidgets.QHBoxLayout(TrainingOrTestSet.MetricsFrame)
        phbox1.addWidget(TrainingOrTestSet.MetricsFrame.MainLabel)
        pvbox.addLayout(phbox1)
        phbox2 = QtWidgets.QHBoxLayout(TrainingOrTestSet.MetricsFrame)
        phbox2.addStretch()
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
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.AUCLabel,1,12,1,1)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.AUCresults,1,13,1,1)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.GINILabel,1,15,1,1)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.GINIresults,1,16,1,1)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.MPCELabel,2,0,2,2)
        pgrid.addWidget(TrainingOrTestSet.MetricsFrame.MPCEresults,2,2,2,1)
        phbox2.addLayout(pgrid)
        phbox2.addStretch()
        pvbox.addLayout(phbox2)
    
        # -------------------------Results Layout ------------------------------------
        #Frame declare:
         
        TrainingOrTestSet.ResultsFrame = QtWidgets.QFrame(TrainingOrTestSet)
        TrainingOrTestSet.ResultsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        TrainingOrTestSet.ResultsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        TrainingOrTestSet.ResultsFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")

        #Labels declare:
        TrainingOrTestSet.ResultsFrame.MainLabel = QtWidgets.QLabel()
        TrainingOrTestSet.ResultsFrame.MainLabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.ResultsFrame.MainLabel.setText("Random Forest results:")
        TrainingOrTestSet.ResultsFrame.MainLabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)        
        TrainingOrTestSet.ResultsFrame.predictedLabel = QtWidgets.QLabel()
        TrainingOrTestSet.ResultsFrame.predictedLabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        TrainingOrTestSet.ResultsFrame.predictedLabel.setText("The following samples were predicted by Random Forest to resemble the group labelled 'bad' quality:")
        TrainingOrTestSet.ResultsFrame.predictedLabel.setFont(UI_MainWindow.Ui_MainWindow.boldfont)        

        #Bad samples grid:
        badsamplesgrid = QtWidgets.QGridLayout()
        badsamplesgrid.addWidget(TrainingOrTestSet.ResultsFrame.predictedLabel,0,0)
        badlist = results[results['predict']=='B'].index
        currentrow = 0
        currentcolumn = 0
        for i in range(0,len(badlist)):
            label = QtWidgets.QLabel()
            label.setText(badlist[i])
            if len(badlist[i])>20:
                 badsamplesgrid.addWidget(label,currentrow,0)
                 currentrow = currentrow+1
                 currentcolumn = 0
            else:
                if currentcolumn>4:
                    currentrow = currentrow +1
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
        RFPlot = RandomForest.RandomForest(results)
        FeaturePlot = FeatureImportancePlot.FeaturePlot(model)
        fgrid = QtWidgets.QGridLayout(TrainingOrTestSet.PlotFrame)
        fgrid.addWidget(FeaturePlot,0,0,1,1)          
        fgrid.addWidget(RFPlot,1,0,1,1)
        
        # -------------------------Complete Tab Layout ------------------------------------
        # Tab Layout
        scroll = QtWidgets.QScrollArea()
        placementwidget = QtWidgets.QWidget()
        placementwidget.setFixedWidth(750)
        placementwidget.setFixedHeight(2000)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(TrainingOrTestSet.MetricsFrame,0,0,1,1)   
        grid.addWidget(TrainingOrTestSet.ResultsFrame,1,0,2,1) 
        grid.addWidget(TrainingOrTestSet.PlotFrame,3,0,9,1)
        placementwidget.setLayout(grid)
        scroll.setWidget(placementwidget)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #scroll.setMinimumHeight(2000)

        scroll.setWidgetResizable(True)

        vLayout = QtWidgets.QVBoxLayout(TrainingOrTestSet)
        vLayout.addWidget(scroll)
        #vLayout.setGeometry()
     
        RandomForest.fig.canvas.mpl_connect("motion_notify_event", UI_MainWindow.Ui_MainWindow.RFonhover)                        
        self.setCurrentIndex(UI_MainWindow.Ui_MainWindow.sIndex)
        