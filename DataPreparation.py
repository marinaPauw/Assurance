import sys
import PyQt5
from PyQt5.QtWidgets import *
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
            metrics["dates"] = "Default"
            dateVector = []
            for row in metrics["StartTimeStamp"]:
                dateVector.append(row[:10])
            metrics["dates"] = dateVector
            print("Date column added. There are now %d columns",
                  len(metrics.columns))
        
        if namecolumn:
            del NumericMetrics[NumericMetrics.columns[0]]
        
        NumericMetrics = NumericMetrics.select_dtypes(['number'])
        print("Non-numeric columns removed. There are now %d columns",
              len(NumericMetrics.columns))
        print(NumericMetrics.columns.values)
        # Now remove all columns that are not numeric, \
        # including date and starttimestamp
        NumericMetrics = NumericMetrics.replace([np.inf, -np.inf], np.nan)
        NumericMetrics = NumericMetrics.fillna(0)

        FileInput.BrowseWindow.currentDataset = NumericMetrics
        return metrics

    def RemoveLowVarianceColumns(self):
        Nm = FileInput.BrowseWindow.currentDataset
        print(type(FileInput.BrowseWindow.currentDataset))
        droppedColumns = []
        dpIndex = []
        threshold = 0.01
        if (len(Nm.columns)) < 1:

            QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab, "Error:",
                              "After removing low variance columns, there were no columns left from which to conduct any sort of analysis. Please select another dataset.")
            UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.
                                                        Ui_MainWindow)

        for i in range(len(Nm.columns)):
            variance = np.var(Nm.iloc[:, i])
            if (variance < threshold):
                droppedColumns.append(Nm.columns[i])
                dpIndex.append(i)
        Nm = Nm.drop(droppedColumns, axis=1)
        # Nm.drop(Nm.columns[dpIndex[i]],axis=1,inplace=True)
        #if (len(Nm.columns)) < 1:
        #    QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab, "Error:",
       #                       "After removing low variance columns, there were no columns left from which to conduct any sort of analysis. Please select another dataset.")
        #    UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.
        #                                                Ui_MainWindow)

        print("Low variance columns removed. There are now %d columns",
              len(Nm.columns))
        print(Nm.columns.values)
        if Nm.index[0]==0 and "Filename" in UI_MainWindow.Ui_MainWindow.metrics[0].columns:
            Nm.index = UI_MainWindow.Ui_MainWindow.metrics[0]["Filename"]
            UI_MainWindow.Ui_MainWindow.metrics[0].index = UI_MainWindow.Ui_MainWindow.metrics[0]["Filename"]
        UI_MainWindow.Ui_MainWindow.NumericMetrics = list()
        UI_MainWindow.Ui_MainWindow.NumericMetrics.append(Nm)
        FileInput.BrowseWindow.currentDataset = Nm

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
