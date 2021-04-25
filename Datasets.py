import sys
import Main
from PyQt5 import QtCore, QtWidgets
import scipy
from sklearn import decomposition as sd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, RobustScaler
from matplotlib.backends.backend_qt5agg\
     import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import matplotlib.pyplot as plt
import re
import MainParser
import Main
import numpy as np
import pandas as pd
import logging
import globalVars

class Datasets(QtCore.QObject):   

    def _init_(self):    
        self.metrics = list()
        self.numericMetrics = list()
        self.trainingMetrics = None
        self.numericTrainingMetrics = None
        self.currentDataset = None

    def ExtractNumericColumns(self, training):
        #Swame produces multiple dataframes, Quameter only one so we must loop through them each:
        #In order to make this applicable to both the test and training data and the main data, 
        # we assign a variable named data and reassign the variable in the end
        if training:
            #This function is the first time we will need to make a numerictraining metrics obj:
            self.numericTrainingMetrics = self.trainingMetrics
            data = self.numericTrainingMetrics
        else:
            #This function is the first time we will need to make a numericMetrics obj:
            data = self.metrics.copy()#Else stupid python will perform changes to self.metrics I kid you not!
        
        for i in range(0,len(data)):
        
            dateColumn = False
            namecolumn = False
            for col in data[i].columns:
                if isinstance(col,str):
                    if "StartTimeStamp" in col:
                        dateColumn = True
                    if "Name" in col:
                        namecolumn = True
                
            if dateColumn:
                dateVector = []
                dateColumnSuccess = True
                if "StartTimeStamp" in data[i].columns.values:
                    for row in data[i]["StartTimeStamp"]:
                        row = str(row)#This is for sciex converter where the timestamp column is not present and therefore read as a float
                        if len(row)==20:
                            dateVector.append(row[:10])
                        else:
                            dateColumnSuccess = False
                    
                    
                    if(dateColumnSuccess):
                        data[i]["dates"] = dateVector
                        self.metrics[i]['dates'] = dateVector
                    else:
                        logging.info("Something is wrong with the startTimeStamp, date calculation abandoned.This may cause problems later on and startTimeStamp column was removed.")
                        data[i] = data[i].drop('StartTimeStamp', axis=1)
            
            if namecolumn:
                del data[i][data[i].columns[0]]           
            
            data[i] = data[i].select_dtypes(['number'])
            
            logging.info(data[i].columns.values)
            data[i] = data[i].fillna(0)
        if training:
            self.numericTrainingMetrics = data
        else:
            self.numericMetrics = data        

    def RemoveLowVarianceColumns(self, training):
        #Again to make this universally applicable, we assign to a temp variable and reassign
        if training:
            data = self.numericTrainingMetrics
        else:
            data = self.numericMetrics
        
        for i in range(0,len(data)):
            Files = []
            if "Filename" in data[i].columns:
                Files = data[i]["Filename"]
            droppedColumns = []
            dpIndex = []
            threshold = 0.01
            if (len(data[i].columns)) < 1:
                    return

            for ii in range(0, len(data[i].columns)):
                try: 
                    variance = np.var(data[i].iloc[:,ii])
                    if (variance < threshold):
                        droppedColumns.append(data[i].columns[ii])
                        dpIndex.append(ii)
                except:
                    logging.info("column variance could not be calculated possibly due to a missing value in the column that could not be dealt with earlier. Column is dropped from analysis.")
                    droppedColumns.append(data[i].columns[ii])
            data[i].drop(columns = droppedColumns, axis=1)

            if len(Files)>0:
                data[i].index = Files
        if training:
            self.numericTrainingMetrics = data
        else:
            self.numericMetrics = data

    def FindRealSampleNames(self, rawSampleNames):
        realSampleNames = []
        for rawSampleName in rawSampleNames:
            if type(rawSampleName) != int:
                counter = rawSampleName.count('.')
                if (counter == 1):  # .mzML
                    realSampleName, throw = rawSampleName.split('.')
                elif (counter == 2):  # .wiff.scan
                    realSampleName, throw, throw = rawSampleName.split('.')
                elif (counter == 3):
                    realSampleName, throw, throw, throw = rawSampleName.split('.')
                else:
                    realSampleName = rawSampleName
                realSampleNames.append(realSampleName)
            else:
                rawSampleName = str(rawSampleName)
                realSampleNames.append(rawSampleName)
        return realSampleNames

    def contains_string(self, l):
        return any(isinstance(item, str) for item in l)