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


class BrowseWindow(QtWidgets.QMainWindow):
    def __init__(self, Ui_MainWindow):
        self.title = "Load file"
        UI_MainWindow.Ui_MainWindow.EnableButtons(self)
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
                   inputFiles = possibleInputFiles
                   UI_MainWindow.Ui_MainWindow.metrics =  \
                       FileInput.BrowseWindow.CombineJSONs(
                           UI_MainWindow.Ui_MainWindow, inputFiles)
                   UI_MainWindow.Ui_MainWindow.metrics.set_index(
                       UI_MainWindow.Ui_MainWindow.metrics.iloc[:,0])
                   DataPreparation.DataPrep.ExtractNumericColumns(
                       UI_MainWindow.Ui_MainWindow.metrics)
                   DataPreparation.DataPrep.RemoveLowVarianceColumns(
                       UI_MainWindow.Ui_MainWindow)
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
                    UI_MainWindow.Ui_MainWindow.filename.setText("   " + inputFile + "  ")
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
        for file in inputFiles:
                #Input reading of jsonfiles here:
            with open(file) as f:
                try:
                    metrics = json.loads(f.read())
                except:
                    QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab,"Error:", 
                                            "Upload failed. Please check the content of the files and try again.")
                    
                    UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
            metricsDf = pd.DataFrame(metrics)
            columnNames = []
            for ii in metricsDf["mzQC"]["runQuality"]:
                for iii in ii["qualityParameters"]:
                    columnNames.append(iii["name"])
            PCAInput = pd.DataFrame(columns=columnNames)
            myPIArray = PCAInput.values
            tempVec = []
            for ii in metricsDf["mzQC"]["runQuality"]:
                for iii in ii["qualityParameters"]:
                    tempVec.append(iii["value"])

            myPIArray = np.vstack((myPIArray, tempVec))
            PCAInput = pd.DataFrame(myPIArray, columns=columnNames)
            Allmetrics = Allmetrics.append(PCAInput)
        if(Allmetrics.iloc[:, 0].count() < 2):
            QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab, "Error:",
                              "There are not enough samples in your file \
                              to conduct analysis. Please choose \
                              another file.")
            UI_MainWindow.Ui_MainWindow.onBrowseClicked(
                    UI_MainWindow.Ui_MainWindow)
        return Allmetrics

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
   
        


