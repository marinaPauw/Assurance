import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import FileInput
import UI_MainWindow
from PyQt5.QtWidgets import QMessageBox
import os


class QuaMeter():
    """description of class"""
    def setupUI(self, parent=None): 
        #Setting up the window:
        UI_MainWindow.Ui_MainWindow.EnableQuaMeterArguments(self)
 #Arguments:
        if(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.CLOTextBox.text()):
            QuaMeter.CLO = UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.CLOTextBox.text()
        if(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.CUOTextBox.text()):
            QuaMeter.CUO = UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.CLOTextBox.text()
        if(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.cpusTextBox.text()):
            QuaMeter.CPU = UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.cpusTextBox.text()

        #Actions for when buttons are clicked:
        UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.BrowseButton.clicked.connect(QuaMeter.onQuaMeterBrowseClicked)
        UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.RUNButton.clicked.connect(QuaMeter.onQuaMeterRUNClicked)


    def onQuaMeterBrowseClicked(self):
        #FileInput.BrowseWindow.__init__(FileInput.BrowseWindow, self)
        UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.files.show()
        QuaMeter.File = FileInput.BrowseWindow.GetQuaMeterInputFiles(QuaMeter)
        if(QuaMeter.File):
            for file in QuaMeter.File:
                fname = os.path.basename(file)
                UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.fileList.setText(fname)
    
    def onQuaMeterRUNClicked(self):
        QuaMeterPath = FileInput.BrowseWindow.GetQuaMeterPath(QuaMeter)
        QuaMeter.process = QtCore.QProcess()
        QuaMeter.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        QuaMeter.process.readyReadStandardOutput.connect(lambda: QuaMeter.on_readyReadStandardOutput(self))
        QuaMeter.process.finished.connect(QuaMeter.on_Finished)
        if  UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.cpusTextBox.text() and UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.CUOTextBox.text() and UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.CLOTextBox.text():
            rstring = "r"
            QuaMeter.process.start(rstring.join(QuaMeterPath), 
                ["",QuaMeter.File,"-cpus", UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.cpusTextBox.text(), "-ChromatogramMzUpperOffset", UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.CUOTextBox.text(), "-ChromatogramMzLowerOffset", UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.CLOTextBox.text()])


    @QtCore.pyqtSlot()
    def on_readyReadStandardOutput(self):
        text = QuaMeter.process.readAllStandardOutput().data().decode()
        UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.textedit.append(text)

    @QtCore.pyqtSlot()
    def on_Finished(self):
        dirpath = os.path.dirname(os.path.realpath(QuaMeter.File))
        dirpath = os.path.join(dirpath, "QC_Results", )
        os.chdir(dirpath)
        files = []
        for root, dirs, allfiles in os.walk(dirpath):  
            for file in allfiles:
                if file.endswith(".json"):
                    files.append(os.path.join(root,file))
        UI_MainWindow.Ui_MainWindow.metrics = FileInput.BrowseWindow.CombineJSONs(UI_MainWindow.Ui_MainWindow, files)
        #UI_MainWindow.Ui_MainWindow.metrics = FileInput.BrowseWindow.metricsParsing(inputFile)
        #UI_MainWindow.Ui_MainWindow.checkColumnLength(self)
        UI_MainWindow.Ui_MainWindow.NumericMetrics = []
        FileInput.BrowseWindow.currentDataset = UI_MainWindow.Ui_MainWindow.metrics[0]
        DataPreparation.DataPrep.ExtractNumericColumns(
                           FileInput.BrowseWindow.currentDataset)
        DataPreparation.DataPrep.RemoveLowVarianceColumns(
                           UI_MainWindow.Ui_MainWindow)
        UI_MainWindow.Ui_MainWindow.NumericMetrics.append(FileInput.BrowseWindow.currentDataset)
        UI_MainWindow.Ui_MainWindow.DisableBrowseButtons(UI_MainWindow.Ui_MainWindow)
        UI_MainWindow.Ui_MainWindow.EnableAnalysisButtons(UI_MainWindow.Ui_MainWindow)

