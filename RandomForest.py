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
import RandomForestResultsTab
import re
import pandas as pd
import numpy as np
import imblearn
import h2o
from h2o.estimators import H2ORandomForestEstimator
from h2o.grid.grid_search import H2OGridSearch
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem

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
        FileInput.BrowseWindow.GetTrainingQualityFiles(UI_MainWindow.Ui_MainWindow)
        #FileInput.BrowseWindow.checkTrainingQualityColumns(self, UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics)
        
        if type(UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].index[0]) != str:
            UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].index = UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0]["Filename"]
                
        
        if hasattr(UI_MainWindow.Ui_MainWindow, "Numerictrainingmetrics"):
            for filename in  UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].index:
                    if filename not in table["Filename"]:
                                    QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab,"Error:" , "A sample has been identified for which the raw file name was not found in the ID files: "+str(filename) + ". The sample was removed from further analysis. Make sure the files in Filename column correspond with file names of IDs." )
                                    UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].drop([filename])
                    
                        
            if(UI_MainWindow.Ui_MainWindow.badPredicted):
                    RandomForest.RunRandomForest(self)
                   
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
                table.drop(table.index[ii], inplace=True)
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
        
        
        badset = badset.sort_values("B")
        badset.index = results.index
        badset["X"] = range(0,len(badset.index)) #Later the annotations get added to this column
        global fig
        fig = Figure()#figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        global ax
        global annot
        ax = fig.add_subplot(1,1,1)
        fig.subplots_adjust(bottom=0.3)
        for i in range(0,len(badset.index)):
            if badset["predict"].iloc[i]=='G':
                ax.plot(badset.index[i], badset["B"].iloc[i],  marker='o', markerfacecolor='dimgrey', markeredgecolor='k')
            else:
                ax.plot(badset.index[i], badset["B"].iloc[i],  marker='o', markerfacecolor='red', markeredgecolor='r')
        ax.set_ylabel("Probability of sample being classified as 'bad'")
        FigureCanvas.__init__(self, fig)
        #self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        ax.set_title("Red samples were classified as 'bad' by the model", fontsize=9)
        fig.suptitle("Probability of each sample being classified into the same category as the 'bad' training data", fontsize=10)
        
        for tick in ax.get_xticklabels():
                tick.set_rotation(90)
                
        self.compute_initial_figure()
        annot = ax.annotate("", xy=(0,0.5),color='green') 
        fig.savefig("RFPlot.png", dpi = 500)
   
    def compute_initial_figure(self):
        pass
    
    def printForReport(self):
        fig.savefig("RFPlot.png", dpi = 500)

    def createTable(self):
        UI_MainWindow.Ui_MainWindow.TrainingOrTestSet.badbtn = QtWidgets.QPushButton(
                'This is my selection for suboptimal quality.',
                UI_MainWindow.Ui_MainWindow.TrainingOrTestSet)
        UI_MainWindow.Ui_MainWindow.TrainingOrTestSet.badbtn.setEnabled(False)
        
        self.table = QtWidgets.QTableWidget()
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        df = UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0]
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                x = str(df.iloc[i, j])
                self.table.setItem(i, j, QTableWidgetItem(x))
        self.table.setHorizontalHeaderLabels(df.columns)
        self.table.setSortingEnabled(True)
        
        RFSelectionGrid = QtWidgets.QGridLayout(UI_MainWindow.Ui_MainWindow.TrainingOrTestSet)
        RFSelectionGrid.addWidget(self.table,0,0,1,3)
        RFSelectionGrid.addWidget(UI_MainWindow.Ui_MainWindow.TrainingOrTestSet.badbtn,2,1,2,1)
        UI_MainWindow.Ui_MainWindow.TrainingOrTestSet.badbtn.clicked.connect(lambda: RandomForest.compute(self))
        UI_MainWindow.Ui_MainWindow.TrainingOrTestSet.badbtn.setEnabled(True)
            
        
    def compute(self):
        UI_MainWindow.Ui_MainWindow.badpredictionList = []
        UI_MainWindow.Ui_MainWindow.TrainingOrTestSet.badbtn.setEnabled(False)
        if type(UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].index[0]) != str and "Filename" in UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].columns:
            UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].index = UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0]["Filename"]
        
        for item in self.table.selectionModel().selectedRows():
            UI_MainWindow.Ui_MainWindow.badpredictionList.append(UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].index[item.row()])
        print(len(UI_MainWindow.Ui_MainWindow.badpredictionList))
        if len(UI_MainWindow.Ui_MainWindow.badpredictionList)>2:
                    RandomForest.RunRandomForest(self)
        #for index in sorted(self.table.selectionModel().selectedRows()):
        
    def RunRandomForest(self):
        for column in UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].columns:
            if column not in UI_MainWindow.Ui_MainWindow.metrics[0].columns and column != "GoodOrBad":
                UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0] = UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].drop(columns=[column])
                
      
        RandomForest.createguideSet(RandomForest)
        
        dataToBeSplit = RandomForest.guideSetDf
                    
        dataToBeSplit.columns= RandomForest.guideSetDf.columns
                    
        dataToBeSplit["GoodOrBad"] = dataToBeSplit["GoodOrBad"].astype('category')
        training_columns = list(dataToBeSplit.columns[dataToBeSplit.columns != 'GoodOrBad'])
        # Output parameter train against input parameters
        response_column = 'GoodOrBad'
        # Split data into train and testing
        h2o.init()
        dataToBeSplit = h2o.H2OFrame(dataToBeSplit)
        train, test = dataToBeSplit.split_frame(ratios=[0.6], seed = 1)
                    
                    
        #Check that the training set contains both groups else error is thrown:
        while len(train["GoodOrBad"].unique())<2:
                        train, test = dataToBeSplit.split_frame(ratios=[0.6], seed = 1)
                        
                    
        train = train.as_data_frame()
        train["GoodOrBad"] = train["GoodOrBad"].astype('category')
        RandomForest.train = train #For the report writing
        print("The number of good in the training section are: " + str( len(train[train["GoodOrBad"]=="G"])))
        test = test.as_data_frame()
        RandomForest.test = test
                    
        # Search criteria
        search_criteria = {'strategy': 'RandomDiscrete',  'seed': 1}
        # Hyper parameters
        hyper_parameters = {'ntrees':[50,200], 'max_depth':[20,40], 'mtries':-1}
                    
        models = H2OGridSearch(H2ORandomForestEstimator(balance_classes=True, seed = 1),  hyper_params=hyper_parameters, search_criteria = search_criteria)
                    
        models.train(x=training_columns, y=response_column, training_frame=h2o.H2OFrame(train), seed=1)
                    
        sortedModels= models.get_grid(sort_by='accuracy', decreasing=True)
                    
        best_model = sortedModels.models[0]

        # Now let's evaluate the model performance on a test set
        # so we get an honest estimate of top model performance
        performance = best_model.model_performance(h2o.H2OFrame(test))

        RandomForest.performance = performance
        #Run the random Forest on the original data:
        rf = best_model.predict(h2o.H2OFrame(UI_MainWindow.Ui_MainWindow.NumericMetrics[0]))
        results = rf.as_data_frame()
        results.index = UI_MainWindow.Ui_MainWindow.NumericMetrics[0].index
        RandomForestResultsTab.LongitudinalTab.printModelResults(self, performance, results, best_model)
        UI_MainWindow.Ui_MainWindow.EnableAnalysisButtons(self)
                    