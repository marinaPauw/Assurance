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
import UI_MainWindow
import re
import pandas as pd
import numpy as np

class RandomForest(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    

    def computeSelectedSamplesFromArea(self, goodOrBad):
        #The format is x1, y1, x2, y2: left, bottom, right, top
        if(goodOrBad == "good"):
            UI_MainWindow.Ui_MainWindow.TrainingSet.goodbtn.setEnabled(False)
        else:
            UI_MainWindow.Ui_MainWindow.TrainingSet.goodbtn.setEnabled(False)

        table = UI_MainWindow.Ui_MainWindow.TrainingSetTable
        area = UI_MainWindow.Ui_MainWindow.predictionArea
        for i in range(0,len(table.index)):
            if(table.iloc[i,1]>area[1]):
                if(table.iloc[i,1]<area[3]):
                    if(i>area[0]):
                        if(i<area[2]):
                            if(goodOrBad == "good"):
                                 if(UI_MainWindow.Ui_MainWindow.badpredictionList.count(table.iloc[i,0])>0):#This item is already part of the badpredictionlist
                                         self.GoodAndBadAreSame()
                                         return
                                 else:
                                         UI_MainWindow.Ui_MainWindow.goodpredictionList.append(table.iloc[i,0])
                            else:
                                 if(UI_MainWindow.Ui_MainWindow.goodpredictionList.count(table.iloc[i,0])>0):#This item is already part of the badpredictionlist
                                         self.GoodAndBadAreSame()
                                         return
                                 else:
                                         UI_MainWindow.Ui_MainWindow.badpredictionList.append(table.iloc[i,0])

        if(len(UI_MainWindow.Ui_MainWindow.goodpredictionList)>0):
                  UI_MainWindow.Ui_MainWindow.goodPredicted=True
                  UI_MainWindow.Ui_MainWindow.TrainingSet.goodbtn.setEnabled(False)
        if(len(UI_MainWindow.Ui_MainWindow.badpredictionList)>0):
                  UI_MainWindow.Ui_MainWindow.badPredicted=True
                  UI_MainWindow.Ui_MainWindow.TrainingSet.badbtn.setEnabled(False)

        if(UI_MainWindow.Ui_MainWindow.goodPredicted):
            if(UI_MainWindow.Ui_MainWindow.badPredicted):
                RandomForest.createguideAndTestSet(RandomForest)
                RandomForest.RunRandomForest(RandomForest)
                QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab,"guide set " ,"Your guideset consisted of the following desired samples: "+ str(UI_MainWindow.Ui_MainWindow.goodpredictionList).strip('[]')+ "and the following suboptimal samples: "+ str(UI_MainWindow.Ui_MainWindow.badpredictionList).strip('[]'))
    
    def GoodAndBadAreSame(self):
        QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab,"guide set " ,"You have selected the same sample for both groups. Please start over.")
        UI_MainWindow.Ui_MainWindow.goodpredictionList.clear()
        UI_MainWindow.Ui_MainWindow.badpredictionList.clear()
        UI_MainWindow.Ui_MainWindow.TrainingSet.badbtn.setEnabled(True)
        UI_MainWindow.Ui_MainWindow.TrainingSet.goodbtn.setEnabled(True)

    def FindIndexes(self):
        RandomForest.goodguidesetIndexes = []
        RandomForest.badguidesetIndexes = []
        for i in UI_MainWindow.Ui_MainWindow.goodpredictionList:
            result = np.where(UI_MainWindow.Ui_MainWindow.metrics == i)
            RandomForest.guideSetDf = RandomForest.guideSetDf.append(UI_MainWindow.Ui_MainWindow.NumericMetrics.iloc[result[0][0]])
            RandomForest.goodguidesetIndexes.append(len(RandomForest.guideSetDf)-1) # Add the goods and bads to lists, then at the end we can allocate them
            if(RandomForest.listToDrop.count(result[0][0])>0):#This item is already part of the badpredictionlist
                self.GoodAndBadAreSame()
            else:
                RandomForest.listToDrop.append(result[0][0])

        for i in UI_MainWindow.Ui_MainWindow.badpredictionList:
            result = np.where(UI_MainWindow.Ui_MainWindow.metrics == i)
            RandomForest.guideSetDf = RandomForest.guideSetDf.append(UI_MainWindow.Ui_MainWindow.NumericMetrics.iloc[result[0][0]])
            RandomForest.badguidesetIndexes.append(len(RandomForest.guideSetDf)-1) # Add the goods and bads to lists, then at the end we can allocate them
            if(RandomForest.listToDrop.count(result[0][0])>0):#This item is already part of the badpredictionlist
                self.GoodAndBadAreSame()
            else:
                RandomForest.listToDrop.append(result[0][0])
                
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
        RandomForest.testSetDf = UI_MainWindow.Ui_MainWindow.NumericMetrics
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
            NMIndex = np.where(UI_MainWindow.Ui_MainWindow.NumericMetrics.iloc[:,0] == RandomForest.testSetDf.iloc[problems[i],0])
            problemSamples.append(UI_MainWindow.Ui_MainWindow.metrics.iloc[ NMIndex[0][0],0])
        print(problems)
        if(len(problems)>0):
            QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab,"Samples identified as suboptimal:", "The following samples have been identified as candidates for outliers/out of control data "+ str(problemSamples).strip('[]'))
        else:
            QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab,"No samples identified as suboptimal:", "For the criteria given, with the given test and guide sets, no samples have been identified as candidates for outliers/out of control data. "+ str(problemSamples).strip('[]'))
        

    def compute_initial_figure(self):
        pass

