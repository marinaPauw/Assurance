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
        UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton.clicked.connect(SwaMe.onSwaMeBrowseClicked)
        UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.SRUNButton.clicked.connect(SwaMe.onSwaMeRUNClicked)


    def onSwaMeBrowseClicked(self):
        #FileInput.BrowseWindow.__init__(FileInput.BrowseWindow, self)
        UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.files.show()
        SwaMe.File = FileInput.BrowseWindow.GetSwaMeInputFile(SwaMe)
        if(SwaMe.File):
                fname = os.path.basename(SwaMe.File)
                UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.SfileList.setText(fname)
    

                
    def onSwaMeRUNClicked(self):
        SwaMePath = FileInput.BrowseWindow.GetSwaMePath(SwaMe)
        SwaMe.process = QtCore.QProcess()
        SwaMe.process.setProcessChannelMode(QProcess.MergedChannels)
        SwaMe.process.readyReadStandardOutput.connect(lambda: SwaMe.on_readyReadStandardOutput(self))
        arguments = ""
        
        if(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.MTTextBox.text()):
            SwaMe.MassTolerance = arguments.join([" -m ", str(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.MTTextBox.text())])
        if(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.RTTextBox.text()):
            SwaMe.RTTolerance = arguments.join([" -rttolerance " , str(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.RTTextBox.text())])
        if(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.divisionTextBox.text()):
            SwaMe.Division = arguments.join([" -d " , str(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.divisionTextBox.text())])
        #if(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.Dir.isChecked):
        #    SwaMe.Dir = str.join(" -dir " , "true")
        if(UI_MainWindow.Ui_MainWindow.IRTinputFile):
            SwaMe.IRT = arguments.join([" -r " , str(UI_MainWindow.Ui_MainWindow.IRTinputFile)])

        if  SwaMePath and SwaMe.File:
            arguments = SwaMePath[0] + " -i " + SwaMe.File + SwaMe.Division + SwaMe.MassTolerance + SwaMe.RTTolerance + SwaMe.IRT  # + SwaMe.Dir 

        SwaMe.process.finished.connect(SwaMe.on_Finished)
        SwaMe.process.start(arguments)

    @QtCore.pyqtSlot()
    def on_readyReadStandardOutput(self):
        text = SwaMe.process.readAllStandardOutput().data().decode()
        UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.textedit.append(text)
        
    @QtCore.pyqtSlot()
    def on_Finished(self):
        dirpath = os.path.dirname(os.path.realpath(SwaMe.File))
        dirpath = os.path.join(dirpath, "QC_Results", )
        os.chdir(dirpath)
        files = []
        for file in glob.glob("*.json"):
            files.append(file)
        UI_MainWindow.Ui_MainWindow.metrics = FileInput.BrowseWindow.CombineJSONs(UI_MainWindow.Ui_MainWindow, files)
        #Now read in metrics:
        
        for dataTable in UI_MainWindow.Ui_MainWindow.metrics:
            DataPreparation.DataPrep.ExtractNumericColumns(dataTable)
            DataPreparation.DataPrep.RemoveLowVarianceColumns(UI_MainWindow.Ui_MainWindow)
            UI_MainWindow.Ui_MainWindow.EnableAnalysisButtons(self)

            
        