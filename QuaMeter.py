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


class QuaMeter():
   
    def onQuaMeterBrowseClicked(self):
        #FileInput.BrowseWindow.__init__(FileInput.BrowseWindow, self)
        UI_MainWindow.Ui_MainWindow.files.show()
        QuaMeter.Dir = FileInput.BrowseWindow.GetQuaMeterInputFiles(QuaMeter)
        if(QuaMeter.Dir):
            UI_MainWindow.Ui_MainWindow.fileList.setText(QuaMeter.Dir)
    
    def onQuaMeterRUNClicked(self):
        if(UI_MainWindow.Ui_MainWindow.CLOTextBox.text()):
            QuaMeter.CLO = UI_MainWindow.Ui_MainWindow.CLOTextBox.text()
        if(UI_MainWindow.Ui_MainWindow.CUOTextBox.text()):
            QuaMeter.CUO = UI_MainWindow.Ui_MainWindow.CLOTextBox.text()
        if(UI_MainWindow.Ui_MainWindow.cpusTextBox.text()):
            QuaMeter.CPU = UI_MainWindow.Ui_MainWindow.cpusTextBox.text()
       
        argument1 = "cd/d " + QuaMeter.Dir 
        
        QuaMeterPath = FileInput.BrowseWindow.GetQuaMeterPath(QuaMeter)
        
        QuaMeter.process = QtCore.QProcess()
        #arguments1 = " cd/d " + QuaMeter.Dir
        QuaMeter.process.finished.connect(QuaMeter.on_Finished)
        QuaMeter.process.waitForFinished()
        QuaMeter.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        QuaMeter.process.readyReadStandardOutput.connect(lambda: QuaMeter.on_readyReadStandardOutput(self))

        cpus = ""
        CUO = ''
        CLO = ""
        if  UI_MainWindow.Ui_MainWindow.cpusTextBox.text() and UI_MainWindow.Ui_MainWindow.cpusTextBox.text()>0 and UI_MainWindow.Ui_MainWindow.cpusTextBox.text()<6:
            cpus = " -cpus "+UI_MainWindow.Ui_MainWindow.cpusTextBox.text()
        
        if UI_MainWindow.Ui_MainWindow.CUOTextBox.text():
            CUO = " -ChromatogramMzUpperOffset " + UI_MainWindow.Ui_MainWindow.CUOTextBox.text()
        
        if UI_MainWindow.Ui_MainWindow.CLOTextBox.text():
            CLO = " -ChromatogramMzLowerOffset " + UI_MainWindow.Ui_MainWindow.CLOTextBox.text()
        
        QuaMeter.process.setWorkingDirectory(QtCore.QDir.toNativeSeparators(QuaMeter.Dir))
        #QuaMeter.process.start(" cd/d " + os.path.dirname(QuaMeter.File))
        arguments2 = QtCore.QDir.toNativeSeparators(QuaMeterPath)+ " *.mzML " +" " +cpus +  CUO + CLO +" -MetricsType idfree"
        QuaMeter.process.start(arguments2)
       
    @QtCore.pyqtSlot()
    def on_readyReadStandardOutput(self):
        text = QuaMeter.process.readAllStandardOutput().data().decode()
        UI_MainWindow.Ui_MainWindow.textedit.append(text)

    @QtCore.pyqtSlot()
    def on_Finished(self):
        dirpath = os.path.dirname(os.path.realpath(QuaMeter.Dir))
        files = []
        for root, dirs, allfiles in os.walk(dirpath):  
            for file in allfiles:
                if file.endswith("qual.tsv"):
                    files.append(os.path.join(root,file))
        UI_MainWindow.Ui_MainWindow.metrics = FileInput.BrowseWindow.CombineTSVs(UI_MainWindow.Ui_MainWindow, files)
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
        QtWidgets.QMessageBox.about(UI_MainWindow.Ui_MainWindow.tab, "Message","QuaMeter has finished successfully.")

