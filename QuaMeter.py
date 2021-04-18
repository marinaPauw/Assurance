import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import MainParser
import Main
from PyQt5.QtWidgets import QMessageBox
from Datasets import Datasets
import os
import logging
import globalVars


class QuaMeter():
   
    def onQuaMeterBrowseClicked(self):
        globalVars.var.files.show()
        QuaMeter.Dir = globalVars.var.parser.GetQuaMeterInputFiles(QuaMeter)
        if(QuaMeter.Dir):
            globalVars.var.fileList.setText(QuaMeter.Dir)
            try:
                globalVars.var.assuranceDirectory = os.getcwd()
                os.chdir(QuaMeter.Dir)
            except:
                logging.info("Changing the directory didn't work.")
    
    def onQuaMeterRUNClicked(self):
        globalVars.var.DisableQuaMeterArguments(self)
        globalVars.var.DisableAnalysisButtons(self)
        if(globalVars.var.CLOTextBox.text()):
            QuaMeter.CLO = globalVars.var.CLOTextBox.text()
        if(globalVars.var.CUOTextBox.text()):
            QuaMeter.CUO = globalVars.var.CLOTextBox.text()
        #if(globalVars.var.cpusTextBox.text()):
        #    QuaMeter.CPU = globalVars.var.cpusTextBox.text()
       
        argument1 = "cd/d " + QuaMeter.Dir 
        
        QuaMeter.QuaMeterPath = MainParser.Parser.GetQuaMeterPath(QuaMeter)
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
       # if  globalVars.var.cpusTextBox.text(): 
        #    try:
        #        cputext = int(globalVars.var.cpusTextBox.text())
        #        if cputext>0 and cputext<6:
        #            cpus = " -cpus "+globalVars.var.cpusTextBox.text()
        #    except:
        #        QtWidgets.QMessageBox.warning(globalVars.var,"Error","cpus value could not be converted to integer and was ignored")
            
                
        if globalVars.var.CUOTextBox.text():
            CUO = " -ChromatogramMzUpperOffset " + globalVars.var.CUOTextBox.text()
        
        if globalVars.var.CLOTextBox.text():
            CLO = " -ChromatogramMzLowerOffset " + globalVars.var.CLOTextBox.text()
        
        QuaMeter.process.setWorkingDirectory(QtCore.QDir.toNativeSeparators(QuaMeter.Dir))
        logging.info("The current working directory is:", flush=True)
        logging.info(QuaMeter.process.workingDirectory(), flush=True)
        
        try:
            arguments2 = QtCore.QDir.toNativeSeparators(QuaMeter.QuaMeterPath)+" " +files[file] +" "  +  CUO + CLO +" -MetricsType idfree"
            logging.info("The following command line instruction was run:", flush=True)
            logging.info(arguments2, flush=True)
            QuaMeter.process.start(arguments2)        
        except IndexError:
            QtWidgets.QMessageBox.about(globalVars.var.tab, "Warning","No mzML files were found in the folder selected.")
            QuaMeter.onQuaMeterBrowseClicked(self)
            globalVars.var.EnableQuaMeterArguments(self)
        except Exception as ex:
            template = "An exception of type {0} occurred and QuaMeter run was not performed. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.info(message, flush=True)
            QtWidgets.QMessageBox.about(globalVars.var.tab, "Warning",message)
            globalVars.var.EnableBrowseButtons(self)
            globalVars.var.EnableQuaMeterArguments(self)
       
    @QtCore.pyqtSlot()
    def on_readyReadStandardOutput(self):
        text = QuaMeter.process.readAllStandardOutput().data().decode()
        globalVars.var.textedit.append(text)
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
            globalVars.var.parser.CombineTSVs(globalVars.var, ffiles)
            
            #We will now prepare the data for further analysis.t
            globalVars.var.database.ExtractNumericColumns(False)
            globalVars.var.database.RemoveLowVarianceColumns(False)

            globalVars.var.DisableBrowseButtons(self)
            globalVars.var.EnableAnalysisButtons(self)
            QtWidgets.QMessageBox.about(globalVars.var.tab, "Message","QuaMeter has finished.")
        else:
            file = file+1
            QuaMeter.StartProcess(self, files, file)
