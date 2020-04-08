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
import pepXMLReader
import UI_MainWindow
import re
import pandas as pd
import numpy as np
import imblearn
import h2o
from h2o.estimators import H2ORandomForestEstimator

class RandomForest(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    

    def computeTrainingSamplesFromArea(self):
        #The format is x1, y1, x2, y2: left, bottom, right, top

        table = UI_MainWindow.Ui_MainWindow.TrainingSetTable
        area = UI_MainWindow.Ui_MainWindow.predictionArea
        badset = range(area[0], area[1])
        for i in badset:
                UI_MainWindow.Ui_MainWindow.badpredictionList.append(table["Filename"].iloc[i])

        if(len(UI_MainWindow.Ui_MainWindow.badpredictionList)>0):
                  UI_MainWindow.Ui_MainWindow.badPredicted=True
                  UI_MainWindow.Ui_MainWindow.TrainingOrTestSet.badbtn.setEnabled(False)

        # Load in the quality data for training set:
        FileInput.BrowseWindow.__init__(UI_MainWindow.Ui_MainWindow)
        FileInput.BrowseWindow.GetTrainingQualityFiles(UI_MainWindow.Ui_MainWindow, "training")
        if(UI_MainWindow.Ui_MainWindow.badPredicted):
                # Test that Filenames in the quality side and the pepXML's are the same:
                for filename in  UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].index:
                            if filename not in table["Filename"]:
                                QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab,"Error:" , "A sample has been identified for which the raw file name was not found in the pepXML's: "+filename )
    
                
                
                RandomForest.createguideSet(RandomForest)
                
                WithoutClass = np.array(UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].ix[:, UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].columns != 'GoodOrBad'])
                Classy = np.array(UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].ix[:, UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].columns == 'GoodOrBad'])
                minSamples = min(len(Classy[Classy=="G"]), len(Classy[Classy=="B"]))
                #try:
                
                oversample = imblearn.over_sampling.SMOTE(k_neighbors=minSamples-1)
                try:
                    X, Y = oversample.fit_resample(WithoutClass, Classy.ravel())
                except ValueError:
                    QtWidgets.QMessageBox.warning("ValueError", "Perhaps the number of samples of one of the classes was not enough?")
                
                dataToBeSplit = pd.concat([pd.DataFrame(X),pd.DataFrame(Y)],axis = 1)
                # Input parameters that are going to train
                dataToBeSplit.columns = UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].columns
                training_columns = list(UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].ix[:, UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].columns != 'GoodOrBad'].columns)
                # Output parameter train against input parameters
                response_column = 'GoodOrBad'
                # Split data into train and testing
                h2o.init()
                dataToBeSplit = h2o.H2OFrame(dataToBeSplit)
                train, test = dataToBeSplit.split_frame(ratios=[0.6])
                model = H2ORandomForestEstimator(ntrees=50, max_depth=20, nfolds=round(minSamples/2), seed=1234)
                # Train model
                model.train(x=training_columns, y=response_column, training_frame=train)
                # Model performance
                performance = model.model_performance(test_data=test)
                
                #Run the random Forest on the original data:
                rf = model.predict(h2o.H2OFrame(UI_MainWindow.Ui_MainWindow.NumericMetrics[0]))
                results = rf.as_data_frame()
                UI_MainWindow.Ui_MainWindow.printModelResults(self, performance, results)
        
       
                
    def AllocateGoodOrBad(self, table):              

        #Now we have to create a column and add to it whether the sample was in the desired or suboptimal group. 
        #This column will serve as our value to predict
        table["GoodOrBad"] = "G"
        for i in UI_MainWindow.Ui_MainWindow.badpredictionList:
            found = False
            for ii in  range(0, len(table.index)):
                if table.index[ii] == i:
                    table["GoodOrBad"].iloc[ii] = "B"
                    found = True
                    continue
            if not found:
                table["GoodOrBad"].iloc[ii] = 1
        return table

    def createguideSet(self):
        RandomForest.guideSetDf = pd.DataFrame()
        RandomForest.guideSetDf = UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0]
        RandomForest.guideSetDf = RandomForest.AllocateGoodOrBad(self,RandomForest.guideSetDf) 
        
    def  __init__(self, results):
        badset = results["B"]
        global fig
        fig = Figure()#figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        global ax
        global annot
        ax = fig.add_subplot(1,1,1)
        for i in range(0,len(badset.index)):
            if badset[i]<0.5:
                ax.plot(0, badset[i],  marker='o', markerfacecolor='dimgrey', markeredgecolor='k')
            else:
                ax.plot(0, badset[i],  marker='o', markerfacecolor='red', markeredgecolor='r')
        ax.set_ylabel("Proportion of votes")
        FigureCanvas.__init__(self, fig)
        #self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        fig.suptitle("Proportion of trees for each sample that voted the sample into the same category as the 'bad' training data", fontsize=10)
        
        self.compute_initial_figure()
        #annot = ax.annotate("", xy=(0,0),color='green')

    
    
    def compute_initial_figure(self):
        pass

