import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import FileInput
import UI_MainWindow
import DataPreparation
from PyQt5.QtWidgets import QMessageBox
import os
import logging


class QuaMeter():
   
    def onQuaMeterBrowseClicked(self):
        #FileInput.BrowseWindow.__init__(FileInput.BrowseWindow, self)
        UI_MainWindow.Ui_MainWindow.files.show()
        QuaMeter.Dir = FileInput.BrowseWindow.GetQuaMeterInputFiles(QuaMeter)
        if(QuaMeter.Dir):
            UI_MainWindow.Ui_MainWindow.fileList.setText(QuaMeter.Dir)
            try:
                UI_MainWindow.Ui_MainWindow.assuranceDirectory = os.getcwd()
                os.chdir(QuaMeter.Dir)
            except:
                logging.info("Changing the directory didn't work.")
    
    def onQuaMeterRUNClicked(self):
        UI_MainWindow.Ui_MainWindow.DisableQuaMeterArguments(self)
        UI_MainWindow.Ui_MainWindow.DisableAnalysisButtons(self)
        if(UI_MainWindow.Ui_MainWindow.CLOTextBox.text()):
            QuaMeter.CLO = UI_MainWindow.Ui_MainWindow.CLOTextBox.text()
        if(UI_MainWindow.Ui_MainWindow.CUOTextBox.text()):
            QuaMeter.CUO = UI_MainWindow.Ui_MainWindow.CLOTextBox.text()
        #if(UI_MainWindow.Ui_MainWindow.cpusTextBox.text()):
        #    QuaMeter.CPU = UI_MainWindow.Ui_MainWindow.cpusTextBox.text()
       
        argument1 = "cd/d " + QuaMeter.Dir 
        
        QuaMeter.QuaMeterPath = FileInput.BrowseWindow.GetQuaMeterPath(QuaMeter)
        if QuaMeter.QuaMeterPath:
            files = []
            with os.scandir(QuaMeter.Dir) as entries:
                for entry in entries:
                    if entry.name.endswith(".mzML"):
                        files.append(entry.name)
            
            QuaMeter.StartProcess(self, files, 0)
                    

    def StartProcess(self, files, file):
        arguments = ""
        QuaMeter.errors = []
        QuaMeter.process = QtCore.QProcess()
        #arguments1 = " cd/d " + QuaMeter.Dir
        QuaMeter.process.finished.connect(lambda:QuaMeter.on_Finished(self, files, file))
        QuaMeter.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        QuaMeter.process.readyReadStandardOutput.connect(lambda: QuaMeter.on_readyReadStandardOutput(self))

        #cputext = 1
        #cpus = ""
        CUO = ''
        CLO = ""
       # if  UI_MainWindow.Ui_MainWindow.cpusTextBox.text(): 
        #    try:
        #        cputext = int(UI_MainWindow.Ui_MainWindow.cpusTextBox.text())
        #        if cputext>0 and cputext<6:
        #            cpus = " -cpus "+UI_MainWindow.Ui_MainWindow.cpusTextBox.text()
        #    except:
        #        QtWidgets.QMessageBox.warning(UI_MainWindow.Ui_MainWindow,"Error","cpus value could not be converted to integer and was ignored")
            
                
        if UI_MainWindow.Ui_MainWindow.CUOTextBox.text():
            CUO = " -ChromatogramMzUpperOffset " + UI_MainWindow.Ui_MainWindow.CUOTextBox.text()
        
        if UI_MainWindow.Ui_MainWindow.CLOTextBox.text():
            CLO = " -ChromatogramMzLowerOffset " + UI_MainWindow.Ui_MainWindow.CLOTextBox.text()
        
        QuaMeter.process.setWorkingDirectory(QtCore.QDir.toNativeSeparators(QuaMeter.Dir))
        logging.info("The current working directory is:", flush=True)
        logging.info(QuaMeter.process.workingDirectory(), flush=True)
        
        try:
            arguments2 = QtCore.QDir.toNativeSeparators(QuaMeter.QuaMeterPath)+" " +files[file] +" "  +  CUO + CLO +" -MetricsType idfree"
            logging.info("The following command line instruction was run:", flush=True)
            logging.info(arguments2, flush=True)
            QuaMeter.process.start(arguments2)        
        except IndexError:
            QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab, "Warning","No mzML files were found in the folder selected.")
            QuaMeter.onQuaMeterBrowseClicked(self)
            UI_MainWindow.Ui_MainWindow.EnableQuaMeterArguments(self)
        except Exception as ex:
            template = "An exception of type {0} occurred and QuaMeter run was not performed. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.info(message, flush=True)
            QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab, "Warning",message)
            UI_MainWindow.Ui_MainWindow.EnableBrowseButtons(self)
            UI_MainWindow.Ui_MainWindow.EnableQuaMeterArguments(self)
       
    @QtCore.pyqtSlot()
    def on_readyReadStandardOutput(self):
        text = QuaMeter.process.readAllStandardOutput().data().decode()
        UI_MainWindow.Ui_MainWindow.textedit.append(text)
        if "error" in text.lower():
            QuaMeter.errors.append(text)

    @QtCore.pyqtSlot()
    def on_Finished(self, files,file):
        if files[file] ==files[-1]:#If the last file:
            if len(QuaMeter.errors)>0:
                str1 = ""
                QtWidgets.QMessageBox(self, "Warning", "The following errors occurred: " + str1.join(QuaMeter.errors))
                
                
                
            dirpath = os.path.dirname(os.path.realpath(QuaMeter.Dir))
            ffiles = []
            for ffile in os.listdir(QuaMeter.Dir):  
                    if ffile.endswith("qual.tsv"):
                        ffiles.append(os.path.join(QuaMeter.Dir,ffile))
            UI_MainWindow.Ui_MainWindow.metrics = FileInput.BrowseWindow.CombineTSVs(UI_MainWindow.Ui_MainWindow, ffiles)
            #UI_MainWindow.Ui_MainWindow.metrics = FileInput.BrowseWindow.metricsParsing(inputFile)
            #UI_MainWindow.Ui_MainWindow.checkColumnLength(self)
            UI_MainWindow.Ui_MainWindow.NumericMetrics = []
            FileInput.BrowseWindow.currentDataset = UI_MainWindow.Ui_MainWindow.metrics[0]
            FileInput.BrowseWindow.currentDataset = DataPreparation.DataPrep.ExtractNumericColumns(self,
                            FileInput.BrowseWindow.currentDataset)
            FileInput.BrowseWindow.currentDataset = DataPreparation.DataPrep.RemoveLowVarianceColumns(self,
                            FileInput.BrowseWindow.currentDataset)
            UI_MainWindow.Ui_MainWindow.NumericMetrics.append(FileInput.BrowseWindow.currentDataset)
            UI_MainWindow.Ui_MainWindow.DisableBrowseButtons(self)
            UI_MainWindow.Ui_MainWindow.EnableAnalysisButtons(self)
            QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab, "Message","QuaMeter has finished.")
        else:
            file = file+1
            QuaMeter.StartProcess(self, files, file)
