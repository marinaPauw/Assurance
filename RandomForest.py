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
    
    global fig
    global badset
    global annot

    def computeTrainingSamplesFromArea(self):
        #The format is x1, y1, x2, y2: left, bottom, right, top

        table = UI_MainWindow.Ui_MainWindow.TrainingSetTable
        area = UI_MainWindow.Ui_MainWindow.predictionArea
        if area[1]>len(table.index)-1:
            area[1] = len(table.index)-1
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
                
                training_columns = list(dataToBeSplit.columns[dataToBeSplit.columns != 'GoodOrBad'])
                # Output parameter train against input parameters
                response_column = 'GoodOrBad'
                # Split data into train and testing
                h2o.init()
                dataToBeSplit = h2o.H2OFrame(dataToBeSplit)
                train, test = dataToBeSplit.split_frame(ratios=[0.6])
                
                train = train.as_data_frame()
                WithoutClassTrain = np.array(train.ix[:, train.columns != 'GoodOrBad'])
                ClassyTrain = np.array(train['GoodOrBad'])
                minTrainSamples = min(len(ClassyTrain[ClassyTrain=="G"]), len(ClassyTrain[ClassyTrain=="B"]))
                
                oversample = imblearn.over_sampling.SMOTE(k_neighbors=minTrainSamples-1)
                #try:
                X, Y = oversample.fit_resample(WithoutClassTrain, ClassyTrain)
                #except ValueError:
                #    QtWidgets.QMessageBox.warning("ValueError", "Perhaps the number of samples of one of the classes was not enough?")
                
                train = pd.concat([pd.DataFrame(X),pd.DataFrame(Y)],axis = 1)
                train.columns = UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].columns
                RandomForest.train = train #For the report writing
                
                test = test.as_data_frame()
                WithoutClassTest = np.array(test.ix[:, test.columns != 'GoodOrBad'])
                ClassyTest = np.array(test['GoodOrBad'])
                minTestSamples = min(len(ClassyTest[ClassyTest=="G"]), len(ClassyTest[ClassyTest=="B"]))
                
                oversample = imblearn.over_sampling.SMOTE(k_neighbors=minTestSamples-1)
                try:
                    X, Y = oversample.fit_resample(WithoutClassTest, ClassyTest)
                except ValueError:
                    QtWidgets.QMessageBox.warning(self,"ValueError", "Perhaps the number of samples of one of the classes was not enough?")
                
                test = pd.concat([pd.DataFrame(X),pd.DataFrame(Y)],axis = 1)
                test.columns = UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].columns
                RandomForest.test = test
                
                model = H2ORandomForestEstimator(ntrees=100, max_depth=20, nfolds=0, seed=1234)
                # Train model
                model.train(x=training_columns, y=response_column, training_frame=h2o.H2OFrame(train))
                # Model performance
                performance = model.model_performance(test_data=h2o.H2OFrame(test))
                RandomForest.performance = performance
                #Run the random Forest on the original data:
                rf = model.predict(h2o.H2OFrame(UI_MainWindow.Ui_MainWindow.NumericMetrics[0]))
                results = rf.as_data_frame()
                results.index = UI_MainWindow.Ui_MainWindow.NumericMetrics[0].index
                UI_MainWindow.Ui_MainWindow.printModelResults(self, performance, results, model)
                
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
                table["GoodOrBad"].iloc[ii] = "Not Found"
        return table

    def createguideSet(self):
        RandomForest.guideSetDf = pd.DataFrame()
        RandomForest.guideSetDf = UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0]
        RandomForest.guideSetDf = RandomForest.AllocateGoodOrBad(self,RandomForest.guideSetDf) 
        
    def  __init__(self, results):
        global badset
        badset = pd.DataFrame()
        badset["B"] = results["B"]
        badset["predict"] = results["predict"]
        badset["X"] = 0
        badset.index = results.index
        # Trying to create a beeswarm plot that is semi impossible in matplotlib:
        badsetround = badset["B"].round(2)
        bsrset = set(badsetround)
        for ii in bsrset:   
            counter = -1    
            for i in range(0, len(badsetround)):
                if badsetround[i] == ii:
                    counter=counter+1
                    if counter>0:
                        if counter % 2 == 0:
                            badset["X"].iloc[i] = 0 + counter * 0.1
                        else:
                            badset["X"].iloc[i] = 0 - counter * 0.1                        
        
        global fig
        fig = Figure()#figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        global ax
        global annot
        ax = fig.add_subplot(1,1,1)
        for i in range(0,len(badset.index)):
            if badset["predict"].iloc[i]=='G':
                ax.plot(0+ badset["X"].iloc[i], badset["B"].iloc[i],  marker='o', markerfacecolor='dimgrey', markeredgecolor='k')
            else:
                ax.plot(0+ badset["X"].iloc[i], badset["B"].iloc[i],  marker='o', markerfacecolor='red', markeredgecolor='r')
        ax.set_ylabel("Proportion of trees that voted each sample as 'bad'")
        FigureCanvas.__init__(self, fig)
        #self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        ax.set_title("Red samples were classified as 'bad' by the model", fontsize=9)
        fig.suptitle("Proportion of trees that voted each sample into the same category as the 'bad' training data", fontsize=10)
        
        self.compute_initial_figure()
        annot = ax.annotate("", xy=(0,0.5),color='green') 
   
    def compute_initial_figure(self):
        pass
    
    def printForReport(self):
        fig.savefig("RFPlot.png", dpi = 500)

