import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import MainParser
import Main
import PyQt5.QtWidgets 
import os
from Datasets import Datasets
import time
import logging
import globalVars


class SwaMe():
    """description of class"""
    def setupUI(self, parent=None): 
        globalVars.var.EnableSwaMeArguments(self)
        #SwaMe.Dir = ""
        SwaMe.Division = ''
        SwaMe.MassTolerance = ""
        SwaMe.RTTolerance = ""
        SwaMe.IRT = ''
        

        #Actions for when buttons are clicked:
        globalVars.var.SBrowseButton.clicked.connect(SwaMe.onSwaMeBrowseClicked)
        globalVars.var.SRUNButton.clicked.connect(SwaMe.onSwaMeRUNClicked)


    def onSwaMeBrowseClicked(self):
        globalVars.var.Sfiles.show()
        SwaMe.Dir = MainParser.Parser.GetSwaMeInputFile(SwaMe)
        if(SwaMe.Dir):
                globalVars.var.SfileList.setText(SwaMe.Dir)
                try:
                    globalVars.var.assuranceDirectory = os.getcwd()
                    os.chdir(SwaMe.Dir)
                except:
                    logging.info("Changing the directory didn't work.")

                
    def onSwaMeRUNClicked(self):
        globalVars.var.DisableSwaMeArguments(self)
        globalVars.var.DisableAnalysisButtons(self)
        SwaMe.Path = MainParser.Parser.GetSwaMePath(SwaMe)
        if SwaMe.Path:
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
            try:        
                    
                    arguments = ""
                    SwaMe.Division = ""
                    SwaMe.MassTolerance =""
                    SwaMe.RTTolerance = ""
                    SwaMe.IRT = ""
                    SwaMe.IRTolerance = ""
                    SwaMe.iRTminintensityTB = ""
                    SwaMe.iRTminpeptidesTB = ""
                    SwaMe.Minintensity = ""
                    SwaMe.lastfile = ""
                    
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
                    
                    if(globalVars.var.minintensityTB.text()):
                        SwaMe.Minintensity = arguments.join([" --minimumIntensity ", str(globalVars.var.minintensityTB.text())])
                    if(globalVars.var.MTTextBox.text()):
                        SwaMe.MassTolerance = arguments.join([" -m ", str(globalVars.var.MTTextBox.text())])
                    if(globalVars.var.RTTextBox.text()):
                        SwaMe.RTTolerance = arguments.join([" --rttolerance " , str(globalVars.var.RTTextBox.text())])
                    if(globalVars.var.divisionTextBox.text()):
                        SwaMe.Division = arguments.join([" -d " , str(globalVars.var.divisionTextBox.text())])
                    #if(globalVars.var.Dir.isChecked):
                    #    SwaMe.Dir = str.join(" -dir " , "true")
                    if(globalVars.var.IRTinputFile):
                        SwaMe.IRT = arguments.join([" -r " , str(globalVars.var.IRTinputFile)])
                        if(globalVars.var.iRTtoleranceTB.text()):
                            SwaMe.IRTolerance = arguments.join([" --irttolerance " , str(globalVars.var.iRTtoleranceTB.text())])
                        if(globalVars.var.iRTminintensityTB.text()):
                            SwaMe.iRTminintensityTB = arguments.join([" --irtminintensity " , str(globalVars.var.iRTminintensityTB.text())])
                        if(globalVars.var.iRTminpeptidesTB.text()):
                            SwaMe.iRTminpeptidesTB = arguments.join([" --irtmintransitions " , str(globalVars.var.iRTminpeptidesTB.text())])
                        
                    SwaMe.outputFile = " -o "+ str(SwaMe.timestr) +"_"+ os.path.splitext(os.path.basename(SwaMe.filename))[0] + ".json"

                    if  SwaMe.Path and SwaMe.i:
                        arguments = QtCore.QDir.toNativeSeparators(SwaMe.Path) + " -i " + QtCore.QDir.toNativeSeparators(SwaMe.i) + SwaMe.Division + SwaMe.MassTolerance + SwaMe.RTTolerance + SwaMe.IRT+SwaMe.IRTolerance+SwaMe.iRTminintensityTB+ SwaMe.iRTminpeptidesTB + SwaMe.Minintensity+SwaMe.outputFile

                    SwaMe.process.start(arguments)
                    
            except IndexError:
                QtWidgets.QMessageBox.about(globalVars.var.tab, "Warning","No mzML files were found in the folder selected.")
                SwaMe.onSwaMeBrowseClicked(self)
                globalVars.var.EnableQuaMeterArguments(self)
            except Exception as ex:
                template = "An exception of type {0} occurred and SwaMe run was not performed. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                logging.info(message, flush=True)
                QtWidgets.QMessageBox.about(globalVars.var.tab, "Warning",message)
                globalVars.var.EnableBrowseButtons(self)
                globalVars.var.EnableQuaMeterArguments(self)

    @QtCore.pyqtSlot()
    def on_readyReadStandardOutput(self):
        text = SwaMe.process.readAllStandardOutput().data().decode()
        globalVars.var.Stextedit.append(text)
        if "loading file" in text.lower():
            SwaMe.lastfile = text
        if "error" in text.lower():
            fullMessage = "For file: "+ SwaMe.lastfile+" - " +text
            globalVars.var.errors.append(fullMessage)
        
    @QtCore.pyqtSlot()
    def on_Finished(self, files, file, paths):
        if SwaMe.filename ==files[-1]:#If the last file:
            if len(globalVars.var.errors)>0:
                str1 = ""
                QtWidgets.QMessageBox(self, "Warning", "The following errors occurred: " + str1.join(globalVars.var.errors))
                           
            #Grab all the mzQC files SwaMe created:
            files = []
            with os.scandir(SwaMe.Dir) as allfiles:
                for file in allfiles:
                    if file.name.endswith(".json"):
                        if file.name.startswith(SwaMe.timestr):
                            files.append(file.name)
            Parser = MainParser.Parser()
            Parser.CombineJSONs(False)
            #Datasets.metrics = MainParser.Parser.metricsParsing(inputFile)
            #globalVars.var.checkColumnLength(self)
            if hasattr(globalVars.var.database,"metrics"):
                if len(globalVars.var.database.metrics)>0:
                    globalVars.var.database.ExtractNumericColumns(False)
                    globalVars.var.database.RemoveLowVarianceColumns(
                                    False)

                    globalVars.var.DisableBrowseButtons(globalVars.var)
                    globalVars.var.EnableAnalysisButtons(globalVars.var)
                    QtWidgets.QMessageBox.about(globalVars.var.tab, "Message","SwaMe has finished successfully.")
                else:
                    QtWidgets.QMessageBox.warning(self,"Error","An error occured and no metrics were created.")
                    SwaMe.onSwaMeBrowseClicked(self)            
            else:
                QtWidgets.QMessageBox.warning(self,"Error","An error occured and no metrics were created.")
                SwaMe.onSwaMeBrowseClicked(self)
                
        else:
            file = file+1
            SwaMe.StartProcess(self, files, file, paths)
                
        

            
        