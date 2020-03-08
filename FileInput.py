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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import re
import UI_MainWindow
import DataPreparation
import FileInput
import pandas as pd
import json
import numpy as np
import os
import collections




class BrowseWindow(QtWidgets.QMainWindow):
    def __init__(self, Ui_MainWindow):
        self.title = "Load file"
        UI_MainWindow.Ui_MainWindow.EnableAnalysisButtons(self)
        global inputFile 

    def GetInputFile(Ui_MainWindow):
        files = QtWidgets. QFileDialog()
        files.setFileMode(QFileDialog.ExistingFiles)
        possibleinputFiles,_ = QtWidgets. QFileDialog.getOpenFileNames(Ui_MainWindow.tab, 
                                                               "Browse", "",
                                                               "All Files (*)", 
                                                               options=
                                                               QFileDialog.\
                                                                   Options())
        if(possibleinputFiles):
            if(len(possibleinputFiles) > 1):
                justJSONFiles = True
                for possiblefile in possibleinputFiles:
                   if(".json" not in possiblefile):
                       justJSONFiles = False
                if not justJSONFiles :
                    QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab,
                                      "Error:" ,"You may select multiple mzQC files to combine into one table, but you may not select multiple files of any other type.")
                    UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)

                if(justJSONFiles==True):
                   inputFiles = possibleinputFiles
                   UI_MainWindow.Ui_MainWindow.metrics =  \
                       FileInput.BrowseWindow.CombineJSONs(
                           UI_MainWindow.Ui_MainWindow, inputFiles)
                   UI_MainWindow.Ui_MainWindow.NumericMetrics = []
                   for i in range(1,len(UI_MainWindow.Ui_MainWindow.metrics)):
                       #UI_MainWindow.Ui_MainWindow.metrics.set_index(
                        #   UI_MainWindow.Ui_MainWindow.metrics.iloc[:,0])
                       BrowseWindow.currentDataset = UI_MainWindow.Ui_MainWindow.metrics[i]
                       DataPreparation.DataPrep.ExtractNumericColumns(
                           BrowseWindow.currentDataset)
                       DataPreparation.DataPrep.RemoveLowVarianceColumns(
                           UI_MainWindow.Ui_MainWindow)
                       UI_MainWindow.Ui_MainWindow.NumericMetrics.append(BrowseWindow.currentDataset)
                   str1 = " " 
                   UI_MainWindow.Ui_MainWindow.tab.UploadFrame.filename.setText(str1.join(inputFiles))
                   UI_MainWindow.Ui_MainWindow.DisableBrowseButtons(UI_MainWindow.Ui_MainWindow)
            else:
                possibleinputFile = possibleinputFiles[0]
                inputFile = BrowseWindow.fileTypeCheck(possibleinputFile)
                if(inputFile):
                    counter = inputFile.count('.') 
                    if(counter==1):# .mzML
                         BrowseWindow.datasetname,throw = inputFile.split('.')
                    elif(counter==2):#If the program lists .wiff.scan
                         BrowseWindow.datasetname,throw,throw = inputFile.split('.')
                    elif(counter==3):
                         BrowseWindow.datasetname,throw,throw,throw = inputFile.split('.')
                    else:
                         BrowseWindow.datasetname = inputFile
                    UI_MainWindow.Ui_MainWindow.tab.UploadFrame.filename.setText("   " + inputFile + "  ")
                    return inputFile
   
    def GetTrainingSetFile(Ui_MainWindow):
        possibleInputFile, _ =QtWidgets. QFileDialog.getOpenFileName(
            Ui_MainWindow.tab,"Select a file from which to create the training set:", "","All Files (*)", options = QFileDialog.Options())
        if(possibleInputFile):
            TrainingSetFile = BrowseWindow.TrainingSetFileTypeCheck(possibleInputFile)
            if(TrainingSetFile):
                return TrainingSetFile
    
    def fileTypeCheck(inputFile):
        if inputFile.endswith('.json') or inputFile.endswith('.csv') or inputFile.endswith('.tsv'):
            return inputFile
        else:
            QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab,
                              "Message from Assurance: ", "Error: File type incorrect. Please load a.json, .tsv or .csv file. Also please ensure that the decimals are separated by '.'.")
            UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)

    def metricsParsing(inputFile):
       try:
        if inputFile.endswith('.json'):
            with open(inputFile) as f:
             metrics = json.loads(f.read())
            metricsDf = pd.DataFrame(metrics)
            columnNames = []
            for ii in metricsDf["mzQC"]["runQuality"]:
               for iii in ii["qualityParameters"]:
                columnNames.append (iii["name"])
            PCAInput = pd.DataFrame(columns=columnNames)
            myPIArray = PCAInput.values
            tempVec = []
            for ii in metricsDf["mzQC"]["runQuality"]:
               for iii in ii["qualityParameters"]:
                  tempVec.append(iii["value"])
        
            myPIArray = np.vstack((myPIArray, tempVec)) 
            PCAInput = pd.DataFrame(myPIArray, columns=columnNames)
            metrics = PCAInput
            if(metrics.iloc[:, 0].count() < 2) :
                QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab,"Error:", 
                                  "There are not enough samples in your file to conduct analysis. Please choose another file.")
                UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
            return metrics

        elif inputFile.endswith('.csv'):
            metrics = pd.DataFrame(pd.read_csv(inputFile, sep=","))
            if(metrics.iloc[:, 0].count() < 2):
                QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab, "Error:",
                                  "There are not enough samples in your file to conduct analysis. Please choose another file.")
                UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
            return metrics

        elif inputFile.endswith('.tsv'):
            metrics = pd.DataFrame(pd.read_csv(inputFile, sep="\t"))
            if(metrics.iloc[:, 0].count() < 2):
                QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab, "Error:",
                                  "There are not enough samples in your file to conduct analysis. Please choose another file.")
                UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
            return metrics


       except json.decoder.JSONDecodeError:
            QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab,"Message from Assurance: ", "This file does not contain data in the correct format. Please load a different file.")
            UI_MainWindow.Ui_MainWindow.onBrowseClicked(
                UI_MainWindow.Ui_MainWindow)

    def FileCheck(path):       
        try:
            return(open(path,'rb'))
        except IOError:
            QMessageBox.warning(UI_MainWindow.Ui_MainWindow, "Message from Assurance: ",
                              "Error loading file...")
            return 0
    
    def TrainingSetFileTypeCheck(inputFile):
          if inputFile.endswith('.csv') or inputFile.endswith('.tsv'):
            return inputFile

          else:
            QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab, "Message from Assurance: ", "Error: File type incorrect. Please load a .json, .tsv or .csv file. Also please ensure that the decimals are separated by '.'.")
            UI_MainWindow.Ui_MainWindow.onLongitudinalClicked(UI_MainWindow.Ui_MainWindow)
            
    def TrainingSetParse(inputFile):
        if inputFile.endswith('.csv'):
            TrainingSet = pd.DataFrame(pd.read_csv(inputFile, sep=","))
            BrowseWindow.TrainingSetFileMatchNames(BrowseWindow,
                                                      TrainingSet)
            return TrainingSet

        elif inputFile.endswith('.tsv'):
            TrainingSet = pd.DataFrame(pd.read_csv(inputFile, sep="\t"))
            BrowseWindow.TrainingSetFileMatchNames(BrowseWindow,
                                                      TrainingSet)
            return TrainingSet

    def TrainingSetFileMatchNames(self, TrainingSet):
        for i in range(0, len(TrainingSet.iloc[:, 0])):
            if(UI_MainWindow.Ui_MainWindow.metrics.iloc[i, 0] != TrainingSet.iloc[i, 0]):
                QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab, "Error:",
                                  "The first column of the  file does not match that of the quality metrics input file. Try again.")
                UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)

    def CombineJSONs(self, inputFiles):
        global Allmetrics
        Allmetrics = pd.DataFrame()
        metrics = {}
        for file in inputFiles:
            try:
                file1 = open(file, 'r')
                string1 = file1.read()
                metrics = json.loads(string1)
                filename = os.path.splitext(os.path.basename(file))[0]
                #Input reading of jsonfiles here:
            except:
                    QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab,"Error:", 
                                            "Upload failed. Please check the content of the files and try again.")
                    UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
            metricsDf = pd.DataFrame(metrics)
            # Create dataframes - for SwaMe we need one for comprehensive, one for swath, one for rt, one for quartiles, one for quantiles
            uniqueSizes = []
            comprehensiveMetricsDf  = pd.DataFrame()
            AllMetricSizesDf = list()


            comprehensiveColumnNames = []
            AllColumnNamesDf = list()

            for ii in metricsDf["mzQC"]["runQuality"]:
               # NumofTotalTransitions = []
               # SumOfTotalTransition = 0
              #  irtCounter=0
              #  for iii in ii["qualityParameters"]:
              #      if iii["name"]=='Prognosticator Metric: IrtPeptides':
              #          for jjj in range(1 , len(metricsDf["mzQC"]["runQuality"][0]["qualityParameters"][iii]["value"])):
              #              NumofTotalTransitions.append(len(metricsDf["mzQC"]["runQuality"][0]["qualityParameters"][iii]["value"][jjj]))
              #              SumOfTotalTransitions= SumOfTotalTransitions+1

                for iii in ii["qualityParameters"]:
                    metricname = iii["name"]
                    if(": " in metricname):
                        metricname = metricname.split(": ",1)[1] 
                    # Before we do anything else, check if its an irt metric:
               #     irtMetricNames = ["MeanIrtMassError","MaxIrtMassError","IrtPeptideFoundProportion","IrtPeptides","IrtPeptidesFound", "IrtSpread","IrtOrderedness"]
               #     if metricname in irtMetricNames:
               #        if not irtMetricsDF:
               #             irtMetricsDF = pd.DataFrame(index = range(1, NumofTotalTransitions),columns = ["PeptideSequence", "PrecursorTargetMz", "RetentionTime", "ProductTargetMzs", "Intensities", "ActualMzs", "AverageMassError", "TotalMassError", "TotalMassErrorPpm", "AverageMassErrorPpm", "MeanIrtMassError","MaxIrtMassError","IrtPeptideFoundProportion","IrtPeptidesFound", "IrtSpread","IrtOrderedness"])
               #             index = 0
               #        if metricname != "IrtPeptides":
               #             for j in range(1,NumOfTransFound):
               #                 irtMetricsDF[metricname][j] = iii["value"]
               ##        else: 
                #            irtMetricsDF.loc[metricname] = iii["value"]* len(irtMetricsDF)






                    if "value" in iii:# This means that an empty value is never added to the dataframe
                        # Now we need to figure out in which dataframe it belongs:
                        #Something other than comprehensive:
                        if isinstance(iii["value"], collections.Sequence) and not isinstance(iii["value"],str):
                            # DO we already have a DF for it:
                            if len(iii["value"]) in uniqueSizes: 
                                index = uniqueSizes.index(len(iii["value"]))
                                #Check if columnname already exists:
                                if(metricname in AllMetricSizesDf[index]):
                                    cIndex = AllMetricSizesDf[index].index(iii["name"])
                                    # Check if its the first instance for this file, else we need to make new NA rows: The idea is that there should be index * iii["value"]
                                    if len(AllMetricSizesDf.index) != index * len(iii["value"]): # first instance of this file
                                        #create some NA's 
                                        for i in len(AllMetricSizesDf[index].columns):
                                            for ii in range((index -1) * len(iii["value"]),index*len(iii["value"])):
                                                AllMetricSizesDf[index][ii][i] = "NA" * len(iii["value"])
                                    # Now change the NA's to values:
                                    AllMetricsSizesDf[index][metricname] = iii["value"]
                                 

                                else:# We first need to create the column:

                                   # Check if the length of the other columns is still just one file else we need to fill with NAs:
                                   if len(AllMetricSizesDf[index].index) == len(iii["value"]): # Just one file
                                       AllMetricSizesDf[index][metricname] = iii["value"]
                                   else:
                                       if len(AllMetricSizesDf[index].index)>0:#There are other files, but they didn't have a value for this metric
                                            AllMetricSizesDf[index][metricname] = np.array([np.repeat("NA" , len(AllMetricSizesDf[index].index) -len(iii["value"])),iii["value"]])
                                            
                                       else:#This is the first metric
                                            AllMetricSizesDf[index][metricname] = iii["value"]


                            else: # We create one:
                                uniqueSizes.append(len(iii["value"]))
                                index = uniqueSizes.index(len(iii["value"]))
                                AllMetricSizesDf.append(pd.DataFrame())
                                temp = []
                                for i in range(1,len(iii["value"])+1):
                                    stringstojoin = {filename, metricname, str(i)}
                                    separator = "_"
                                    temp.append(separator.join(stringstojoin))
                                AllMetricSizesDf[index]['Name'] = temp
                                AllMetricSizesDf[index][metricname] = iii["value"]


                        elif 1 in uniqueSizes: 
                                index = uniqueSizes.index(1)
                                #Check if columnname already exists:
                                if(metricname in AllMetricSizesDf[index]):
                                    cIndex = AllMetricSizesDf[index].index(iii["name"])
                                    # Check if its the first instance for this file, else we need to make new NA rows: The idea is that there should be index * iii["value"]
                                    if len(AllMetricSizesDf.index) != index * len(iii["value"]): # first instance of this file
                                        #create some NA's 
                                        for i in len(AllMetricSizesDf[index].columns):
                                                AllMetricSizesDf[index][ii][i] = "NA" * len(iii["value"])
                                    # Now change the NA's to values:
                                    AllMetricsSizesDf[index][metricname] = iii["value"]
                                 

                                else:# We first need to create the column:

                                   # Check if the length of the other columns is still just one file else we need to fill with NAs:
                                   if len(AllMetricSizesDf[index].index) == 0 or len(AllMetricSizesDf[index].index) == 1: # FIrst value of the whole dataset or second value of the dataset
                                       AllMetricSizesDf[index][metricname] = iii["value"]
                                   else:
                                       if len(AllMetricSizesDf[index].index) >1:
                                        AllMetricSizesDf[index][metricname] = np.array([np.repeat("NA" , len(AllMetricSizesDf[index].index)),iii["value"]])


                        else: # We create need to create the comprehensive table:
                                uniqueSizes.append(1)
                                index = uniqueSizes.index(1)
                                AllMetricSizesDf.append(pd.DataFrame())
                                stringstojoin = {filename, metricname, "1"}
                                separator = "_"
                                AllMetricSizesDf[index]['Name'] = separator.join(stringstojoin)
                                AllMetricSizesDf[index][metricname] = iii["value"]

        return AllMetricSizesDf


    def QuaMeterFileTypeCheck(self, inputFile):
        if inputFile.endswith('.wiff') or inputFile.endswith('.raw') or inputFile.endswith('.mzML'):
            return inputFile
        else:
             QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab,
                              "Message from Assurance: ", "Error: File type incorrect. Please load a .mzML, .wiff or .raw file.")
             UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
     
    def GetQuaMeterInputFiles(self):
        possibleinputFiles,_ = QtWidgets. QFileDialog.getOpenFileNames(None, " Files for QuaMeter input", "", "mzML files (*.mzML)", 
                                                               options=
                                                               QFileDialog.\
                                                                   Options())
        if(possibleinputFiles):
           inputFiles = [] 
           if(len(possibleinputFiles) > 1):
                for possiblefile in possibleinputFiles:
                  inputFiles.append(BrowseWindow.QuaMeterFileTypeCheck(self, possiblefile))
               
           else:
                possiblefile = possibleinputFiles[0]
                inputFiles.append(BrowseWindow.QuaMeterFileTypeCheck(self, possiblefile))

        if(inputFiles):
            return inputFiles

    def GetQuaMeterPath(self):
        QuaMeterPath,_ = QtWidgets. QFileDialog.getOpenFileNames(None, "Please locate the QuaMeter exe on your system:", "", "exe files (*.exe)", 
                                                               options=
                                                               QFileDialog.\
                                                                   Options())
        if(QuaMeterPath):
            return QuaMeterPath

    def SwaMeFileTypeCheck(self, inputFile):
        if inputFile.endswith('.mzML'):
            return inputFile
        else:
             QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab,
                              "Message from Assurance: ", "Error: File type incorrect. Please load a .mzML file.")
             UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
     
    def GetSwaMeInputFile(self):
        possibleinputFile,_ = QtWidgets. QFileDialog.getOpenFileName(None, " Input File for SwaMe:", "", "mzML files (*.mzML)", 
                                                               options=
                                                               QFileDialog.\
                                                                   Options())
        if(possibleinputFile):
                inputFile= BrowseWindow.SwaMeFileTypeCheck(self, possibleinputFile)

        if(inputFile):
            return inputFile

    def GetSwaMePath(self):
        SwaMePath,_ = QtWidgets. QFileDialog.getOpenFileNames(None, "Please locate the SwaMe exe on your system:", "", "exe files (*.exe)", 
                                                               options=
                                                               QFileDialog.\
                                                                   Options())
        if(SwaMePath):
            return SwaMePath

    def GetIRTInputFile(Ui_MainWindow):
        file = QtWidgets. QFileDialog()
        file.setFileMode(QFileDialog.ExistingFile)
        possibleinputFile,_ = QtWidgets. QFileDialog.getOpenFileName(Ui_MainWindow.tab, 
                                                               "Browse", "",
                                                               "TraML Files (*.TraML)", 
                                                               options=
                                                               QFileDialog.\
                                                                   Options())
        if possibleinputFile:
            if possibleinputFile.endswith('.TraML') or possibleinputFile.endswith('.tsv') or possibleinputFile.endswith('.csv'):
                return possibleinputFile

    def find_indices(lst, condition):
            return [i for i, elem in enumerate(lst) if condition(elem)]
   
        


