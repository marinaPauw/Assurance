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
from sklearn.ensemble import RandomForestClassifier
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import FileInput
import DataPreparation
import UI_MainWindow
import re
import pandas as pd
import numpy as np

class RandomForest(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    

    def computeSelectedSamplesFromArea(self):
        #The format is x1, y1, x2, y2: left, bottom, right, top

        table = UI_MainWindow.Ui_MainWindow.TrainingSetTable
        area = UI_MainWindow.Ui_MainWindow.predictionArea
        badset = range(area[0], area[1])
        for i in badset:
                UI_MainWindow.Ui_MainWindow.badpredictionList.append(table["Filename"].iloc[i])

        if(len(UI_MainWindow.Ui_MainWindow.badpredictionList)>0):
                  UI_MainWindow.Ui_MainWindow.badPredicted=True
                  UI_MainWindow.Ui_MainWindow.TrainingSet.badbtn.setEnabled(False)

        # Load in the quality data:
        FileInput.BrowseWindow.__init__(Ui_MainWindow)
        trainingInputFile = FileInput.BrowseWindow.GetInputFile(Ui_MainWindow)
        if trainingInputFile:
            #filepath = FileInput.BrowseWindow.FileCheck(self, inputFile)
            Ui_MainWindow.trainingMetrics = FileInput.BrowseWindow.metricsParsing(self, trainingInputFile)
            #Ui_MainWindow.checkColumnLength(self)
            #Ui_MainWindow.metrics.set_index(Ui_MainWindow.metrics[0].index[0])
            Ui_MainWindow.trainingMetrics[0] = DataPreparation.DataPrep.ExtractNumericColumns(self, Ui_MainWindow.trainingMetrics[0])
            Ui_MainWindow.trainingMetrics[0] = DataPreparation.DataPrep.RemoveLowVarianceColumns(self,Ui_MainWindow.trainingMetrics[0])    

        if(UI_MainWindow.Ui_MainWindow.badPredicted):
                RandomForest.createguideAndTestSet(RandomForest)
                RandomForest.RunRandomForest(RandomForest)
                QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab,"guide set " ,"Your guideset consisted of the following desired samples: "+ str(UI_MainWindow.Ui_MainWindow.goodpredictionList).strip('[]')+ "and the following suboptimal samples: "+ str(UI_MainWindow.Ui_MainWindow.badpredictionList).strip('[]'))
    
   
                
    def AllocateGoodOrBad(self):              

        #Now we have to create a column and add to it whether the sample was in the desired or suboptimal group. 
        #This column will serve as our value to predict
        RandomForest.guideSetDf["GoodOrBad"] = 2
        for i in RandomForest.goodguidesetIndexes:
            RandomForest.guideSetDf.iloc[i,-1] = 1
        for i in RandomForest.badguidesetIndexes:
            RandomForest.guideSetDf.iloc[i,-1] = 0

    def createguideAndTestSet(self):
        RandomForest.guideSetDf = pd.DataFrame()
        RandomForest.testSetDf = DataPreparation.DataPrep.NumericMetrics
        RandomForest.listToDrop = []
        RandomForest.FindIndexes(self)
        RandomForest.testSetDf = RandomForest.testSetDf.drop(RandomForest.listToDrop)
        RandomForest.AllocateGoodOrBad(self)
       
    def RunRandomForest(self):
        model = RandomForestClassifier(n_estimators = 100, max_depth=2)
        model.fit(RandomForest.guideSetDf.loc[:,RandomForest.guideSetDf.columns !="GoodOrBad"], RandomForest.guideSetDf.loc[:,"GoodOrBad"])
        results = model.predict(RandomForest.testSetDf)
        get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]
        problems = get_indexes(0, results)
        problemSamples = []
        for i in range(len(problems)):
            NMIndex = np.where(DataPreparation.DataPrep.NumericMetrics.iloc[:,0] == RandomForest.testSetDf.iloc[problems[i],0])
            problemSamples.append(UI_MainWindow.Ui_MainWindow.metrics.iloc[ NMIndex[0][0],0])
        print(problems)
        if(len(problems)>0):
            QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab,"Samples identified as suboptimal:", "The following samples have been identified as candidates for outliers/out of control data "+ str(problemSamples).strip('[]'))
        else:
            QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab,"No samples identified as suboptimal:", "For the criteria given, with the given test and guide sets, no samples have been identified as candidates for outliers/out of control data. "+ str(problemSamples).strip('[]'))
        

    def compute_initial_figure(self):
        pass

