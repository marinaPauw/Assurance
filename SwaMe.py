import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import FileInput
import UI_MainWindow
from PyQt5.QtWidgets import QMessageBox
import os


class SwaMe():
    """description of class"""
    def setupUI(self, parent=None): 
        UI_MainWindow.Ui_MainWindow.EnableSwaMeArguments(self)

        #Arguments:
        SwaMe.MassTolerance = 5000 #Arbitrary value that I hope no one would ever choose
        SwaMe.RTTolerance = 5000
        SwaMe.Division = 5000
        SwaMe.Dir=False
        #SwaMe.IRT==False

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
            SwaMe.MassTolerance = UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.MTTextBox.text()
        if(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.RTTextBox.text()):
            SwaMe.RTTolerance = UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.RTTextBox.text()
        if(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.divisionTextBox.text()):
            SwaMe.Division = UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.divisionTextBox.text()
        if(UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.Dir.isChecked):
            SwaMe.Dir = True

        if  SwaMePath and SwaMe.File and SwaMe.Division!=5000 and SwaMe.MassTolerance!=5000:
            arguments = SwaMePath[0] + " -i " + SwaMe.File+ " --dir "+ str(SwaMe.Dir)+ " -d " +SwaMe.Division+ " -m " + SwaMe.MassTolerance

        elif  SwaMePath and SwaMe.File and SwaMe.Division!=5000:
            arguments = SwaMePath[0] + " -i " + SwaMe.File+ " --dir "+ str(SwaMe.Dir)+ " -d "+SwaMe.Division

        elif  SwaMePath and SwaMe.File:
            arguments = SwaMePath[0] + " -i " + SwaMe.File+ " --dir "+ str(SwaMe.Dir)
            
        SwaMe.process.start(arguments)

    @QtCore.pyqtSlot()
    def on_readyReadStandardOutput(self):
        text = SwaMe.process.readAllStandardOutput().data().decode()
        UI_MainWindow.Ui_MainWindow.tab.UploadFrame.rightFrame.textedit.append(text) 



            
        