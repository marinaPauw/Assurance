import sys
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
import sys
import statistics
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
import FileInput
import UI_MainWindow
import numpy as np
import pandas as pd
import Datasets
import logging


class DataPrep(object):
    """description of class"""

    def ExtractNumericColumns(self, metrics):
        # All analysis basically require numeric datatypes so lets \
        # sort the numeric columns into one dataset for future analysis:

        NumericMetrics = metrics
        dateColumn = False
        namecolumn = False
        for col in metrics.columns:
            if isinstance(col,str):
                if "StartTimeStamp" in col:
                    dateColumn = True
                if "Name" in col:
                    namecolumn = True
        if dateColumn:
            dateVector = []
            dateColumnSuccess = True
            if "StartTimeStamp" in metrics.columns.values:
                for row in metrics["StartTimeStamp"]:
                    row = str(row)#This is for sciex converter where the timestamp column is not present and therefore read as a float
                    if len(row)==20:
                        dateVector.append(row[:10])
                    else:
                        dateColumnSuccess = False
                if(dateColumnSuccess):
                    metrics["dates"] = dateVector
                    logging.info("Date column added. There are now %d columns",
                    len(metrics.columns))
                else:
                    logging.info("Something is wrong with the startTimeStamp, date calculation abandoned.This may cause problems later on and startTimeStamp column was removed.")
                    NumericMetrics = NumericMetrics.drop('StartTimeStamp', axis=1)
        
        if namecolumn:
            del NumericMetrics[NumericMetrics.columns[0]]
        
        NumericMetrics = NumericMetrics.select_dtypes(['number'])
        logging.info("Non-numeric columns removed. There are now %d columns",
              len(NumericMetrics.columns))
        logging.info(NumericMetrics.columns.values)
        # Now remove all columns that are not numeric, \
        # including date and starttimestamp
        #NumericMetrics = NumericMetrics.replace([np.inf, -np.inf], np.nan)
        NumericMetrics = NumericMetrics.fillna(0)
        return NumericMetrics

    def RemoveLowVarianceColumns(self, Nm):
        Files = []
        if "Filename" in Nm.columns:
            Files = Nm["Filename"]
        droppedColumns = []
        dpIndex = []
        threshold = 0.01
        if (len(Nm.columns)) < 1:
                return

        for i in range(0, len(Nm.columns)):
            try: 
                variance = np.var(Nm.iloc[:,i])
                if (variance < threshold):
                    droppedColumns.append(Nm.columns[i])
                    dpIndex.append(i)
            except:
                logging.info("column variance could not be calculated possibly due to a missing value in the column that could not be dealt with earlier. Column is dropped from analysis.")
                droppedColumns.append(Nm.columns[i])
        Nm.drop(columns = droppedColumns, axis=1)

        if len(Files)>0:
            Nm.index = Files
        return Nm

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
