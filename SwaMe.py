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
        
        #Widget declaring:
        SwaMe.QMWindow.BrowseButton = QtWidgets.QPushButton(SwaMe.QMWindow)
        SwaMe.QMWindow.files = QtWidgets.QLabel(SwaMe.QMWindow)
        SwaMe.QMWindow.fileList = QtWidgets.QLabel(SwaMe.QMWindow)
        SwaMe.QMWindow.divisionLabel= QtWidgets.QLabel(SwaMe.QMWindow)
        SwaMe.QMWindow.divisionTextBox= QLineEdit(SwaMe.QMWindow)
        SwaMe.QMWindow.MTLabel= QtWidgets.QLabel(SwaMe.QMWindow)
        SwaMe.QMWindow.MTTextBox = QLineEdit(SwaMe.QMWindow)
        SwaMe.QMWindow.RTLabel= QtWidgets.QLabel(SwaMe.QMWindow)
        SwaMe.QMWindow.RTTextBox = QLineEdit(SwaMe.QMWindow)
        #SwaMe.QMWindow.DirLabel = QtWidgets.QLabel(SwaMe.QMWindow)
        SwaMe.QMWindow.Dir = QtWidgets.QRadioButton("Whole Directory:")
        SwaMe.QMWindow.RUNButton = QtWidgets.QPushButton(SwaMe.QMWindow)
        
        #Widget geometries:
        SwaMe.QMWindow.files.setGeometry(QtCore.QRect(90, 120, 300, 20))
        SwaMe.QMWindow.fileList.setGeometry(QtCore.QRect(90, 120, 300, 200))
        SwaMe.QMWindow.divisionLabel.setGeometry(QtCore.QRect(90, 120, 300, 20))
        SwaMe.QMWindow.MTLabel.setGeometry(QtCore.QRect(90, 120, 300, 20))
        SwaMe.QMWindow.RTLabel.setGeometry(QtCore.QRect(90, 120, 300, 20))

        #Widget stylesheets:
        SwaMe.QMWindow.BrowseButton.setStyleSheet("background-color: rgb(240,240,240);")

        #Widget texts:
        SwaMe.QMWindow.BrowseButton.setText("Browse ")
        SwaMe.QMWindow.files.setText("Files selected: ")
        SwaMe.QMWindow.divisionLabel.setText("Number of segments to divide the RT into: ")
        SwaMe.QMWindow.MTLabel.setText("MassTolerance:")
        SwaMe.QMWindow.RTLabel.setText("RTTolerance:")
        SwaMe.QMWindow.RUNButton.setText("RUN")

        
        #Layout:
        SwaMe.QMWindow.vbox = QtWidgets.QVBoxLayout(SwaMe.QMWindow)
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget( SwaMe.QMWindow.BrowseButton)
        vbox2 = QtWidgets.QVBoxLayout(SwaMe.QMWindow)
        vbox2.addStretch()
        vbox2.addWidget(SwaMe.QMWindow.files)     
        vbox2.addWidget(SwaMe.QMWindow.fileList)
        hbox1.addLayout(vbox2)
        hbox1.addStretch()
        SwaMe.QMWindow.vbox.addLayout(hbox1)
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(SwaMe.QMWindow.divisionLabel)
        hbox2.addWidget(SwaMe.QMWindow.divisionTextBox)
        SwaMe.QMWindow.vbox.addLayout(hbox2)
        hbox3 = QtWidgets.QHBoxLayout()
        hbox3.addWidget(SwaMe.QMWindow.MTLabel)
        hbox3.addWidget(SwaMe.QMWindow.MTTextBox)
        hbox3.addWidget(SwaMe.QMWindow.RTLabel)
        hbox3.addWidget(SwaMe.QMWindow.RTTextBox)
        SwaMe.QMWindow.vbox.addLayout(hbox3)
        hbox4 = QtWidgets.QHBoxLayout()
        hbox4.addWidget(SwaMe.QMWindow.RUNButton)
        SwaMe.QMWindow.vbox.addLayout(hbox4)
        hbox5 = QtWidgets.QHBoxLayout()
        hbox5.addWidget(SwaMe.QMWindow.RTLabel)
        hbox5.addWidget(SwaMe.QMWindow.RTTextBox)
        SwaMe.QMWindow.vbox.addLayout(hbox5)
        hbox6 = QtWidgets.QHBoxLayout()
        hbox6.addWidget(SwaMe.QMWindow.Dir)
        SwaMe.QMWindow.vbox.addLayout(hbox6)
        SwaMe.QMWindow.show()

       
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



