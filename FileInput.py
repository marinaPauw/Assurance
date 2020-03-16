import sys
from PyQt5 import QtWidgets
import datetime
import UI_MainWindow
import DataPreparation
import pandas as pd
import numpy as np
import os
import collections
import json
import DataPreparation





class BrowseWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.title = "Load file"
        UI_MainWindow.Ui_MainWindow.EnableAnalysisButtons(self)

    def GetInputFile(self):
        files = QtWidgets. QFileDialog()
        files.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        possibleinputFiles,_ = QtWidgets. QFileDialog.getOpenFileNames(UI_MainWindow.Ui_MainWindow.tab, 
                                                               "Browse", "",
                                                               "All Files (*)", 
                                                               options=
                                                               QtWidgets.QFileDialog.\
                                                                   Options())
        if(possibleinputFiles):
            if(len(possibleinputFiles) > 1):
                justJSONFiles = True
                for possiblefile in possibleinputFiles:
                   if(".json" not in possiblefile):
                       justJSONFiles = False
                if not justJSONFiles :
                    QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab,
                                      "Error:" ,"You may select multiple mzQC files to combine into one table, but you may not select multiple files of any other type.")
                    UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)

                if(justJSONFiles==True):
                   inputFiles = possibleinputFiles
                   UI_MainWindow.Ui_MainWindow.metrics =  \
                       BrowseWindow.CombineJSONs(
                           UI_MainWindow.Ui_MainWindow, inputFiles)
                   UI_MainWindow.Ui_MainWindow.NumericMetrics = []
                   for i in range(1,len(UI_MainWindow.Ui_MainWindow.metrics)):
                       #UI_MainWindow.Ui_MainWindow.metrics.set_dfIndex(
                        #   UI_MainWindow.Ui_MainWindow.metrics.iloc[:,0])
                       BrowseWindow.currentDataset = UI_MainWindow.Ui_MainWindow.metrics[0]
                       DataPreparation.DataPrep.ExtractNumericColumns(self,
                           BrowseWindow.currentDataset)
                       DataPreparation.DataPrep.RemoveLowVarianceColumns(
                           UI_MainWindow.Ui_MainWindow)
                       UI_MainWindow.Ui_MainWindow.NumericMetrics.append(BrowseWindow.currentDataset)
                   str1 = " " 
                   UI_MainWindow.Ui_MainWindow.tab.UploadFrame.filename.setText(str1.join(inputFiles))
                   UI_MainWindow.Ui_MainWindow.DisableBrowseButtons(UI_MainWindow.Ui_MainWindow)
            else:
                possibleinputFile = possibleinputFiles[0]
                inputFile = BrowseWindow.fileTypeCheck(self, possibleinputFile)
                if(inputFile):
                    counter = inputFile.count('.') 
                    if(counter==1):# .mzML
                         BrowseWindow.datasetname, throw = inputFile.split('.')
                    elif(counter==2):#If the program lists .wiff.scan
                         BrowseWindow.datasetname,throw,throw = inputFile.split('.')
                    elif(counter==3):
                         BrowseWindow.datasetname,throw,throw,throw = inputFile.split('.')
                    else:
                         BrowseWindow.datasetname = inputFile
                    UI_MainWindow.Ui_MainWindow.tab.UploadFrame.filename.setText("   " + inputFile + "  ")
                    return inputFile
   
    def GetTrainingSetFile(self):
        possibleInputFile, _ =QtWidgets. QFileDialog.getOpenFileName(
            UI_MainWindow.Ui_MainWindow.tab,"Select a file from which to create the training set:", "","All Files (*)", options = QtWidgets.QFileDialog.Options())
        if(possibleInputFile):
            TrainingSetFile = BrowseWindow.TrainingSetFileTypeCheck(self, possibleInputFile)
            if(TrainingSetFile):
                return TrainingSetFile
    
    def fileTypeCheck(self,inputFile):
        if inputFile.endswith('.json') or inputFile.endswith('.csv') or inputFile.endswith('.tsv'):
            return inputFile
        else:
            QtWidgets.QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab,
                              "Message from Assurance: ", "Error: File type incorrect. Please load a.json, .tsv or .csv file. Also please ensure that the decimals are separated by '.'.")
            UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)

    def metricsParsing(self,inputFile):
       try:
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
                  tempVec.append(iii["value"])
        
            myPIArray = np.vstack((myPIArray, tempVec)) 
            PCAInput = pd.DataFrame(myPIArray, columns=columnNames)
            metrics = PCAInput
            if(metrics.iloc[:, 0].count() < 2) :
                QtWidgets.QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab,"Error:", 
                                  "There are not enough samples in your file to conduct analysis. Please choose another file.")
                UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
            return metrics

        elif inputFile.endswith('.csv'):
            metrics = pd.DataFrame(pd.read_csv(inputFile, sep=","))
            if(metrics.iloc[:, 0].count() < 2):
                QtWidgets.QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab, "Error:",
                                  "There are not enough samples in your file to conduct analysis. Please choose another file.")
                UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
            return metrics

        elif inputFile.endswith('.tsv'):
            metrics = pd.DataFrame(pd.read_csv(inputFile, sep="\t"))
            if(metrics.iloc[:, 0].count() < 2):
                QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab, "Error:",
                                  "There are not enough samples in your file to conduct analysis. Please choose another file.")
                UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
            return metrics


       except json.decoder.JSONDecodeError:
            QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab,"Message from Assurance: ", "This file does not contain data in the correct format. Please load a different file.")
            UI_MainWindow.Ui_MainWindow.onBrowseClicked(
                UI_MainWindow.Ui_MainWindow)

    def FileCheck(self, path):       
        try:
            return(open(path,'rb'))
        except IOError:
            QtWidgets.QMessageBox.warning(UI_MainWindow.Ui_MainWindow, "Message from Assurance: ",
                              "Error loading file...")
            return 0
    
    def TrainingSetFileTypeCheck(self, inputFile):
          if inputFile.endswith('.csv') or inputFile.endswith('.tsv'):
            return inputFile

          else:
            QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab, "Message from Assurance: ", "Error: File type incorrect. Please load a .json, .tsv or .csv file. Also please ensure that the decimals are separated by '.'.")
            UI_MainWindow.Ui_MainWindow.onLongitudinalClicked(UI_MainWindow.Ui_MainWindow)
            
    def TrainingSetParse(self,inputFile):
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
               QtWidgets.QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab, "Error:",
                                  "The first column of the  file does not match that of the quality metrics input file. Try again.")
               UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)

    def CombineJSONs(self, inputFiles):
        AllMetricSizesDf = list()
        uniqueSizes = []
        for file in inputFiles:
            try:
                file1 = open(file, 'r')
                string1 = file1.read()
                metrics = json.loads(string1)
                filename = os.path.splitext(os.path.basename(file))[0]
                #Input reading of jsonfiles here:
            except:
                    QtWidgets.QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab,"Error:", 
                                            "Upload failed. Please check the content of the files and try again.")
                    UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
            metricsDf = pd.DataFrame(metrics)
            # Create dataframes - for SwaMe we need one for comprehensive, one for swath, one for rt, one for quartiles, one for quantiles
            fileIndexInFiles = 0
            i=0
            while i < len(inputFiles):
                if file == inputFiles[i]:
                    fileIndexInFiles = i+1
                i=i+1

            UI_MainWindow.Ui_MainWindow.tab.AnalysisFrame.UploadProgress.setValue(fileIndexInFiles/len(inputFiles)*100)

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
                                                    print(AllMetricSizesDf[dfIndex]["Target mz"])
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
                                          print("Error creating filename row.")
                                    
                                    else: #this file has other values, but not this metric
                                        if isinstance(iii["value"], collections.Sequence) and len(iii["value"]) == 1:
                                                AllMetricSizesDf[dfIndex][metricname].loc[filename]  = iii['value'][0]
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
                                            for y in range(0,len(AllMetricSizesDf[dfIndex]['Name'])):
                                                if AllMetricSizesDf[dfIndex]['Name'].index[y] == filename:
                                                    fileIndex = y
                                            if isinstance(iii["value"], collections.Sequence) and len(iii["value"]) == 1:
                                                AllMetricSizesDf[dfIndex].loc[[filename], [metricname]]  = iii['value'][0]
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
        
        print(AllMetricSizesDf[0])
        return AllMetricSizesDf


    def QuaMeterFileTypeCheck(self, inputFile):
        if inputFile.endswith('.wiff') or inputFile.endswith('.raw') or inputFile.endswith('.mzML'):
            return inputFile
        else:
             QtWidgets.QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab,
                              "Message from Assurance: ", "Error: File type incorrect. Please load a .mzML, .wiff or .raw file.")
             UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
     
    def GetQuaMeterInputFiles(self):
        possibleinputFiles,_ = QtWidgets. QFileDialog.getOpenFileNames(None, " Files for QuaMeter input", "", "mzML files (*.mzML)", 
                                                               options=
                                                               QtWidgets.QFileDialog.\
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
                                                               QtWidgets.QFileDialog.\
                                                                   Options())
        if(QuaMeterPath):
            return QuaMeterPath

    def SwaMeFileTypeCheck(self, inputFile):
        if inputFile.endswith('.mzML'):
            return inputFile
        else:
             QtWidgets.QMessageBox.warning(UI_MainWindow.Ui_MainWindow.tab,
                              "Message from Assurance: ", "Error: File type incorrect. Please load a .mzML file.")
             UI_MainWindow.Ui_MainWindow.onBrowseClicked(UI_MainWindow.Ui_MainWindow)
     
    def GetSwaMeInputFile(self):
        possibleinputFile,_ = QtWidgets. QFileDialog.getOpenFileName(None, " Input File for SwaMe:", "", "mzML files (*.mzML)", 
                                                               options=
                                                               QtWidgets.QFileDialog.\
                                                                   Options())
        if(possibleinputFile):
                inputFile= BrowseWindow.SwaMeFileTypeCheck(self, possibleinputFile)

        if(inputFile):
            return inputFile

    def GetSwaMePath(self):
        SwaMePath,_ = QtWidgets. QFileDialog.getOpenFileNames(None, "Please locate the SwaMe exe on your system:", "", "exe files (*.exe)", 
                                                               options=
                                                               QtWidgets.QFileDialog.\
                                                                   Options())
        if(SwaMePath):
            return SwaMePath

    def GetIRTInputFile(self):
        file = QtWidgets. QFileDialog()
        file.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        possibleinputFile,_ = QtWidgets. QFileDialog.getOpenFileName(UI_MainWindow.Ui_MainWindow.tab, 
                                                               "Browse", "",
                                                               "TraML Files (*.TraML)", 
                                                               options=
                                                               QtWidgets.QFileDialog.\
                                                                   Options())
        if possibleinputFile:
            if possibleinputFile.endswith('.TraML') or possibleinputFile.endswith('.tsv') or possibleinputFile.endswith('.csv'):
                return possibleinputFile

    def find_indices(self, lst, condition):
            return [i for i, elem in enumerate(lst) if condition(elem)]
   
        


