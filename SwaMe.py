import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import FileInput
import UI_MainWindow
from PyQt5.QtWidgets import QMessageBox
import os
import glob
import DataPreparation
import time
import shutil


class SwaMe():
    """description of class"""
    def setupUI(self, parent=None): 
        UI_MainWindow.Ui_MainWindow.EnableSwaMeArguments(self)
        #SwaMe.Dir = ""
        SwaMe.Division = ''
        SwaMe.MassTolerance = ""
        SwaMe.RTTolerance = ""
        SwaMe.IRT = ''
        

        #Actions for when buttons are clicked:
        UI_MainWindow.Ui_MainWindow.SBrowseButton.clicked.connect(SwaMe.onSwaMeBrowseClicked)
        UI_MainWindow.Ui_MainWindow.SRUNButton.clicked.connect(SwaMe.onSwaMeRUNClicked)


    def onSwaMeBrowseClicked(self):
        #FileInput.BrowseWindow.__init__(FileInput.BrowseWindow, self)
        UI_MainWindow.Ui_MainWindow.Sfiles.show()
        SwaMe.Dir = FileInput.BrowseWindow.GetSwaMeInputFile(SwaMe)
        if(SwaMe.Dir):
                UI_MainWindow.Ui_MainWindow.SfileList.setText(SwaMe.Dir)
                try:
                    UI_MainWindow.Ui_MainWindow.assuranceDirectory = os.getcwd()
                    os.chdir(SwaMe.Dir)
                except:
                    print("Changing the directory didn't work.")

                
    def onSwaMeRUNClicked(self):
        
        
        SwaMe.Path = FileInput.BrowseWindow.GetSwaMePath(SwaMe)
        SwaMe.timestr = time.strftime("%Y%m%d-%H%M%S")
        os.chdir(SwaMe.Dir)
        
       
        #Find a file in the directory to be inputFile:
        paths = []
        files = []
        with os.scandir(SwaMe.Dir) as entries:
            for entry in entries:
                if entry.name.endswith(".mzML"):
                    paths.append(entry.path)
                    files.append(entry.name)
                    
                    
        SwaMe.StartProcess(self, files, 0, paths)
                    

    def StartProcess(self, files, file, paths):
                    arguments = ""
                    SwaMe.Division = ""
                    SwaMe.MassTolerance =""
                    SwaMe.RTTolerance = ""
                    SwaMe.IRT = ""
                    SwaMe.IRTolerance = ""
                    SwaMe.iRTminintensityTB = ""
                    SwaMe.iRTminpeptidesTB = ""
                    SwaMe.Minintensity = ""
        
                    
                    SwaMe.i = paths[file]
                    SwaMe.filename = files[file]
                    
                    SwaMe.process = QtCore.QProcess()
                    SwaMe.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
                    SwaMe.process.readyReadStandardOutput.connect(lambda: SwaMe.on_readyReadStandardOutput(self))
                    SwaMe.process.finished.connect(lambda: SwaMe.on_Finished(self, files, file, paths))
        
                    if len(SwaMe.i)<2:
                        QtWidgets.QMessageBox.warning(self, "Warning","Does the folder contain mzML's?")
                        SwaMe.onSwaMeBrowseClicked(self)
                        SwaMe.onSwaMeRUNClicked(self)
                    
                    if(UI_MainWindow.Ui_MainWindow.minintensityTB.text()):
                        SwaMe.Minintensity = arguments.join([" --minimumIntensity ", str(UI_MainWindow.Ui_MainWindow.minintensityTB.text())])
                    if(UI_MainWindow.Ui_MainWindow.MTTextBox.text()):
                        SwaMe.MassTolerance = arguments.join([" -m ", str(UI_MainWindow.Ui_MainWindow.MTTextBox.text())])
                    if(UI_MainWindow.Ui_MainWindow.RTTextBox.text()):
                        SwaMe.RTTolerance = arguments.join([" --rttolerance " , str(UI_MainWindow.Ui_MainWindow.RTTextBox.text())])
                    if(UI_MainWindow.Ui_MainWindow.divisionTextBox.text()):
                        SwaMe.Division = arguments.join([" -d " , str(UI_MainWindow.Ui_MainWindow.divisionTextBox.text())])
                    #if(UI_MainWindow.Ui_MainWindow.Dir.isChecked):
                    #    SwaMe.Dir = str.join(" -dir " , "true")
                    if(UI_MainWindow.Ui_MainWindow.IRTinputFile):
                        SwaMe.IRT = arguments.join([" -r " , str(UI_MainWindow.Ui_MainWindow.IRTinputFile)])
                        if(UI_MainWindow.Ui_MainWindow.iRTtoleranceTB):
                            SwaMe.IRTolerance = arguments.join([" --irttolerance " , str(UI_MainWindow.Ui_MainWindow.iRTtoleranceTB.text())])
                        if(UI_MainWindow.Ui_MainWindow.iRTminintensityTB):
                            SwaMe.iRTminintensityTB = arguments.join([" --irtminintensity " , str(UI_MainWindow.Ui_MainWindow.iRTminintensityTB.text())])
                        if(UI_MainWindow.Ui_MainWindow.iRTminpeptidesTB):
                            SwaMe.iRTminpeptidesTB = arguments.join([" --irtmintransitions " , str(UI_MainWindow.Ui_MainWindow.iRTminpeptidesTB.text())])
                        
                    SwaMe.outputFile = " -o "+ str(SwaMe.timestr) +"_"+ os.path.splitext(os.path.basename(SwaMe.filename))[0] + ".json"

                    if  SwaMe.Path and SwaMe.i:
                        arguments = QtCore.QDir.toNativeSeparators(SwaMe.Path) + " -i " + QtCore.QDir.toNativeSeparators(SwaMe.i) + SwaMe.Division + SwaMe.MassTolerance + SwaMe.RTTolerance + SwaMe.IRT+SwaMe.IRTolerance+SwaMe.iRTminintensityTB+ SwaMe.iRTminpeptidesTB + SwaMe.Minintensity+SwaMe.outputFile

                    SwaMe.process.start(arguments)

    @QtCore.pyqtSlot()
    def on_readyReadStandardOutput(self):
        text = SwaMe.process.readAllStandardOutput().data().decode()
        UI_MainWindow.Ui_MainWindow.Stextedit.append(text)
        
    @QtCore.pyqtSlot()
    def on_Finished(self, files, file, paths):
        if SwaMe.filename ==files[-1]:#If the last file:
                        
            files = []
            with os.scandir(SwaMe.Dir) as allfiles:
                for file in allfiles:
                    if file.name.endswith(".json"):
                        if file.name.startswith(SwaMe.timestr):
                            files.append(file.name)
            UI_MainWindow.Ui_MainWindow.metrics = FileInput.BrowseWindow.CombineJSONs(UI_MainWindow.Ui_MainWindow, files)
            #UI_MainWindow.Ui_MainWindow.metrics = FileInput.BrowseWindow.metricsParsing(inputFile)
            #UI_MainWindow.Ui_MainWindow.checkColumnLength(self)
            if hasattr(UI_MainWindow.Ui_MainWindow,"metrics"):
                UI_MainWindow.Ui_MainWindow.NumericMetrics = []
                FileInput.BrowseWindow.currentDataset = UI_MainWindow.Ui_MainWindow.metrics[0]
                FileInput.BrowseWindow.currentDataset = DataPreparation.DataPrep.ExtractNumericColumns(UI_MainWindow.Ui_MainWindow,
                                FileInput.BrowseWindow.currentDataset)
                FileInput.BrowseWindow.currentDataset = DataPreparation.DataPrep.RemoveLowVarianceColumns(
                                UI_MainWindow.Ui_MainWindow, FileInput.BrowseWindow.currentDataset)
                UI_MainWindow.Ui_MainWindow.NumericMetrics.append(FileInput.BrowseWindow.currentDataset)
                UI_MainWindow.Ui_MainWindow.DisableBrowseButtons(UI_MainWindow.Ui_MainWindow)
                UI_MainWindow.Ui_MainWindow.EnableAnalysisButtons(UI_MainWindow.Ui_MainWindow)
                QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab, "Message","SwaMe has finished successfully.")
            else:
                QtWidgets.QMessageBox.warning(self,"Error","An error occured and no metrics were created.")
                SwaMe.onSwaMeBrowseClicked(self)
                
        else:
            file = file+1
            SwaMe.StartProcess(self, files, file, paths)
                
        

            
        