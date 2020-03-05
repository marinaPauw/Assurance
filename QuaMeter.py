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
        QuaMeter.Files = FileInput.BrowseWindow.GetQuaMeterInputFiles(QuaMeter)
        if(QuaMeter.Files):
            for file in QuaMeter.Files:
                fname = os.path.basename(file)
                UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.fileList.addItem(fname)
    
    def onQuaMeterRUNClicked(self):
        QuaMeterPath = FileInput.BrowseWindow.GetQuaMeterPath(QuaMeter)
        if  UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.cpusTextBox.text() and UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.CUOTextBox.text() and UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.CLOTextBox.text():
            rstring = "r"
            QtCore.QProcess.startDetached(rstring.join(QuaMeterPath), 
                ["",QuaMeter.Files,"-cpus", UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.cpusTextBox.text(), "-ChromatogramMzUpperOffset", UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.CUOTextBox.text(), "-ChromatogramMzLowerOffset", UI_MainWindow.Ui_MainWindow.tab.UploadFrame.leftFrame.CLOTextBox.text()])

