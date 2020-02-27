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
        QuaMeter.QMWindow = QtWidgets.QWidget()
        QuaMeter.QMWindow.setWindowTitle("QuaMeter arguments")
        
        #Widget declaring:
        QuaMeter.QMWindow.BrowseButton = QtWidgets.QPushButton(QuaMeter.QMWindow)
        QuaMeter.QMWindow.files = QtWidgets.QLabel(QuaMeter.QMWindow)
        QuaMeter.QMWindow.fileList = QtWidgets.QListWidget(QuaMeter.QMWindow)
        QuaMeter.QMWindow.cpusLabel= QtWidgets.QLabel(QuaMeter.QMWindow)
        QuaMeter.QMWindow.cpusTextBox = QLineEdit(self)
        QuaMeter.QMWindow.CLOLabel= QtWidgets.QLabel(QuaMeter.QMWindow)
        QuaMeter.QMWindow.CLOTextBox = QLineEdit(self)
        QuaMeter.QMWindow.CUOLabel= QtWidgets.QLabel(QuaMeter.QMWindow)
        QuaMeter.QMWindow.CUOTextBox = QLineEdit(self) 
        QuaMeter.QMWindow.RUNButton = QtWidgets.QPushButton(QuaMeter.QMWindow)
        
        #Widget geometries:
        QuaMeter.QMWindow.files.setGeometry(QtCore.QRect(90, 120, 300, 20))
        QuaMeter.QMWindow.fileList.setGeometry(QtCore.QRect(90, 120, 300, 200))
        QuaMeter.QMWindow.cpusLabel.setGeometry(QtCore.QRect(90, 120, 300, 20))
        QuaMeter.QMWindow.CLOLabel.setGeometry(QtCore.QRect(90, 120, 300, 20))
        QuaMeter.QMWindow.CUOLabel.setGeometry(QtCore.QRect(90, 120, 300, 20))

        #Widget stylesheets:
        QuaMeter.QMWindow.BrowseButton.setStyleSheet("background-color: rgb(240,240,240);")

        #Widget texts:
        QuaMeter.QMWindow.BrowseButton.setText("Browse ")
        QuaMeter.QMWindow.files.setText("Files selected: ")
        QuaMeter.QMWindow.cpusLabel.setText("Number of CPU's: ")
        QuaMeter.QMWindow.CLOLabel.setText("Chromatogram Lower Offset:")
        QuaMeter.QMWindow.CUOLabel.setText("Chromatogram Upper Offset:")
        QuaMeter.QMWindow.RUNButton.setText("RUN")

        
        #Layout:
        QuaMeter.QMWindow.vbox = QtWidgets.QVBoxLayout(QuaMeter.QMWindow)
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget( QuaMeter.QMWindow.BrowseButton)
        vbox2 = QtWidgets.QVBoxLayout(QuaMeter.QMWindow)
        vbox2.addStretch()
        vbox2.addWidget(QuaMeter.QMWindow.files)     
        vbox2.addWidget(QuaMeter.QMWindow.fileList)
        hbox1.addLayout(vbox2)
        hbox1.addStretch()
        QuaMeter.QMWindow.vbox.addLayout(hbox1)
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(QuaMeter.QMWindow.cpusLabel)
        hbox2.addWidget(QuaMeter.QMWindow.cpusTextBox)
        QuaMeter.QMWindow.vbox.addLayout(hbox2)
        hbox3 = QtWidgets.QHBoxLayout()
        hbox3.addWidget(QuaMeter.QMWindow.CLOLabel)
        hbox3.addWidget(QuaMeter.QMWindow.CLOTextBox)
        hbox3.addWidget(QuaMeter.QMWindow.CUOLabel)
        hbox3.addWidget(QuaMeter.QMWindow.CUOTextBox)
        QuaMeter.QMWindow.vbox.addLayout(hbox3)
        hbox4 = QtWidgets.QHBoxLayout()
        hbox4.addWidget(QuaMeter.QMWindow.RUNButton)
        QuaMeter.QMWindow.vbox.addLayout(hbox4)
        QuaMeter.QMWindow.show()

        #Arguments:
        if(QuaMeter.QMWindow.CLOTextBox.text()):
            QuaMeter.CLO = QuaMeter.QMWindow.CLOTextBox.text()
        if(QuaMeter.QMWindow.CUOTextBox.text()):
            QuaMeter.CUO = QuaMeter.QMWindow.CLOTextBox.text()
        if(QuaMeter.QMWindow.cpusTextBox.text()):
            QuaMeter.CPU = QuaMeter.QMWindow.cpusTextBox.text()

        #Actions for when buttons are clicked:
        QuaMeter.QMWindow.BrowseButton.clicked.connect(QuaMeter.onQuaMeterBrowseClicked)
        QuaMeter.QMWindow.RUNButton.clicked.connect(QuaMeter.onQuaMeterRUNClicked)


    def onQuaMeterBrowseClicked(self):
        #FileInput.BrowseWindow.__init__(FileInput.BrowseWindow, self)
        QuaMeter.QMWindow.files.show()
        QuaMeter.Files = FileInput.BrowseWindow.GetQuaMeterInputFiles(QuaMeter)
        if(QuaMeter.Files):
            for file in Files:
                fname = os.path.basename(file)
                QuaMeter.QMWindow.fileList.addItem(fname)
    
    def onQuaMeterRUNClicked(self):
        QuaMeterPath = FileInput.BrowseWindow.GetQuaMeterPath(QuaMeter)
        if  QuaMeter.QMWindow.cpusTextBox.text() and QuaMeter.QMWindow.CUOTextBox.text() and QuaMeter.QMWindow.CLOTextBox.text():
            rstring = "r"
            QtCore.QProcess.startDetached(rstring.join(QuaMeterPath), 
                ["",QuaMeter.Files,"-cpus", QuaMeter.QMWindow.cpusTextBox.text(), "-ChromatogramMzUpperOffset", QuaMeter.QMWindow.CUOTextBox.text(), "-ChromatogramMzLowerOffset", QuaMeter.QMWindow.CLOTextBox.text()])


