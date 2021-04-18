import sys
import Main
import pandas as pd
import os
from PyQt5 import QtWidgets,QtCore
import MainParser
import pepXMLReader
import globalVars

class maxQuantTxtReader(object):
    def parseTxt(self, file):
        with open(file) as thisFile:
            df = pd.read_csv(thisFile, sep="\t")
        
        if "Raw file" in df.columns:
            for file in df["Raw file"]:
                if "Experiment" in df.columns:
                    if file in  df["Experiment"].values:
                        df= df.drop(df[ df['Raw file'] == file].index)
            df.index = df["Raw file"]
            
        pepTable = pd.DataFrame(index =df.index , columns = ["Filename","Number of distinct peptides","Number of spectra identified"])
        
        if "Peptide Sequences Identified" in df.columns:
            pepTable["Number of distinct peptides"] = df["Peptide Sequences Identified"]
        if "Raw file" in df.columns:
            pepTable["Filename"] = df["Raw file"]
        if "MS/MS Identified" in df.columns:
            pepTable["Number of spectra identified"] = df["MS/MS Identified"]
        QtCore.QMetaObject.invokeMethod(globalVars.var.progress1, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 40))
        #summary.txt contains a total which we are not interested in
        if "Total" in pepTable.index:
            pepTable = pepTable.drop(["Total"])
            
        if len(pepTable["Number of distinct peptides"])==0 or len(pepTable["Filename"])==0 or len(pepTable["Number of spectra identified"])==0:
            QtWidgets.QMessageBox.warning("","Something went wrong, please try a different file.")
            globalVars.var.parser.GetTrainingSetFiles()       
            if globalVars.var.TrainingSetTable:
                if "pepxml" in globalVars.var.TrainingSetfiles[0].lower():
                    globalVars.var.TrainingSetTable = pepXMLReader.pepXMLReader.parsePepXML(self, TrainingSetfiles)
                elif ".txt" in globalVars.var.TrainingSetfiles[0].lower():
                    globalVars.var.TrainingSetTable = maxQuantTxtReader.parseTxt(self, TrainingSetfiles[0])
             
        else:
            QtCore.QMetaObject.invokeMethod(globalVars.var.progress1, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 90))
            return pepTable    
