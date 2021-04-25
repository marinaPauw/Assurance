import sys
from PyQt5 import QtWidgets, QtCore
import datetime
import Main
import globalVars
import pandas as pd
import numpy as np
import os
import collections
import json
from Datasets import Datasets
import logging


class Parser():
    def __init__(self):
        self.possibleInputFiles = list()
        self.trainingsetQualityFiles = list()
        self.trainingsetIDFiles = list()
        self.combinedList = list()
        self.NullError = False

    def GetInputFile(self):
        #This function sets possibleInputFiles if the upload option is selected (as opposed to running Qua/SwaMe)
        files = QtWidgets. QFileDialog()
        files.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        self.possibleInputFiles,_ = QtWidgets. QFileDialog.getOpenFileNames(parent=None,caption = "Browse", directory="",
                                                               filter = "All Files (*)", 
                                                               options=
                                                               QtWidgets.QFileDialog.\
                                                                   Options())
                               
    def parseInputFiles(self):
        #This function takes the variable possibleinputfiles and parses the files into the datasets obj created in the Main function
            logging.info(self.possibleInputFiles)
            if(len(self.possibleInputFiles) > 1):
                justJSONFiles = True
                justTSVFiles = True
                for possiblefile in self.possibleInputFiles:
                    if(".json" not in possiblefile):
                       justJSONFiles = False
                    if(".tsv" not in possiblefile):
                           justTSVFiles = False
                if not justJSONFiles and not justTSVFiles:
                    return False

                if(justJSONFiles==True):     
                    self.CombineJSONs(False)
                    if "Filename" in  globalVars.var.database.metrics[0].columns:
                            globalVars.var.database.metrics[0].index = globalVars.var.database.metrics[0]["Filename"]
                    elif "Dataset" in  globalVars.var.database.metrics[0].columns:
                            globalVars.var.database.metrics[0].index = globalVars.var.database.metrics[0]["Dataset"]        
                    str1 = " " 
                    inputs = str1.join(self.possibleInputFiles)
                    QtCore.QMetaObject.invokeMethod(globalVars.var.filenameDisplay, "setText",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(str, inputs))
                    
            
                elif(justTSVFiles == True):
                    self.CombineTSVs(False)          
                    for col in globalVars.var.database.metrics[0].columns:
                        if globalVars.var.database.metrics[0][col].isnull().values.all():
                                    self.NullError =True
                                    return
                    if "Filename" in  globalVars.var.database.metrics[0].columns:
                            globalVars.var.database.metrics[0].index = globalVars.var.database.metrics[0]["Filename"]
                    elif "Dataset" in  globalVars.var.database.metrics[0].columns:
                            globalVars.var.database.metrics[0].index = globalVars.var.database.metrics[0]["Dataset"]
                                        
                    str1 = " " 
                    inputs = str1.join(self.possibleInputFiles)
                    QtCore.QMetaObject.invokeMethod(globalVars.var.filenameDisplay, "setText",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(str, inputs))
                    
            
            else:
                logging.info(77)
                try:
                    if(self.fileTypeCheck(self.possibleInputFiles[0])):
                        QtCore.QMetaObject.invokeMethod(globalVars.var.filenameDisplay, "setText",
                                    QtCore.Qt.QueuedConnection,
                                    QtCore.Q_ARG(str, str(self.possibleInputFiles[0])))
                        globalVars.var.database.metrics = []
                        Parser.metricsParsing(self)
                        if "Filename" in  globalVars.var.database.metrics[0].columns:
                                globalVars.var.database.metrics[0].index = globalVars.var.database.metrics[0]["Filename"]
                        elif "Dataset" in  globalVars.var.database.metrics[0].columns:
                                globalVars.var.database.metrics[0].index = globalVars.var.database.metrics[0]["Dataset"]
                        for col in globalVars.var.database.metrics[0].columns:
                                if globalVars.var.database.metrics[0][col].isnull().all():                         
                                    globalVars.var.database.metrics[0]= globalVars.var.database.metrics[0].drop(columns = col)
                        dropRows = []
                        for index, row in globalVars.var.database.metrics[0].iterrows():
                                if row.isnull().all():
                                    dropRows.append(row)
                        if len(dropRows)>0:
                            globalVars.var.database.metrics[0] = globalVars.var.database.metrics[0].drop(index = dropRows)
                        logging.info(globalVars.var.database.metrics[0].head())
                except Exception as ex:
                    logging.info(ex)
                    
    def GetTrainingSetFiles(self):
        #This function sets the trainingsetFiles property of this class if the training files are ID files
        temp, _ =QtWidgets. QFileDialog.getOpenFileNames(
            globalVars.var.tab,"Select the files from which to create the training set:", "","All files (*)", options = QtWidgets.QFileDialog.Options())
        if(temp):
            for file in temp:
                if self.TrainingSetFileTypeCheck(file):
                    self.trainingsetIDFiles.append(file)
    
    def GetTrainingQualityFiles(self):
        #This function sets the trainingset for the training quality files
        try:
            files = QtWidgets. QFileDialog()
            files.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            self.trainingsetQualityFiles,_ = QtWidgets. QFileDialog.getOpenFileNames(globalVars.var.tab, 
                                                                "Locate the training set quality file(s):", "",
                                                                "All Files (*)", 
                                                                options=
                                                                QtWidgets.QFileDialog.\
                                                                    Options())
            if(self.trainingsetQualityFiles):
                if(len(self.trainingsetQualityFiles) > 1):
                    justJSONFiles = True
                    justTSVFiles = True
                    for possiblefile in self.trainingsetQualityFiles:
                        if(".json" not in possiblefile):
                            justJSONFiles = False
                        if(".tsv" not in possiblefile):
                            justTSVFiles = False   
                
                    if not justJSONFiles and not justTSVFiles:
                        return False

                    elif(justJSONFiles): 
                        self.CombineJSONs(True)
                        #Check if both are DDA or both are DIA:
                    
                            
                    elif justTSVFiles:
                        self.CombineTSVs(True)          
                    
                    else: 
                        return False
                        
                        
                else:
                        globalVars.var.Numerictrainingmetrics = []
                        df = pd.read_csv(self.trainingsetQualityFiles[0], sep="\t")   
                        for col in df.columns:
                            if df[col].isnull().values.all():
                                self.NullError =True
                                return
                        if 'Filename' in df.columns:
                            if ".mzML" in df['Filename'][0]:
                                for item in range(0,len(df['Filename'])):
                                    df['Filename'].iloc[item] = df['Filename'].iloc[item].split('.')[0]
                        #Nan's creep in if you make the tsv with excel sometimes
                            df.index = df['Filename']
                        globalVars.var.Numerictrainingmetrics.append(df)
        except:
            QtWidgets.QMessageBox.warning(globalVars.var,"Error","An error occured. Please double check the data.")
                   
    def checkTrainingQualityColumns(self):
        #Prepare the training quality data for Analysis
        globalVars.var.database.ExtractNumericColumns(True)#True referring to training dataset
        globalVars.var.database.RemoveLowVarianceColumns(True)
        
    def fileTypeCheck(self,inputFile):
        logging.info(169)
        if inputFile.endswith('.json') or inputFile.endswith('.csv') or inputFile.endswith('.tsv'):
            return True
       
    def metricsParsing(self):
        #This function is invoked if there is only one file. It could be a mistake/ it could be a file that contains the results for the dataset all in one file:
        #Like if you add the -o argument to running QuaMeter
            inputFile = self.possibleInputFiles[0]
            if inputFile.endswith('.json'):
                with open(inputFile) as f:
                    metrics = json.loads(f.read())
                metricsDf = pd.DataFrame(metrics)
                columnNames = []
                for ii in metricsDf["mzQC"]["runQuality"]:
                    for iii in ii["qualityParameters"]:
                        columnNames.append (iii["name"])
                PCAInput = pd.DataFrame(columns = columnNames)
                myPIArray = PCAInput.values
                tempVec = []
                for ii in metricsDf["mzQC"]["runQuality"]:
                    for iii in ii["qualityParameters"]:
                        try:
                            tempVec.append(iii["value"])
                        except:
                            logging.info("For "+ str(iii)+"there was no value.")
                            tempVec.append(0)
                            str1 = str(iii)
                            str1 = str1.join(str(inputFile))
                            globalVars.var.Nulvalues.append(str1)      
            
                myPIArray = np.vstack((myPIArray, tempVec)) 
                PCAInput = pd.DataFrame(myPIArray, columns=columnNames)
                metrics = PCAInput

            elif inputFile.endswith('.csv'):
                metrics = pd.DataFrame(pd.read_csv(inputFile, sep=","))
                metrics = metrics.fillna(value=0)

            elif inputFile.endswith('.tsv'):
                metrics = pd.DataFrame(pd.read_csv(inputFile, sep="\t"))
                metrics = metrics.fillna(value=0)
            
            globalVars.var.database.metrics.append(metrics)
            return

    def FileCheck(self, path):      
        #This function checks that the file exists and can be opened 
        try:
            return(open(path,'rb'))
        except IOError:
            return False
    
    def TrainingSetFileTypeCheck(self, inputFile):
          #Checks that the ID files are the right file type
          if inputFile.endswith('.pepXML') or inputFile.endswith('.txt') or inputFile.endswith('.mzid'):
            return True

          else:
            return False
            
    def TrainingSetFileMatchNames(self, TrainingSet):
        #This function checks that the for the ID files supplied for the training set, the 
        for i in range(0, len(TrainingSet.iloc[:, 0])):
            if(globalVars.var.database.metrics[0].iloc[i, 0] != TrainingSet.iloc[i, 0]):
                return False

    def CombineJSONs(self, training):
        if training:
            inputFiles = self.trainingsetQualityFiles
        else:
            inputFiles = self.possibleInputFiles
        
        AllMetricSizesDf = list()
        uniqueSizes = []
        for file in inputFiles:
            try:
                file1 = open(file, 'r')
                string1 = file1.read()
                metrics = json.loads(string1)
                filename = os.path.splitext(os.path.basename(file))[0]
            except:
                   return False
            metricsDf = pd.DataFrame(metrics)
            fileIndexInFiles = 0
            i=0
            while i < len(inputFiles):
                if file == inputFiles[i]:
                    fileIndexInFiles = i+1
                i=i+1
            QtCore.QMetaObject.invokeMethod(globalVars.var.UploadProgress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, fileIndexInFiles/(len(inputFiles)+1)*100))
            
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
               #             irtMetricsDF = pd.DataFrame(dfIndex = range(1, NumofTotalTransitions),columns = ["PeptideSequence", "PrecursorTargetMz", "RetentionTime", "ProductTargetMzs", "Intensities", "ActualMzs", "AverageMassError", "TotalMassError", "TotalMassErrorPpm", "AverageMassErrorPpm", "MeanIrtMassError","MaxIrtMassError","IrtPeptideFoundProportion","IrtPeptidesFound", "IrtSpread","IrtOrderedness"])
               #             index = 0
               #        if metricname != "IrtPeptides":
               #             for j in range(1,NumOfTransFound):
               #                 irtMetricsDF[metricname][j] = iii["value"]
               ##        else: 
                #            irtMetricsDF.loc[metricname] = iii["value"]* len(irtMetricsDF)






                    if "value" in iii:# This means that an empty value is never added to the dataframe
                        # Now we need to figure out in which dataframe it belongs:
                        #Something other than comprehensive:
                        if isinstance(iii["value"], collections.Sequence) and len(iii["value"]) > 1 and not isinstance(iii["value"],str):
                            ##########################Tuple:
                            
                            if isinstance(iii["value"][0], collections.Sequence) and not isinstance(iii["value"][0],str):# If prognosticator tuple:
                                if metricname== "IrtPeptides":
                                    #Deal with them here
                                    a=10
                                
                                if metricname== "MS1TIC":
                                    if 34333 not in uniqueSizes: # I chose a random number just to keep track
                                        uniqueSizes.append(34333)
                                        dfIndex = uniqueSizes.index(34333) 
                                        AllMetricSizesDf.append(pd.DataFrame(columns = [str("RT"+ filename),str("TIC"+ filename)]))
                                        AllMetricSizesDf[dfIndex][str("RT"+ filename)] = iii["value"][0]
                                        AllMetricSizesDf[dfIndex][ "TIC"+ filename] = iii["value"][1]                                        

                                    else:
                                        dfIndex = uniqueSizes.index(34333) 
                                        AllMetricSizesDf[dfIndex][str("RT"+ filename)] = iii["value"][0]
                                        AllMetricSizesDf[dfIndex][ "TIC"+ filename] = iii["value"][1]

                                if metricname== "MS2TIC":
                                    if 34444 not in uniqueSizes: # I chose a random number just to keep track
                                        uniqueSizes.append(34444)
                                        dfIndex = uniqueSizes.index(34444) 
                                        AllMetricSizesDf.append(pd.DataFrame(columns = [str("RT"+ filename),str("TIC"+ filename)]))
                                        AllMetricSizesDf[dfIndex][str("RT"+ filename)] = iii["value"][0]
                                        AllMetricSizesDf[dfIndex]["TIC"+ filename] = iii["value"][1]                                        

                                    else:
                                        dfIndex = uniqueSizes.index(34444) 
                                        AllMetricSizesDf[dfIndex][str("RT"+ filename)] = iii["value"][0]
                                        AllMetricSizesDf[dfIndex]["TIC"+ filename] = iii["value"][1]
                            
                                if metricname== "CombinedTIC":
                                    if 54555 not in uniqueSizes: # I chose a random number just to keep track
                                        uniqueSizes.append(54555)
                                        dfIndex = uniqueSizes.index(54555) 
                                        AllMetricSizesDf.append(pd.DataFrame(columns = [str("RT"+ filename),str("MS1TIC"+ filename),str("MS2TIC"+ filename)]))
                                        AllMetricSizesDf[dfIndex][str("RT"+ filename)] = iii["value"][0]
                                        AllMetricSizesDf[dfIndex][ "MS1TIC"+ filename] = iii["value"][1]
                                        AllMetricSizesDf[dfIndex][ "MS2TIC"+ filename] = iii["value"][2]                                        

                                    else:
                                        dfIndex = uniqueSizes.index(54555) 
                                        AllMetricSizesDf[dfIndex][str("RT"+ filename)] = iii["value"][0]
                                        AllMetricSizesDf[dfIndex][ "MS1TIC"+ filename] = iii["value"][1]
                                        AllMetricSizesDf[dfIndex][ "MS2TIC"+ filename] = iii["value"][2]
                            
                                if metricname== "MS2BPC":
                                    if 65646 not in uniqueSizes: # I chose a random number just to keep track
                                        uniqueSizes.append(65646)
                                        dfIndex = uniqueSizes.index(65646) 
                                        AllMetricSizesDf.append(pd.DataFrame(columns = [str("RT"+ filename),str("BPC"+ filename)]))
                                        AllMetricSizesDf[dfIndex][str("RT"+ filename)] = iii["value"][0]
                                        AllMetricSizesDf[dfIndex]["BPC"+ filename] = iii["value"][1]
                                        

                                    else:
                                        dfIndex = uniqueSizes.index(65646) 
                                        AllMetricSizesDf[dfIndex][str("RT"+ filename)] = iii["value"][0]
                                        AllMetricSizesDf[dfIndex]["BPC"+ filename] = iii["value"][1]

                                if metricname== "MS1BPC":
                                    if 77877 not in uniqueSizes: # I chose a random number just to keep track
                                        uniqueSizes.append(77877)
                                        dfIndex = uniqueSizes.index(77877) 
                                        AllMetricSizesDf.append(pd.DataFrame(columns = [str("RT"+ filename),str("MS1BPC"+ filename)]))
                                        AllMetricSizesDf[dfIndex][str("RT"+ filename)] = iii["value"][0]
                                        AllMetricSizesDf[dfIndex]["MS1BPC"+ filename] = iii["value"][1]
                                        

                                    else:
                                        dfIndex = uniqueSizes.index(77877) 
                                        AllMetricSizesDf[dfIndex][str("RT"+ filename)] = iii["value"][0]
                                        AllMetricSizesDf[dfIndex]["MS1BPC"+ filename] = iii["value"][1]

                               ################Tuple end        
                                       
                            else:
                                temp = []
                                for i in range(1,len(iii["value"])+1):
                                                stringstojoin = {filename,  str(i)}
                                                separator = "_"
                                                temp.append(separator.join(stringstojoin))
                                # DO we already have a DF for it:
                                if len(iii["value"]) in uniqueSizes: 
                                    dfIndex = uniqueSizes.index(len(iii["value"]))
                                    #Check if columnname already exists:
                                    if(metricname in AllMetricSizesDf[dfIndex].columns):
                                        # Check if its the first instance for this file, else we need to make new NA rows: The idea is that there should be dfIndex * iii["value"]
                                        if temp[0] not in AllMetricSizesDf[dfIndex]['Name']:# first instance of this file
                                            #create some NA's 
                                            for iiii in range(0,len(temp)):
                                                series = pd.Series()
                                                series.name = temp[iiii]
                                                AllMetricSizesDf[dfIndex]= AllMetricSizesDf[dfIndex].append(series)
                                                AllMetricSizesDf[dfIndex]["Name"].loc[str(temp[iiii])] = temp[iiii]
                                                AllMetricSizesDf[dfIndex][metricname].loc[temp[iiii]] = iii['value'][iiii]
                                                if metricname == "Target mz":
                                                    logging.info(AllMetricSizesDf[dfIndex]["Target mz"])
                                        else:
                                            for iiii in range(0,len(temp)):
                                                 AllMetricSizesDf[dfIndex][metricname].loc[temp[iiii]] = iii["value"][iiii]
                                   

                                    else:# We first need to create the column:

                                       # Check if the length of the other columns is still just one file else we need to fill with NAs:
                                       if temp[1] in AllMetricSizesDf[dfIndex]['Name']: #This file hs other values
                                           #Create some NA's
                                            AllMetricSizesDf[dfIndex][metricname] = pd.Series([np.repeat("NA",len(AllMetricSizesDf[dfIndex].index))])
                                            for iiii in range(0,len(temp)):
                                                 AllMetricSizesDf[dfIndex][metricname].loc[temp[iiii]] = iii["value"][iiii]

                                       else:#This is the first occurence of this file 
                                            for iiii in range(0,len(temp)-1):
                                                series = pd.Series()
                                                series.name = temp[iiii]
                                                AllMetricSizesDf[dfIndex] = AllMetricSizesDf[dfIndex].append(series)
                                                AllMetricSizesDf[dfIndex]['Name'].loc[temp[iiii]] = temp[iiii]
                                                AllMetricSizesDf[dfIndex][metricname].loc[temp[iiii]] = iii['value'][iiii]

                                else: # We create the df:
                                    uniqueSizes.append(len(iii["value"]))
                                    dfIndex = uniqueSizes.index(len(iii["value"]))
                                    AllMetricSizesDf.append(pd.DataFrame(columns = ['Name', metricname], index = temp))

                                    for iiii in range(0,len(temp)):
                                            AllMetricSizesDf[dfIndex].loc[temp[iiii]] = [temp[iiii] , iii['value'][iiii]]   
                        
                        elif 1 in uniqueSizes: 
                                 dfIndex = uniqueSizes.index(1)
                                #Check if columnname already exists:
                                 if(metricname in AllMetricSizesDf[dfIndex].columns):
                                    # Check if its the first instance for this file, in that case we need to make new NA rows: The idea is that there should be index * iii["value"]
                                    if filename not in AllMetricSizesDf[dfIndex]['Name']: # first instance of this file
                                        #create some NA's 
                                      series = pd.Series()
                                      series.name = filename
                                      AllMetricSizesDf[dfIndex] = AllMetricSizesDf[dfIndex].append(series)
                                      if filename in AllMetricSizesDf[dfIndex].index:
                                            AllMetricSizesDf[dfIndex]["Name"].loc[filename] = filename
                                            if isinstance(iii["value"], collections.Sequence) and len(iii["value"]) == 1:
                                                AllMetricSizesDf[dfIndex][metricname].loc[filename] = iii['value'][0]
                                            else:
                                                AllMetricSizesDf[dfIndex][metricname].loc[filename]  = iii['value']
                                             
                                      else:
                                          logging.info("Error creating filename row.")
                                    
                                    else: #this file has other values, but not this metric
                                        if isinstance(iii["value"], collections.Sequence) and len(iii["value"]) == 1:
                                                AllMetricSizesDf[dfIndex][metricname].loc[filename]  = iii['value'][0]
                                        else:
                                            if type(iii['value'])==list and len(iii['value'])==0:
                                                continue
                                            else:
                                                AllMetricSizesDf[dfIndex][metricname].loc[filename]  = iii['value'] 

                                 else:# We first need to create the column:

                                   # Check if the length of the other columns is still just one file else we need to fill with NAs:
                                   if filename not in AllMetricSizesDf[dfIndex].index: # FIrst value for this column and row
                                        AllMetricSizesDf[dfIndex][metricname] = pd.Series() 
                                        series = pd.Series()
                                        series.name = filename
                                        AllMetricSizesDf[dfIndex] = AllMetricSizesDf[dfIndex].append(series)
                                        if isinstance(iii["value"], collections.Sequence) and len(iii["value"]) == 1:
                                                AllMetricSizesDf[dfIndex][metricname].loc[filename]  = iii['value'][0]
                                        else:
                                                AllMetricSizesDf[dfIndex][metricname].loc[filename]  = iii['value']
                                   else:# filename exists, column name is new
                                        #if len(AllMetricSizesDf[dfIndex].index) >1:
                                            AllMetricSizesDf[dfIndex][metricname] = pd.Series() 
                                            if isinstance(iii["value"], collections.Sequence) and len(iii["value"]) == 1:
                                                if type(iii['value'][0]) != dict and type(iii['value'][0]) != list:
                                                    AllMetricSizesDf[dfIndex][metricname].loc[filename]  = iii['value'][0]
                                                else:
                                                    continue # No support for the irtpeptide double nested dictionaries at the moment.
                                            else:
                                                if type(iii['value'])==list and len(iii['value'])==0:
                                                    continue
                                                else:
                                                    AllMetricSizesDf[dfIndex][metricname].loc[filename]  = iii['value']
                                        

                                    
                        else: # We create need to create the comprehensive table:
                                uniqueSizes.append(1)
                                dfIndex = uniqueSizes.index(1)
                                AllMetricSizesDf.append(pd.DataFrame(columns = ['Name', metricname]))
                                series = pd.Series()
                                series.name = filename
                                AllMetricSizesDf[dfIndex]= AllMetricSizesDf[dfIndex].append(series)
                                AllMetricSizesDf[dfIndex]["Name"].loc[filename] = iii["name"]
                                AllMetricSizesDf[dfIndex][metricname].loc[filename] = iii['value']
        
        QtCore.QMetaObject.invokeMethod(globalVars.var.UploadProgress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int,100))
        if training:
            globalVars.var.database.trainingmetrics = AllMetricSizesDf
            globalVars.var.database.numericTrainingMetrics = globalVars.var.database.trainingmetrics
        else:
            globalVars.var.database.metrics = AllMetricSizesDf

    def CombineTSVs(self, training):
        if training:
            inputFiles = self.trainingsetQualityFiles
        else:
            inputFiles = self.possibleInputFiles
        
        df = pd.DataFrame()
        for file in inputFiles:
            df = df.append(pd.read_csv(file, sep="\t"))
            df = df.fillna(value=0)
            
        if "Filename" in df.columns:
            if ".mzML" in df["Filename"].iloc[0]:
                for file in range(0,len(df.index)):
                    df["Filename"].iloc[file] =   os.path.splitext(df["Filename"].iloc[file])[0]
                
            df.index = df["Filename"]    
        if training:
            globalVars.var.database.trainingmetrics.append(df)
            globalVars.var.database.numericTrainingMetrics = globalVars.var.database.trainingmetrics
        else:
            globalVars.var.database.metrics.append(df)

    def QuaMeterFileTypeCheck(self, inputFile):
        if inputFile.endswith('.wiff') or inputFile.endswith('.raw') or inputFile.endswith('.mzML'):
            return inputFile
        else:
            return False
     
    def GetQuaMeterInputFiles(self):
        FilesDir = QtWidgets. QFileDialog.getExistingDirectory(None, " Select the directory for QuaMeter input")
        if(FilesDir):
            return FilesDir

    def GetQuaMeterPath(self):
        QuaMeterPath,_ = QtWidgets.QFileDialog.getOpenFileName(None, "Please locate the QuaMeter exe on your system:", "", "exe files (*.exe)", 
                                                               options=
                                                               QtWidgets.QFileDialog.\
                                                                   Options())
        if(QuaMeterPath):
            return QuaMeterPath
            
    def SwaMeFileTypeCheck(self, inputFile):
        
        
        if inputFile.endswith('.mzML'):
            return inputFile
        else:
            return False
     
    def GetSwaMeInputFile(self):
        FilesDir= QtWidgets.QFileDialog.getExistingDirectory(None, " Select the directory containing files for SwaMe input")
        if(FilesDir):
            return FilesDir

    def GetSwaMePath(self):
        SwaMePath = ""
        if hasattr(globalVars.var, "assuranceDirectory"):
            if "SwaMe" in os.listdir(globalVars.var.assuranceDirectory):
                folderDir = os.path.join(globalVars.var.assuranceDirectory, "SwaMe")
                if "SwaMe.Console.exe" in os.listdir(folderDir):
                    SwaMePath = os.path.join(folderDir, "SwaMe.Console.exe")
        if len(SwaMePath)>2:
            return SwaMePath
        else:
            SwaMePath,_ = QtWidgets. QFileDialog.getOpenFileNames(None, "Please locate the SwaMe exe on your system:", "", "exe files (*.exe)", 
                                                                options=
                                                                QtWidgets.QFileDialog.\
                                                                    Options())
            if(SwaMePath):
                return SwaMePath[0]

    def GetIRTInputFile(self):
        file = QtWidgets. QFileDialog()
        file.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        possibleinputFile,_ = QtWidgets. QFileDialog.getOpenFileName(globalVars.var.tab, 
                                                               "Browse", "",
                                                               "TraML Files (*.TraML)", 
                                                               options=
                                                               QtWidgets.QFileDialog.\
                                                                   Options())
        if possibleinputFile:
            if possibleinputFile.endswith('.TraML') or possibleinputFile.endswith('.tsv') or possibleinputFile.endswith('.csv'):
                return possibleinputFile

   
        

