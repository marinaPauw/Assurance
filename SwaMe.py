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
        #Setting up the window:
        SwaMe.QMWindow = QtWidgets.QWidget()
        SwaMe.QMWindow.setWindowTitle("SwaMe arguments")
        
        

       
        #Actions for when buttons are clicked:
        SwaMe.QMWindow.BrowseButton.clicked.connect(SwaMe.onSwaMeBrowseClicked)
        SwaMe.QMWindow.RUNButton.clicked.connect(SwaMe.onSwaMeRUNClicked)


    def onSwaMeBrowseClicked(self):
        #FileInput.BrowseWindow.__init__(FileInput.BrowseWindow, self)
        SwaMe.QMWindow.files.show()
        SwaMe.File = FileInput.BrowseWindow.GetSwaMeInputFile(SwaMe)
        if(SwaMe.File):
                fname = os.path.basename(SwaMe.File)
                SwaMe.QMWindow.fileList.setText(fname)
    
    def onSwaMeRUNClicked(self):
        #Arguments:
        SwaMe.MassTolerance = 5000 #Arbitrary value that I hope no one would ever choose
        SwaMe.RTTolerance = 5000
        SwaMe.Division = 5000
        SwaMe.Dir=False
        #SwaMe.IRT==False

        if(SwaMe.QMWindow.MTTextBox.text()):
            SwaMe.MassTolerance = SwaMe.QMWindow.MTTextBox.text()
        if(SwaMe.QMWindow.RTTextBox.text()):
            SwaMe.RTTolerance = SwaMe.QMWindow.RTTextBox.text()
        if(SwaMe.QMWindow.divisionTextBox.text()):
            SwaMe.Division = SwaMe.QMWindow.divisionTextBox.text()
        if(SwaMe.QMWindow.Dir.isChecked):
            SwaMe.Dir = True

        SwaMePath = FileInput.BrowseWindow.GetSwaMePath(SwaMe)
        if  SwaMePath and SwaMe.File and SwaMe.Division!=5000 and SwaMe.MassTolerance!=5000:
            rstring = "r"
            QtCore.QProcess.startDetached(rstring.join(SwaMePath), 
                ["-i" , SwaMe.File, "-d", SwaMe.Division, "-m", SwaMe.MassTolerance, "--dir", str(SwaMe.Dir)])



