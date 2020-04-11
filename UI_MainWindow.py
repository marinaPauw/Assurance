import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
import sys
import statistics
import scipy
from sklearn import decomposition as sd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import matplotlib.pyplot as plt
import re
import FileInput
import QuaMeter
import IndividualMetrics
import PCA
import PCAGraph
import DataPreparation
import RandomForest
import numpy as np
import pandas as pd
import SwaMe
import pepXMLReader
import RFSelectionPlots
import FeatureImportancePlot
from scipy.spatial import distance_matrix


class Ui_MainWindow(QtWidgets.QTabWidget):
    
    def setupUi(self):

        self.setWindowTitle("Assurance")
        self.resize(800,650)

        # fonts and style:
        Ui_MainWindow.boldfont = QtGui.QFont()
        Ui_MainWindow.boldfont.setBold(True)

        # Setting up the home tab:
        Ui_MainWindow.tab = QtWidgets.QWidget()
        self.setCurrentIndex(0)
        self.tab.main_layout = QtWidgets.QVBoxLayout()
        self.addTab(self.tab, "Home")
        self.tab.setStyleSheet("background-color: gainsboro;")

         #--------------------------------------------------------------Frames:-------------------------------------------------------
        Ui_MainWindow.tab.UploadFrame = QtWidgets.QFrame(self)
        Ui_MainWindow.tab.UploadFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Ui_MainWindow.tab.UploadFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Ui_MainWindow.tab.UploadFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")
         
         
        Ui_MainWindow.tab.UploadFrame.leftFrame = QtWidgets.QFrame(Ui_MainWindow.tab.UploadFrame)
        Ui_MainWindow.tab.UploadFrame.leftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Ui_MainWindow.tab.UploadFrame.leftFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Ui_MainWindow.tab.UploadFrame.leftFrame.setStyleSheet("background-color: rgb(192,192,192); margin:5px;")
        

        Ui_MainWindow.tab.UploadFrame.rightFrame = QtWidgets.QFrame(Ui_MainWindow.tab.UploadFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Ui_MainWindow.tab.UploadFrame.rightFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Ui_MainWindow.tab.UploadFrame.rightFrame.setStyleSheet("background-color: rgb(192,192,192); margin:5px;")

        
        Ui_MainWindow.tab.AnalysisFrame = QtWidgets.QFrame(self)
        Ui_MainWindow.tab.AnalysisFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Ui_MainWindow.tab.AnalysisFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Ui_MainWindow.tab.AnalysisFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")

        Ui_MainWindow.tab.OutputFrame = QtWidgets.QFrame(self)
        Ui_MainWindow.tab.OutputFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Ui_MainWindow.tab.OutputFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Ui_MainWindow.tab.OutputFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")


        #-------------------------------------------------QuaMeterLayout--------------------------------------------------------
        
        #Widget declaring:
        Ui_MainWindow.tab.UploadFrame.leftFrame.QuaMeterbutton = QtWidgets.QPushButton(Ui_MainWindow.tab.UploadFrame.leftFrame)
        Ui_MainWindow.tab.UploadFrame.leftFrame.QuaMeterbutton.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.tab.UploadFrame.leftFrame.BrowseButton = QtWidgets.QPushButton(Ui_MainWindow.tab.UploadFrame.leftFrame)
        Ui_MainWindow.tab.UploadFrame.leftFrame.files = QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.leftFrame)
        Ui_MainWindow.tab.UploadFrame.leftFrame.fileList = QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.leftFrame)
        Ui_MainWindow.tab.UploadFrame.leftFrame.cpusLabel= QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.leftFrame)
        Ui_MainWindow.tab.UploadFrame.leftFrame.cpusTextBox = QtWidgets.QLineEdit(Ui_MainWindow.tab.UploadFrame.leftFrame)
        Ui_MainWindow.tab.UploadFrame.leftFrame.CLOLabel= QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.leftFrame)
        Ui_MainWindow.tab.UploadFrame.leftFrame.CLOTextBox = QtWidgets.QLineEdit(Ui_MainWindow.tab.UploadFrame.leftFrame)
        Ui_MainWindow.tab.UploadFrame.leftFrame.CUOLabel= QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.leftFrame)
        Ui_MainWindow.tab.UploadFrame.leftFrame.CUOTextBox = QtWidgets.QLineEdit(Ui_MainWindow.tab.UploadFrame.leftFrame) 
        Ui_MainWindow.tab.UploadFrame.leftFrame.RUNButton = QtWidgets.QPushButton(Ui_MainWindow.tab.UploadFrame.leftFrame)
        Ui_MainWindow.tab.UploadFrame.leftFrame.textedit =QtWidgets.QTextEdit(readOnly=True)
        

        #Widget stylesheets:
        Ui_MainWindow.tab.UploadFrame.leftFrame.BrowseButton.setStyleSheet("background-color: rgb(240,240,240);")

        #Widget texts:
        Ui_MainWindow.tab.UploadFrame.leftFrame.BrowseButton.setText("Browse ")
        Ui_MainWindow.tab.UploadFrame.leftFrame.files.setText("Folder:")
        Ui_MainWindow.tab.UploadFrame.leftFrame.cpusLabel.setText("Number of CPU's: ")
        Ui_MainWindow.tab.UploadFrame.leftFrame.CLOLabel.setText("Chromatogram Lower Offset:")
        Ui_MainWindow.tab.UploadFrame.leftFrame.CUOLabel.setText("Chromatogram Upper Offset:")
        Ui_MainWindow.tab.UploadFrame.leftFrame.RUNButton.setText("RUN")


        #QuaMetervbox:
        #Layout:
        QuaMetervbox = QtWidgets.QVBoxLayout(Ui_MainWindow.tab.UploadFrame.leftFrame)
        hbox0 = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.leftFrame)
        hbox0.addWidget(Ui_MainWindow.tab.UploadFrame.leftFrame.QuaMeterbutton)
        QuaMetervbox.addLayout(hbox0)
        hbox1 = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.leftFrame)
        Qvbox2 = QtWidgets.QVBoxLayout(Ui_MainWindow.tab.UploadFrame.leftFrame)
        Qvbox2.addWidget( Ui_MainWindow.tab.UploadFrame.leftFrame.BrowseButton)
        QhboxFiles = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.leftFrame)
        QhboxFiles.addWidget(Ui_MainWindow.tab.UploadFrame.leftFrame.files)     
        QhboxFiles.addWidget(Ui_MainWindow.tab.UploadFrame.leftFrame.fileList)
        Qvbox2.addLayout(QhboxFiles)
        hbox1.addLayout(Qvbox2)
        hbox1.addStretch()
        QuaMetervbox.addLayout(hbox1)

        hbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.leftFrame)
        hbox2.addWidget(Ui_MainWindow.tab.UploadFrame.leftFrame.cpusLabel)
        hbox2.addWidget(Ui_MainWindow.tab.UploadFrame.leftFrame.cpusTextBox)
        QuaMetervbox.addLayout(hbox2)
        hbox3 = QtWidgets.QHBoxLayout()
        hbox3.addWidget(Ui_MainWindow.tab.UploadFrame.leftFrame.CLOLabel)
        hbox3.addWidget(Ui_MainWindow.tab.UploadFrame.leftFrame.CLOTextBox)
        hbox3.addWidget(Ui_MainWindow.tab.UploadFrame.leftFrame.CUOLabel)
        hbox3.addWidget(Ui_MainWindow.tab.UploadFrame.leftFrame.CUOTextBox)
        QuaMetervbox.addLayout(hbox3)
        hbox4 = QtWidgets.QHBoxLayout()
        hbox4.addWidget(Ui_MainWindow.tab.UploadFrame.leftFrame.RUNButton)
        hbox4.addWidget(Ui_MainWindow.tab.UploadFrame.leftFrame.textedit)
        QuaMetervbox.addLayout(hbox4)

        #-------------------------------------------------SwaMeLayout--------------------------------------------------------

        #Widget declaring:
        Ui_MainWindow.tab.UploadFrame.rightFrame.SwaMebutton = QtWidgets.QPushButton(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton = QtWidgets.QPushButton(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.Sfiles = QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SfileList = QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.divisionLabel= QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.divisionTextBox= QtWidgets.QLineEdit(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.MTLabel= QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.MTTextBox = QtWidgets.QLineEdit(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.RTLabel= QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.RTTextBox = QtWidgets.QLineEdit(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SRUNButton = QtWidgets.QPushButton(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRT = QtWidgets.QRadioButton("iRT")
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTtoleranceLabel =QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminintensityLabel =QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminpeptidesLabel =QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTtoleranceTB =QtWidgets.QLineEdit(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminintensityTB =QtWidgets.QLineEdit(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminpeptidesTB =QtWidgets.QLineEdit(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.textedit =QtWidgets.QTextEdit(readOnly=True)
        Ui_MainWindow.IRTinputFile = None


        #Widget stylesheets:
        Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.tab.UploadFrame.rightFrame.SwaMebutton.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton.setFixedHeight(30)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton.setFixedHeight(30)


        #Widget texts:
        Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton.setText("Browse ")
        Ui_MainWindow.tab.UploadFrame.rightFrame.Sfiles.setText("Folder: ")
        Ui_MainWindow.tab.UploadFrame.rightFrame.divisionLabel.setText("Number of segments to divide the RT into: ")
        Ui_MainWindow.tab.UploadFrame.rightFrame.MTLabel.setText("MassTolerance:")
        Ui_MainWindow.tab.UploadFrame.rightFrame.RTLabel.setText("RTTolerance:")
        Ui_MainWindow.tab.UploadFrame.rightFrame.SRUNButton.setText("RUN")
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTtoleranceLabel.setText("iRTtolerance")
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminintensityLabel.setText("MinIRTIntensity")
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminpeptidesLabel.setText("MinIRTpeptides")

        
        #Layout:
        SwaMevbox = QtWidgets.QVBoxLayout(Ui_MainWindow.tab.UploadFrame.rightFrame)
        SwaMehbox0 = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.rightFrame)
        SwaMehbox0.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.SwaMebutton)
        SwaMevbox.addLayout(SwaMehbox0)
        SwaMehbox1 = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.rightFrame)
        SwaMevbox2 = QtWidgets.QVBoxLayout(Ui_MainWindow.tab.UploadFrame.rightFrame)
        SwaMehboxFiles = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.rightFrame)
        SwaMehboxFiles.addWidget( Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton)
        SwaMehboxFiles.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.Sfiles)     
        SwaMehboxFiles.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.SfileList)
        SwaMevbox2.addLayout(SwaMehboxFiles)
        SwaMehbox1.addLayout(SwaMevbox2)
        SwaMehbox1.addStretch()
        SwaMevbox.addLayout(SwaMehbox1)
        SwaMehbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.rightFrame)
        SwaMehbox2.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.divisionLabel)
        SwaMehbox2.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.divisionTextBox)
        SwaMevbox.addLayout(SwaMehbox2)
        SwaMehbox3 = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.rightFrame)
        SwaMehbox3.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.MTLabel)
        SwaMehbox3.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.MTTextBox)
        SwaMehbox3.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.RTLabel)
        SwaMehbox3.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.RTTextBox)
        SwaMevbox.addLayout(SwaMehbox3)
        SwaMehbox4 = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.rightFrame)
        SwaMehbox4.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.iRT)
        SwaMevbox.addLayout(SwaMehbox4)
        SwaMehbox5 = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.rightFrame)
        SwaMehbox5.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.iRTtoleranceLabel)
        SwaMehbox5.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.iRTtoleranceTB)
        SwaMevbox.addLayout(SwaMehbox5)
        SwaMehbox6 = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.rightFrame)
        SwaMehbox6.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminintensityLabel)
        SwaMehbox6.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminintensityTB)
        SwaMehbox6.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminpeptidesLabel)
        SwaMehbox6.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminpeptidesTB)
        SwaMevbox.addLayout(SwaMehbox6)
        SwaMehbox7 = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame.rightFrame)
        SwaMehbox7.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.SRUNButton)
        SwaMehbox7.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame.textedit)
        SwaMevbox.addLayout(SwaMehbox7)
        #------------------------------------------------OutputFrame--------------------------------------------------------
        pdf = QtWidgets.QPushButton(self.tab)
        pdf.setStyleSheet("background-color: rgb(240,240,240);")
        pdf.setText("Export to PDF")
        
        outputHBOX = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.OutputFrame)
        outputHBOX.addStretch()
        outputHBOX.addWidget(pdf)
        outputHBOX.addStretch()
        

        #-------------------------------------------------MainLayout--------------------------------------------------------
          #All the buttons MainWindow:
        Ui_MainWindow.tab.UploadFrame.browse = QtWidgets.QPushButton(self.tab)
        Ui_MainWindow.tab.UploadFrame.browse.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.tab.AnalysisFrame.Outliers = QtWidgets.QPushButton(self.tab)
        Ui_MainWindow.tab.AnalysisFrame.Outliers.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.tab.AnalysisFrame.IndMetrics = QtWidgets.QPushButton(self.tab)
        Ui_MainWindow.tab.AnalysisFrame.IndMetrics.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.tab.AnalysisFrame.Longitudinal = QtWidgets.QPushButton(self.tab)
        Ui_MainWindow.tab.AnalysisFrame.Longitudinal.setStyleSheet("background-color: rgb(240,240,240);")

        #clicked.connect
        Ui_MainWindow.tab.UploadFrame.leftFrame.QuaMeterbutton.clicked.connect(self.onQuaMeterClicked)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SwaMebutton.clicked.connect(self.onSwaMeClicked)
        Ui_MainWindow.tab.UploadFrame.browse.clicked.connect(self.onBrowseClicked)
        Ui_MainWindow.tab.AnalysisFrame.Outliers.clicked.connect(self.onOutliersClicked)
        Ui_MainWindow.tab.AnalysisFrame.IndMetrics.clicked.connect(self.onIndMetricsClicked)
        Ui_MainWindow.tab.AnalysisFrame.Longitudinal.clicked.connect(self.onLongitudinalClicked)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRT.toggled.connect(self.onIRTClicked)

        # Labels and progressbars
        self.tab.UploadFrame.InstructionLabel = QtWidgets.QLabel()
        self.tab.UploadFrame.InstructionLabel.setGeometry(QtCore.QRect(90, 120, 300, 10))
        Ui_MainWindow.tab.UploadFrame.filename = QtWidgets.QLabel(self.tab)
        Ui_MainWindow.tab.UploadFrame.filename.setGeometry(QtCore.QRect(90, 120, 300, 10))
        Ui_MainWindow.tab.UploadFrame.InputLabel = QtWidgets.QLabel()
        Ui_MainWindow.tab.UploadFrame.uploadLabel = QtWidgets.QLabel()
        self.tab.AnalysisFrame.UploadProgress = QtWidgets.QProgressBar()
        self.tab.AnalysisFrame.UploadProgress.setGeometry(200, 80, 250, 20)
        self.tab.AnalysisFrame.progress1 = QtWidgets.QProgressBar()
        self.tab.AnalysisFrame.progress1.setGeometry(200, 80, 250, 20)
        self.tab.AnalysisFrame.chooseLabel = QtWidgets.QLabel()
        self.tab.AnalysisFrame.analysisLabel = QtWidgets.QLabel()
        self.tab.AnalysisFrame.progress2 = QtWidgets.QProgressBar()
        self.tab.AnalysisFrame.progress2.setGeometry(200, 80, 250, 20)
        
        #UploadFrame:
        uploadvbox = QtWidgets.QVBoxLayout(Ui_MainWindow.tab.UploadFrame)
        uploadvbox.addWidget(Ui_MainWindow.tab.UploadFrame.InputLabel)
        Instructionshbox = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame)
        Instructionshbox.addWidget(self.tab.UploadFrame.InstructionLabel)
        Instructionshbox.setAlignment(QtCore.Qt.AlignLeft)
        uploadvbox.addLayout(Instructionshbox)
        QuaMehbox = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame)
        QuaMehbox.addWidget(Ui_MainWindow.tab.UploadFrame.leftFrame,0)
        QuaMehbox.addWidget(Ui_MainWindow.tab.UploadFrame.rightFrame,2)
        uploadvbox.addLayout(QuaMehbox)
        hbox7 = QtWidgets.QHBoxLayout(Ui_MainWindow.tab.UploadFrame)
        hbox7.addWidget(Ui_MainWindow.tab.UploadFrame.uploadLabel)
        hbox7.addWidget(Ui_MainWindow.tab.UploadFrame.browse)
        hbox7.addWidget(Ui_MainWindow.tab.UploadFrame.filename)
        hbox7.addWidget(Ui_MainWindow.tab.AnalysisFrame.UploadProgress)
        Ui_MainWindow.tab.UploadFrame.browse.setFixedHeight(30)
        uploadvbox.addLayout(hbox7)


        #AnalysisFrame
        avbox = QtWidgets.QVBoxLayout(Ui_MainWindow.tab.AnalysisFrame)
        hbox6 = QtWidgets.QHBoxLayout()
        hbox6.addWidget(self.tab.AnalysisFrame.analysisLabel)
        hbox6.setAlignment(QtCore.Qt.AlignLeft)
        avbox.addLayout(hbox6)
        hbox8 = QtWidgets.QHBoxLayout()
        hbox8.addWidget(self.tab.AnalysisFrame.chooseLabel)
        hbox8.setAlignment(QtCore.Qt.AlignLeft)
        avbox.addLayout(hbox8)
        hbox9 = QtWidgets.QHBoxLayout()
        hbox9.addWidget(Ui_MainWindow.tab.AnalysisFrame.Outliers)
        hbox9.addWidget(Ui_MainWindow.tab.AnalysisFrame.IndMetrics)
        hbox9.addWidget(Ui_MainWindow.tab.AnalysisFrame.Longitudinal)
        hbox9.setAlignment(QtCore.Qt.AlignLeft)
        Ui_MainWindow.tab.AnalysisFrame.Outliers.setFixedHeight(40)
        Ui_MainWindow.tab.AnalysisFrame.Outliers.setFixedWidth(130)
        Ui_MainWindow.tab.AnalysisFrame.Longitudinal.setFixedHeight(40)
        Ui_MainWindow.tab.AnalysisFrame.Longitudinal.setFixedWidth(130)
        Ui_MainWindow.tab.AnalysisFrame.IndMetrics.setFixedHeight(40)
        Ui_MainWindow.tab.AnalysisFrame.IndMetrics.setFixedWidth(130)
        avbox.addLayout(hbox9)
        hbox9.setAlignment(QtCore.Qt.AlignCenter)
        hbox10 = QtWidgets.QHBoxLayout()
        hbox10.addWidget(self.tab.AnalysisFrame.progress1)
        hbox10.addWidget(self.tab.AnalysisFrame.progress2)
        hbox10.setAlignment(QtCore.Qt.AlignLeft)
        avbox.addLayout(hbox10)
        hbox11 = QtWidgets.QHBoxLayout()
        avbox.addLayout(hbox11)
        hbox11.setAlignment(QtCore.Qt.AlignLeft)


        #MainLayout
        vbox = QtWidgets.QVBoxLayout(self.tab)
        hbox0 = QtWidgets.QHBoxLayout()
        hbox0.addWidget(Ui_MainWindow.tab.UploadFrame)
        vbox.addLayout(hbox0)
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(Ui_MainWindow.tab.AnalysisFrame)
        vbox.addLayout(hbox1)
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(Ui_MainWindow.tab.OutputFrame)
        vbox.addLayout(hbox2)
        
        vbox.setAlignment(QtCore.Qt.AlignLeft)
        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(self)

    def enable_slot(self):
        PCAGraph.PCAGraph.loadingsToggledOn(Ui_MainWindow)
        Ui_MainWindow.PCA.LoadingsProgressBar.setValue(100)

    def disable_slot(self):
        PCAGraph.PCAGraph.loadingsToggledOff()

    @pyqtSlot()
    def onQuaMeterClicked(self):
        Ui_MainWindow.DisableAnalysisButtons(self)
        QuaMeter.QuaMeter.setupUI(self)


    @pyqtSlot()
    def onSwaMeClicked(self):
        Ui_MainWindow.DisableAnalysisButtons(self)
        SwaMe.SwaMe.setupUI(self)

    @pyqtSlot()
    def onBrowseClicked(self):
        Ui_MainWindow.DisableAnalysisButtons(self)
        FileInput.BrowseWindow.__init__(Ui_MainWindow)
        inputFile = FileInput.BrowseWindow.GetInputFile(Ui_MainWindow)
        if inputFile:
            #filepath = FileInput.BrowseWindow.FileCheck(self, inputFile)
            Ui_MainWindow.metrics = FileInput.BrowseWindow.metricsParsing(self, inputFile)
            if  "Filename" in Ui_MainWindow.metrics[0].columns:
                Ui_MainWindow.metrics[0].index = Ui_MainWindow.metrics[0]["Filename"]
            Ui_MainWindow.NumericMetrics =[]
            #Ui_MainWindow.checkColumnLength(self)
            #Ui_MainWindow.metrics.set_index(Ui_MainWindow.metrics[0].index[0])
            Ui_MainWindow.NumericMetrics.append(DataPreparation.DataPrep.ExtractNumericColumns(self, self.metrics[0]))

            Ui_MainWindow.NumericMetrics[0]  = DataPreparation.DataPrep.RemoveLowVarianceColumns(self, self.NumericMetrics[0])
            Ui_MainWindow.NumericMetrics[0].index = Ui_MainWindow.metrics[0].index
        Ui_MainWindow.EnableAnalysisButtons(self)

    @pyqtSlot()
    def onOutliersClicked(self):
        self.DisableAnalysisButtons()

        Ui_MainWindow.tab.AnalysisFrame.progress1.show()
        Ui_MainWindow.tab.AnalysisFrame.progress1.setValue(10)

       
        self.EnableAnalysisButtons()
        
        FileInput.BrowseWindow.currentDataset = Ui_MainWindow.NumericMetrics[0]
             # Check if you have the correct number of variables/samples
        if self.checkColumnNumberForPCA() == 1:

                if self.checkSampleNumberForPCA() == 1:
                    if len(FileInput.BrowseWindow.currentDataset.columns)>1:

                        #sampleToVariableRatio = PCA.PCA.calculateSampleToVariableRatio(self, FileInput.BrowseWindow.currentDataset)
        
       
                        PCA.PCA.CreatePCAGraph(FileInput.BrowseWindow.currentDataset)
                        Ui_MainWindow.tab.AnalysisFrame.progress1.setValue(51)
                        # Need to correctly calculate euc distance in N dimension
                        outliers = Ui_MainWindow.CalculateOutliers(self)
                        Ui_MainWindow.outlierlist = outliers["Filename"]

                        # --------------------------------------Widgets-------------------------------------------
                        Ui_MainWindow.PCA = QtWidgets.QTabWidget()
                        Ui_MainWindow.PCA.plotlabel = QtWidgets.QLabel(Ui_MainWindow.PCA)
                        Ui_MainWindow.PCA.plotlabel.setGeometry(10, 500, 1000, 300)
                        Ui_MainWindow.PCA.PCAplot = PCAGraph.PCAGraph(self.metrics,
                                                                      PCA.plotdata)

                        Ui_MainWindow.outlierlistLabel = QtWidgets.QLabel(Ui_MainWindow.PCA)
                        Ui_MainWindow.OutlierSamples = QtWidgets.QLabel(Ui_MainWindow.PCA)
                        Ui_MainWindow.OutlierSamples.setAlignment(QtCore.Qt.AlignLeft)

                        oIndex = self.addTab(Ui_MainWindow.PCA, "Outlier detection results")
                        Ui_MainWindow.PCA.layout = QtWidgets.QVBoxLayout()
                        Ui_MainWindow.PCA.Checkboxlabel = QtWidgets.QLabel(Ui_MainWindow.PCA)
                        Ui_MainWindow.PCA.Checkboxlabel.setText("Toggle loadings on/off:")
                        Ui_MainWindow.PCA.Checkbox = QtWidgets.QCheckBox("Loadings",
                                                                         Ui_MainWindow.PCA)
                        Ui_MainWindow.PCA.Checkbox.setChecked(False)
                        Ui_MainWindow.PCA.Checkbox.stateChanged.connect(
                            lambda x: Ui_MainWindow.enable_slot(self)
                            if x else Ui_MainWindow.disable_slot(self))
                        Ui_MainWindow.PCA.LoadingsProgressBar = QtWidgets.QProgressBar()
                        Ui_MainWindow.PCA.LoadingsProgressBar.setGeometry(200, 80, 250, 20)

                        
                        Ui_MainWindow.PCA.Redolabel = QtWidgets.QLabel(Ui_MainWindow.PCA)
                        Ui_MainWindow.PCA.Redolabel.setText("Redo analysis without the outliers:")
                        Ui_MainWindow.PCA.Redobox = QtWidgets.QCheckBox("Redo",
                                                                         Ui_MainWindow.PCA)
                        Ui_MainWindow.PCA.Redobox.setChecked(False)
                        Ui_MainWindow.PCA.Redobox.stateChanged.connect(
                            lambda x: Ui_MainWindow.enable_reanalysis(self))

                    # --------------------------------------Layout-------------------------------------------

                        vbox2 = QtWidgets.QVBoxLayout(Ui_MainWindow.PCA)
                        hbox = QtWidgets.QHBoxLayout(Ui_MainWindow.PCA)
                        vbox3 = QtWidgets.QVBoxLayout(Ui_MainWindow.PCA)
                        vbox3.addStretch()
                        vbox3.addWidget(Ui_MainWindow.outlierlistLabel)
                        vbox3.addWidget(Ui_MainWindow.OutlierSamples)
                        vbox3.addWidget(Ui_MainWindow.PCA.Checkboxlabel)
                        vbox3.addWidget(Ui_MainWindow.PCA.Checkbox)
                        vbox3.addWidget(Ui_MainWindow.PCA.LoadingsProgressBar)
                        vbox3.addWidget(Ui_MainWindow.PCA.Redolabel)
                        vbox3.addWidget(Ui_MainWindow.PCA.Redobox)
                        vbox3.addStretch()
                        vbox3.setAlignment(QtCore.Qt.AlignLeft)

                        hbox.addLayout(vbox3)
                        vbox4 = QtWidgets.QVBoxLayout(Ui_MainWindow.PCA)
                        Ui_MainWindow.PCA.Emptyspace = QtWidgets.QLabel(Ui_MainWindow.PCA)
                        Ui_MainWindow.PCA.Emptyspace.setText(" ")
                        vbox4.addWidget(Ui_MainWindow.PCA.Emptyspace)
                        hbox.addLayout(vbox4)
                        hboxPlot = QtWidgets.QHBoxLayout(Ui_MainWindow.PCA)
                        hboxPlot.addStretch()

                        hboxPlot.addWidget(Ui_MainWindow.PCA.plotlabel)
                        hboxPlot.addStretch()
                        vbox2.addLayout(hboxPlot)
                        vbox2.setAlignment(QtCore.Qt.AlignCenter)
                        hbox.setAlignment(QtCore.Qt.AlignCenter)
                        vbox2.addLayout(hbox)
                        hbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.PCA)

                        hbox.addWidget(Ui_MainWindow.PCA.PCAplot)
                        Ui_MainWindow.PCA.PCAplot.setGeometry(400, 200, 500, 100)
                        hbox2.setAlignment(QtCore.Qt.AlignCenter)
                        vbox2.addLayout(hbox2)
                        Ui_MainWindow.retranslateUi2(Ui_MainWindow.PCA)
                        Ui_MainWindow.EnableAnalysisButtons(self)
                        Ui_MainWindow.tab.AnalysisFrame.progress1.setValue(100)
                        PCAGraph.fig.canvas.mpl_connect("motion_notify_event",
                                                        Ui_MainWindow.onhover)
                        self.setCurrentIndex(oIndex)

    def DisableBrowseButtons(self):
        Ui_MainWindow.tab.UploadFrame.browse.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SwaMebutton.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.leftFrame.QuaMeterbutton.setEnabled(False)

    def EnableQuaMeterArguments(self):
        
        Ui_MainWindow.tab.UploadFrame.leftFrame.files.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.leftFrame.fileList.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.leftFrame.cpusLabel.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.leftFrame.cpusTextBox.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.leftFrame.CLOLabel.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.leftFrame.CLOTextBox.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.leftFrame.CUOLabel.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.leftFrame.CUOTextBox.setEnabled(True) 
        Ui_MainWindow.tab.UploadFrame.leftFrame.BrowseButton.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.leftFrame.RUNButton.setEnabled(True)
        #Ui_MainWindow.tab.UploadFrame.leftFrame.Dir.setEnabled(True)

    def DisableQuaMeterArguments(self):
        Ui_MainWindow.tab.UploadFrame.leftFrame.BrowseButton.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.leftFrame.files.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.leftFrame.fileList.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.leftFrame.cpusLabel.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.leftFrame.cpusTextBox.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.leftFrame.CLOLabel.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.leftFrame.CLOTextBox.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.leftFrame.CUOLabel.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.leftFrame.CUOTextBox.setEnabled(False) 
        Ui_MainWindow.tab.UploadFrame.leftFrame.BrowseButton.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.leftFrame.RUNButton.setEnabled(False)

    def EnableSwaMeArguments(self):
        
        Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.Sfiles.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SfileList.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.divisionLabel.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.divisionTextBox.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.MTLabel.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.MTTextBox.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.RTLabel.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.RTTextBox.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SRUNButton.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRT.setEnabled(True)
        
    def DisableSwaMeArguments(self):
        Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.Sfiles.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SfileList.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.divisionLabel.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.divisionTextBox.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.MTLabel.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.MTTextBox.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.RTLabel.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.RTTextBox.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SRUNButton.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRT.setEnabled(False)
        Ui_MainWindow.DisableSwaMeIRTArguments(self)

    def EnableSwaMeIRTArguments(self):
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTtoleranceLabel.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminintensityLabel.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminpeptidesLabel.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTtoleranceTB.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminintensityTB.setEnabled(True)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminpeptidesTB.setEnabled(True)

    def DisableSwaMeIRTArguments(self):
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTtoleranceLabel.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminintensityLabel.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminpeptidesLabel.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTtoleranceTB.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminintensityTB.setEnabled(False)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminpeptidesTB.setEnabled(False)

    def EnableAnalysisButtons(self):
        Ui_MainWindow.tab.UploadFrame.browse.setEnabled(True)
        Ui_MainWindow.tab.AnalysisFrame.Outliers.setEnabled(True)
        Ui_MainWindow.tab.AnalysisFrame.IndMetrics.setEnabled(True)
        Ui_MainWindow.tab.AnalysisFrame.Longitudinal.setEnabled(True)

    def DisableAnalysisButtons(self):
        Ui_MainWindow.tab.UploadFrame.browse.setEnabled(False)
        Ui_MainWindow.tab.AnalysisFrame.Outliers.setEnabled(False)
        Ui_MainWindow.tab.AnalysisFrame.IndMetrics.setEnabled(False)
        Ui_MainWindow.tab.AnalysisFrame.Longitudinal.setEnabled(False)

    @pyqtSlot()
    def enable_reanalysis(self):
        Ui_MainWindow.NumericMetrics[0] = Ui_MainWindow.NumericMetrics[0].drop(Ui_MainWindow.outlierlist)
        Ui_MainWindow.onOutliersClicked(self)

    @pyqtSlot()
    def onIRTClicked(self):
         Ui_MainWindow.EnableSwaMeIRTArguments(self)
         Ui_MainWindow.IRTinputFile = FileInput.BrowseWindow.GetIRTInputFile(Ui_MainWindow)

    @pyqtSlot()
    def onIndMetricsClicked(self):
        Ui_MainWindow.DisableAnalysisButtons(self)
        Ui_MainWindow.tab.AnalysisFrame.progress2.show()
        Ui_MainWindow.tab.AnalysisFrame.progress2.setValue(10)
        Ui_MainWindow.indMetrics = QtWidgets.QTabWidget()
        Ui_MainWindow.tab.AnalysisFrame.progress2.setValue(33)
        Ui_MainWindow.iIndex = self.addTab(Ui_MainWindow.indMetrics,
                                 "Individual metrics")
         
       
        Ui_MainWindow.listOfMetrics = list()
        if "StartTimeStamp" in Ui_MainWindow.metrics[0].columns:
            Ui_MainWindow.listOfMetrics.append("StartTimeStamp")
        for dataset in range(len(Ui_MainWindow.NumericMetrics)): # For each dataset in all the datasets we have
            for element in Ui_MainWindow.NumericMetrics[dataset].columns:
                    Ui_MainWindow.listOfMetrics.append(element)
                    
        Ui_MainWindow.element = Ui_MainWindow.listOfMetrics[0]
        #-------------- widgets ---------------------------------------
        
        whichds = 0
        for dataset in range(len(Ui_MainWindow.NumericMetrics)):
                if Ui_MainWindow.element in Ui_MainWindow.NumericMetrics[dataset].columns:
                    whichds = dataset
                    break
        Ui_MainWindow.sampleSelected = Ui_MainWindow.NumericMetrics[0].index[0]
        Ui_MainWindow.createGraph(self, whichds)

    def createGraph(self, whichds):
        Ui_MainWindow.indMetrics.comboBox = QtWidgets.QComboBox(Ui_MainWindow.indMetrics)
        for metric in Ui_MainWindow.listOfMetrics:
            Ui_MainWindow.indMetrics.comboBox.addItem(metric)
        Ui_MainWindow.indMetrics.comboBox.activated[str].connect(self.metric_change)
        Ui_MainWindow.indMetrics.sampleBox = QtWidgets.QComboBox(Ui_MainWindow.indMetrics)
        for sample in Ui_MainWindow.metrics[0].index:
            Ui_MainWindow.indMetrics.sampleBox.addItem(sample)
        Ui_MainWindow.indMetrics.sampleBox.activated[str].connect(self.sample_change)
        Ui_MainWindow.tab.AnalysisFrame.progress2.setValue(100)
        vbox = QtWidgets.QVBoxLayout(Ui_MainWindow.indMetrics)
        hbox1 = QtWidgets.QHBoxLayout(Ui_MainWindow.indMetrics)
        hbox1.addStretch()
        Ui_MainWindow.indMetrics.indPlotLabel = QtWidgets.QLabel(
                        Ui_MainWindow.indMetrics)
        Ui_MainWindow.indMetrics.indPlotLabel.setText(Ui_MainWindow.element)
        Ui_MainWindow.indMetrics.indPlotLabel.setFont(
                            Ui_MainWindow.boldfont)
        hbox1.addWidget(Ui_MainWindow.indMetrics.indPlotLabel)
        hbox1.addStretch()
        vbox.addLayout(hbox1)
        hbox15 = QtWidgets.QHBoxLayout(Ui_MainWindow.indMetrics)
        hbox15.addStretch()
        hbox15.addWidget(Ui_MainWindow.indMetrics.sampleBox)
        vbox.addLayout(hbox15)
        hbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.indMetrics)
        hbox2.addStretch()
        try:
            indMetPlot
            indMetPlot.clear()
        except NameError:
            indMetPlot = None
        indMetPlot = IndividualMetrics.MyIndMetricsCanvas(Ui_MainWindow.NumericMetrics[whichds],
                            Ui_MainWindow.NumericMetrics[whichds], Ui_MainWindow.element)
        hbox2.addWidget(indMetPlot)
        hbox2.addStretch()
        vbox.addLayout(hbox2)
        hbox3 =  QtWidgets.QHBoxLayout(Ui_MainWindow.indMetrics)
        hbox3.addStretch()
        hbox3.addWidget(Ui_MainWindow.indMetrics.comboBox)
        hbox3.addStretch()
        vbox.addLayout(hbox3)
        vbox.setContentsMargins(30, 20, 30, 100)
        self.setCurrentIndex(Ui_MainWindow.iIndex)
        Ui_MainWindow.EnableAnalysisButtons(self)

    def metric_change(self, text):
        Ui_MainWindow.element = text
        whichds = 0
        for dataset in range(len(Ui_MainWindow.NumericMetrics)):
                if Ui_MainWindow.element in Ui_MainWindow.NumericMetrics[dataset].columns:
                    whichds = dataset
                    break
        Ui_MainWindow.removeTab(self, Ui_MainWindow.iIndex)
        Ui_MainWindow.indMetrics = QtWidgets.QTabWidget()
        Ui_MainWindow.iIndex = self.addTab(Ui_MainWindow.indMetrics,
                                 "Individual metrics")
        Ui_MainWindow.createGraph(self, whichds)

    def sample_change(self, text):
        Ui_MainWindow.sampleSelected = text
        for dataset in range(len(Ui_MainWindow.NumericMetrics)):
                if Ui_MainWindow.element in Ui_MainWindow.metrics[dataset].columns:
                    whichds = dataset
                    break

        Ui_MainWindow.removeTab(self, Ui_MainWindow.iIndex)
        Ui_MainWindow.indMetrics = QtWidgets.QTabWidget()
        Ui_MainWindow.iIndex = self.addTab(Ui_MainWindow.indMetrics,
                                 "Individual metrics")
        Ui_MainWindow.createGraph(self, whichds)

    def checkColumnNumberForPCA(self):
        if(len(Ui_MainWindow.NumericMetrics[0].columns) < 3):
            QtWidgets.QMessageBox.warning(self, "Warning:", "There are less than three \
                              numeric columns in the dataset. PCA will not \
                              be performed.")
            return 0
        else: 
            return 1

    def checkSampleNumberForPCA(self):
        if(len(FileInput.BrowseWindow.currentDataset.index) < 4):
            QtWidgets.QMessageBox.warning(self, "Warning:", "There are less than three samples in the dataset. PCA will not be performed.")
            return 0
        else:
            return 1


    def enable_legend(metric):
        IndividualMetrics.MyIndMetricsCanvas.ShowLegend(metric)

    def disable_legend(metric):
        IndividualMetrics.MyIndMetricsCanvas.HideLegend(metric)

    @pyqtSlot()
    def onLongitudinalClicked(self):
        Ui_MainWindow.DisableAnalysisButtons(self)
        Ui_MainWindow.predictionArea = [0, 0, 0, 0]
        # Bools to keep track:
        Ui_MainWindow.goodPredicted = False
        Ui_MainWindow.badPredicted = False
        Ui_MainWindow.goodpredictionList = []
        Ui_MainWindow.badpredictionList = []
        # InputtingFile:
        QtWidgets.QMessageBox.about(Ui_MainWindow.tab,  "You have selected Longitudinal analysis.",
                          "For this supervised approach you will need to provide training and test set data that contains both good and bad quality data. It is imperitive that you have high confidence in the training set and we recommend that you run PCA on the set to ascertain that there are no outliers. \n You will be asked to select a folder which contains corresponding pepxml files and QuaMeter/SwaMe output files for training set selection. Then you will be presented with a graph on which you should separate good from bad. Next you will do the same for the test set after which you will be presented with the model fit results.")
        
        FileInput.BrowseWindow.__init__(FileInput.BrowseWindow)
        TrainingSetFiles = FileInput.BrowseWindow.GetTrainingSetFiles(self)
        Ui_MainWindow.TrainingSetTable = pd.DataFrame(columns = ["Filename","Number of Distinct peptides","Number of spectra identified"])
        
        if TrainingSetFiles:
            Ui_MainWindow.TrainingSetTable = pepXMLReader.pepXMLReader.parsePepXML(self, TrainingSetFiles)
            Ui_MainWindow.TrainingOrTestSet = QtWidgets.QTabWidget()
            Ui_MainWindow.TrainingOrTestSet.setStyleSheet("margin: 2px")
            Ui_MainWindow.sIndex = self.addTab(Ui_MainWindow.TrainingOrTestSet,"Setting up the training set:")
            
            Ui_MainWindow.CreateTrainingTab(self)
            self.setCurrentIndex(Ui_MainWindow.sIndex)
        

    def onhover(event):
        vis = PCAGraph.annot.get_visible()
        if event.inaxes == PCAGraph.ax:
            cont, ind = PCAGraph.fig.contains(event)
            if cont:
                Ui_MainWindow.update_annot(event)
                PCAGraph.annot.set_visible(True)
                PCAGraph.fig.canvas.draw_idle()
                return
        if vis:
            PCAGraph.annot.set_visible(False)
            PCAGraph.fig.canvas.draw_idle()

    def update_annot(event):
        pos = {event.xdata, event.ydata}
        closestx = np.unravel_index((np.abs(PCA.plotdata - event.xdata))
                                    .argmin(), PCA.plotdata.shape)
        PCAGraph.annot.xyann = (PCA.plotdata[closestx[0], 0],
                                PCA.plotdata[closestx[0], 1])
        samplenames = DataPreparation.DataPrep.FindRealSampleNames(
            Ui_MainWindow, FileInput.BrowseWindow.currentDataset.index)
        if(len(samplenames) != len(set(samplenames))):
            # if there are duplicates in the filenames column like RTsegments
            # or per swath metrics
            sampleNameColumn1Combination = samplenames[closestx[0]] + "-" \
                + str(FileInput.BrowseWindow.currentDataset.iloc[closestx[0], 1])
            text = sampleNameColumn1Combination.format(PCA.plotdata[
                                                       closestx[0], 0],
                                                       PCA.plotdata[
                                                       closestx[0], 1])
        else:
            text = samplenames[closestx[0]].format(
                PCA.plotdata[closestx[0], 0],
                PCA.plotdata[closestx[0], 1])
        PCAGraph.annot.set_text(text)

    def CreateTrainingTab(self):
        # Create the tab which will contain the graph:
        Ui_MainWindow.tplot = FigureCanvas
        try:
                Ui_MainWindow.TrainingSetPlot 
                Ui_MainWindow.TrainingSetPlot .clear()
        except:
                Ui_MainWindow.TrainingSetPlot  = None
        Ui_MainWindow.TrainingSetPlot = RFSelectionPlots.RFSelectionPlots( Ui_MainWindow.TrainingSetTable, "training") # element = column index used for the y-value
        vbox = QtWidgets.QVBoxLayout(Ui_MainWindow.TrainingOrTestSet)
        hbox1 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingOrTestSet)
        hbox1.addStretch()
        Ui_MainWindow.TrainingOrTestSet.PlotLabel = QtWidgets.QLabel(Ui_MainWindow.TrainingOrTestSet)
        Ui_MainWindow.TrainingOrTestSet.PlotLabel.setText(
                "Graph of input data - Please draw a rectangle over the samples you would like to select for the guide set:")
        font = QtGui.QFont()
        font.setPointSize(18)
        hbox1.addWidget(Ui_MainWindow.TrainingOrTestSet.PlotLabel)
        hbox1.addStretch()
        vbox.addLayout(hbox1)
        hbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingOrTestSet)
        hbox2.addStretch()
        hbox2.addWidget(Ui_MainWindow.TrainingSetPlot)
        hbox2.addStretch()
        vbox.addLayout(hbox2)
        hbox3 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingOrTestSet)
        hbox3.addStretch()
        Ui_MainWindow.TrainingOrTestSet.badbtn = QtWidgets.QPushButton(
                'This is my selection for suboptimal quality.',
                Ui_MainWindow.TrainingOrTestSet)
        Ui_MainWindow.TrainingOrTestSet.badbtn.setEnabled(False)
        hbox3.addWidget(Ui_MainWindow.TrainingOrTestSet.badbtn)
        hbox3.addStretch()
        vbox.addLayout(hbox3)
        hbox4 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingOrTestSet)
        vbox.addLayout(hbox4)
        vbox.addStretch()

            # Create full training set
        Ui_MainWindow.TrainingOrTestSet.badbtn.clicked.connect(lambda: RandomForest.RandomForest.computeTrainingSamplesFromArea(self))
        
    def printModelResults(self, performance, results, model):
        Ui_MainWindow.removeTab(self, Ui_MainWindow.sIndex)
        print(Ui_MainWindow.currentIndex(self))
        Ui_MainWindow.setCurrentIndex(self,0)
        
        Ui_MainWindow.TrainingOrTestSet = QtWidgets.QTabWidget()
        Ui_MainWindow.sIndex = self.addTab(Ui_MainWindow.TrainingOrTestSet,"Random Forest Results:")
        Ui_MainWindow.TrainingOrTestSet.setStyleSheet("background-color: gainsboro; ")
        
        # -------------------------Metrics Frame Layout ------------------------------------
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame = QtWidgets.QFrame(Ui_MainWindow.TrainingOrTestSet)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.setStyleSheet("background-color: rgb(245,245,245); margin:2px;")

        
        #Labels declare:
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MainLabel = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MainLabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MainLabel.setText("Performance metrics:")
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MainLabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MSELabel = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MSELabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MSELabel.setText("MSE:")
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MSELabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MSEresults = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MSEresults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MSEresults.setText(str(round(performance._metric_json["MSE"],4)))
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.RMSELabel = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.RMSELabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.RMSELabel.setText("RMSE:")
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.RMSELabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.RMSEresults = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.RMSEresults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.RMSEresults.setText(str(round(performance._metric_json["RMSE"],4)))        
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.R2Label = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.R2Label.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.R2Label.setText("R2:")
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.R2Label.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.R2results = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.R2results.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.R2results.setText(str(round(performance._metric_json["r2"],4)))        
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.LLLabel = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.LLLabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.LLLabel.setText("logloss:")
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.LLLabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.LLresults = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.LLresults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.LLresults.setText(str(round(performance._metric_json["logloss"],4)))       
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AUCLabel = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AUCLabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AUCLabel.setText("AUC:")
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AUCLabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AUCresults = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AUCresults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AUCresults.setText(str(round(performance._metric_json["AUC"],4)))            
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.GINILabel = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.GINILabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.GINILabel.setText("GINI:")
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.GINILabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.GINIresults = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.GINIresults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.GINIresults.setText(str(round(performance._metric_json["Gini"],4)))     
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MPCELabel = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MPCELabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MPCELabel.setText("Mean per class error:")
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MPCELabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MPCEresults = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MPCEresults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MPCEresults.setText(str(round(performance._metric_json["mean_per_class_error"],4)))    
 
                
        #Layout within Frame:
        pvbox = QtWidgets.QVBoxLayout(Ui_MainWindow.TrainingOrTestSet.MetricsFrame)
        phbox1 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingOrTestSet.MetricsFrame)
        phbox1.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MainLabel)
        pvbox.addLayout(phbox1)
        phbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingOrTestSet.MetricsFrame)
        phbox2.addStretch()
        pgrid = QtWidgets.QGridLayout(Ui_MainWindow.TrainingOrTestSet.MetricsFrame)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MainLabel,0,0,1,8)
        
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MSELabel,1,0,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MSEresults,1,1,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.RMSELabel,1,3,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.RMSEresults,1,4,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.R2Label,1,6,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.R2results,1,7,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.LLLabel,1,9,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.LLresults,1,10,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AUCLabel,1,12,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AUCresults,1,13,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.GINILabel,1,15,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.GINIresults,1,16,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MPCELabel,1,18,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MPCEresults,1,19,1,1)
        phbox2.addLayout(pgrid)
        phbox2.addStretch()
        pvbox.addLayout(phbox2)
    
        # -------------------------Results Layout ------------------------------------
        #Frame declare:
         
        Ui_MainWindow.TrainingOrTestSet.ResultsFrame = QtWidgets.QFrame(Ui_MainWindow.TrainingOrTestSet)
        Ui_MainWindow.TrainingOrTestSet.ResultsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Ui_MainWindow.TrainingOrTestSet.ResultsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Ui_MainWindow.TrainingOrTestSet.ResultsFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")

        #Labels declare:
        Ui_MainWindow.TrainingOrTestSet.ResultsFrame.MainLabel = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.ResultsFrame.MainLabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.ResultsFrame.MainLabel.setText("Random Forest results:")
        Ui_MainWindow.TrainingOrTestSet.ResultsFrame.MainLabel.setFont(Ui_MainWindow.boldfont)        
        Ui_MainWindow.TrainingOrTestSet.ResultsFrame.predictedLabel = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.ResultsFrame.predictedLabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.ResultsFrame.predictedLabel.setText("The following samples were predicted by Random Forest to resemble the group labelled 'bad' quality:")
        Ui_MainWindow.TrainingOrTestSet.ResultsFrame.predictedLabel.setFont(Ui_MainWindow.boldfont)        

        #Bad samples grid:
        badsamplesgrid = QtWidgets.QGridLayout()
        badsamplesgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.ResultsFrame.predictedLabel,0,0)
        badlist = results[results['predict']=='B'].index
        for i in range(0,len(badlist)):
            label = QtWidgets.QLabel()
            label.setText(badlist[i])
            currentrow = math.floor(i/5)
            currentcolumn = i-currentrow*5
            badsamplesgrid.addWidget(label,currentrow,currentcolumn)

                        
        #Layout within Frame:
        rvbox = QtWidgets.QVBoxLayout(Ui_MainWindow.TrainingOrTestSet.ResultsFrame)
        rhbox1 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingOrTestSet.ResultsFrame)
        rhbox1.addWidget(Ui_MainWindow.TrainingOrTestSet.ResultsFrame.MainLabel)
        rvbox.addLayout(rhbox1)        
        rhbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingOrTestSet.ResultsFrame)
        rhbox2.addLayout(badsamplesgrid)
        rvbox.addLayout(rhbox2)

               
        #-------------------------plots---------------------------------
        Ui_MainWindow.TrainingOrTestSet.PlotFrame = QtWidgets.QFrame(Ui_MainWindow.TrainingOrTestSet)
        Ui_MainWindow.TrainingOrTestSet.PlotFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Ui_MainWindow.TrainingOrTestSet.PlotFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Ui_MainWindow.TrainingOrTestSet.PlotFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")


        # plot
        RFPlot = RandomForest.RandomForest(results)
        FeaturePlot = FeatureImportancePlot.FeaturePlot(model)
        fgrid = QtWidgets.QGridLayout(Ui_MainWindow.TrainingOrTestSet.PlotFrame)
        fgrid.addWidget(FeaturePlot,0,0,1,1)          
        fgrid.addWidget(RFPlot,1,0,1,1)
        
        # -------------------------Complete Tab Layout ------------------------------------
        # Tab Layout
        scroll = QtWidgets.QScrollArea()
        placementwidget = QtWidgets.QWidget()
        placementwidget.setFixedWidth(750)
        placementwidget.setFixedHeight(2000)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame,0,0,1,1)   
        grid.addWidget(Ui_MainWindow.TrainingOrTestSet.ResultsFrame,1,0,2,1) 
        grid.addWidget(Ui_MainWindow.TrainingOrTestSet.PlotFrame,3,0,9,1)
        placementwidget.setLayout(grid)
        scroll.setWidget(placementwidget)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #scroll.setMinimumHeight(2000)

        scroll.setWidgetResizable(True)

        vLayout = QtWidgets.QVBoxLayout(Ui_MainWindow.TrainingOrTestSet)
        vLayout.addWidget(scroll)
        #vLayout.setGeometry()
     
        RandomForest.fig.canvas.mpl_connect("motion_notify_event", Ui_MainWindow.RFonhover)                        
        self.setCurrentIndex(Ui_MainWindow.sIndex)
        
    def RFonhover(event):
        vis = RandomForest.annot.get_visible()
        if event.inaxes == RandomForest.ax:
            cont, ind = RandomForest.fig.contains(event)
            if cont:
                Ui_MainWindow.RFupdate_annot(event)
                RandomForest.annot.set_visible(True)
                RandomForest.fig.canvas.draw_idle()
                return
        if vis:
            RandomForest.annot.set_visible(False)
            RandomForest.fig.canvas.draw_idle()
            
    def RFupdate_annot(event):
        closestyIndex = np.abs(RandomForest.badset["B"] - event.ydata).argmin()
        closesty = RandomForest.badset["B"].loc[closestyIndex]
        badsetclosey = RandomForest.badset[RandomForest.badset['B']==closesty]
        closestxIndex = np.abs(badsetclosey['X'] - event.xdata).argmin()        
        closestx = RandomForest.badset["X"].loc[closestxIndex]
        RandomForest.annot.xyann = (closestx , closesty)
        RandomForest.annot.set_text(closestxIndex)
        
    def CalculateOutliers(self):
        sampleSize = range(len(FileInput.BrowseWindow.currentDataset.index))
        PCA.Distances = self.calculateDistanceMatrix(PCA.finalDf)
        Ui_MainWindow.tab.AnalysisFrame.progress1.setValue(60)
        #self.metrics.index = self.metrics.iloc[:,0]
        medianDistances = Ui_MainWindow.createMedianDistances(self, sampleSize)
        outlierDistance = Ui_MainWindow.calculateOutLierDistances(self, medianDistances)
        Ui_MainWindow.tab.AnalysisFrame.progress1.setValue(65)

        for iterator in sampleSize:
            medianDistances["MedianDistance"][iterator] = np.percentile(PCA.Distances[iterator], 50)
        print(medianDistances)      
        Q1 = np.percentile(medianDistances["MedianDistance"], 25)
        Q3 =np.percentile(medianDistances["MedianDistance"], 75)
        IQR = Q3-Q1
        outlierDistance = Q3 + 1.5*IQR
        Ui_MainWindow.tab.AnalysisFrame.progress1.setValue(65)
       #Zscores:
        from scipy.stats import zscore
        medianDistances["zScore"] = zscore(medianDistances["MedianDistance"])
        medianDistances["outlier"]= medianDistances["zScore"].apply(
        lambda x: x <= -3.5 or x >= 3.5
        )
        print("The following runs were identified as candidates for possible outliers based on their z-scores:")
        Q3 = np.percentile(medianDistances["MedianDistance"], 75)  # Q3

        Ui_MainWindow.tab.AnalysisFrame.progress1.setValue(75)
        Outliers = medianDistances[medianDistances["outlier"]]
        return Outliers

    def createMedianDistances(self, sampleSize):
        medianDistances = pd.DataFrame()
        if FileInput.BrowseWindow.currentDataset.index[0] != 1:
            medianDistances["Filename"] = FileInput.BrowseWindow.currentDataset.index
        else:
            medianDistances["Filename"] = FileInput.BrowseWindow.currentDataset["Filename"]
        medianDistances["MedianDistance"] = 'default value'
        for iterator in sampleSize:
            medianDistances["MedianDistance"][iterator] = np.percentile(
                PCA.Distances[iterator], 50)
        return medianDistances

    def calculateOutLierDistances(self, medianDistances):
        Q1 = np.percentile(medianDistances["MedianDistance"], 25)
        Q3 = np.percentile(medianDistances["MedianDistance"], 75)
        IQR = Q3 - Q1
        outlierDistance = Q3 + 1.5*IQR
        return outlierDistance


    def calculateDistanceMatrix(self, df):
        PCA.Distances = pd.DataFrame(distance_matrix(
            df.values, df.values, p=2),
            index=df.index, columns=df.index)
        return PCA.Distances

    def moveToPrediction(self):
        items = self.RandomForest.items
        for element in range(0, len(items)):
            QtWidgets.QListWidgetItem(items[element].text(),
                                      self.
                                      RandomForest.predictionList)
        self.RandomForest.backbtn.setEnabled(True)
        self.RandomForest.sourceList.setEnabled(True)
        if(len(items) > 0):
            self.RandomForest.badbtn.setEnabled(True)
        return

    def moveToSource(self):
        Ui_MainWindow.RandomForest.predictionList.clear()
        Ui_MainWindow.RandomForest.badbtn.setEnabled(False)

    def sourceSelectionChanged(self):
        Ui_MainWindow.RandomForest.items = \
            self.RandomForest.sourceList.selectedItems()
        Ui_MainWindow.RandomForest.predictionbtn.setEnabled(True)

    def retranslateUi2(self):
        _translate = QtCore.QCoreApplication.translate
        array = range(1, len(Ui_MainWindow.outlierlist), 1)
        Ui_MainWindow.outlierlistLabel.setText(
            "The following runs are suggested as candidates for being possible outliers: ")
        Ui_MainWindow.PCA.plotlabel.setText(
            "Principal components analysis of quality metrics for outlier detection:")
        font = QtGui.QFont()
        font.setPointSize(18)
        if(len(Ui_MainWindow.outlierlist) > 0):
            outlierstring = Ui_MainWindow.outlierlist.array[0]
            for element in array:
                outlierstring = str(outlierstring) + "\n" + str(Ui_MainWindow.outlierlist.array[element])
        else:
            outlierstring = "No outliers found."
        Ui_MainWindow.OutlierSamples.setText(outlierstring)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        Ui_MainWindow.tab.AnalysisFrame.Outliers.setText(_translate("MainWindow",
                                           "Detect Outliers"))
        Ui_MainWindow.tab.AnalysisFrame.IndMetrics.setText(_translate("MainWindow",
                                             "Individual metrics"))
        Ui_MainWindow.tab.AnalysisFrame.Longitudinal.setText(_translate("MainWindow",
                                               "Longitudinal analysis"))
        Ui_MainWindow.tab.UploadFrame.browse.setText(_translate("MainWindow", "Browse: "))
        Ui_MainWindow.tab.UploadFrame.leftFrame.QuaMeterbutton.setText(_translate("MainWindow", "Generate quality metrics with QuaMeter ID-Free"))
        Ui_MainWindow.tab.UploadFrame.rightFrame.SwaMebutton.setText(_translate("MainWindow", "Generate quality metrics with SwaMe"))
        Ui_MainWindow.tab.UploadFrame.filename.setText(_translate("MainWindow", "   File...                  "))
        Ui_MainWindow.tab.UploadFrame.filename.setStyleSheet("background-color: white;")
        Ui_MainWindow.tab.UploadFrame.InstructionLabel.setText(_translate("MainWindow", "Choose between running QuaMeter and SwaMe directly or upload previous results:"))
        Ui_MainWindow.tab.UploadFrame.InstructionLabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.tab.UploadFrame.InputLabel.setText(_translate("MainWindow", "File Input"))
        Ui_MainWindow.tab.UploadFrame.InputLabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.tab.UploadFrame.uploadLabel.setText(_translate("MainWindow", "Upload a file (Either json, csv or tsv format):"))
        Ui_MainWindow.tab.UploadFrame.uploadLabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.tab.AnalysisFrame.analysisLabel.setText(_translate("MainWindow", "Experiment Analysis"))
        Ui_MainWindow.tab.AnalysisFrame.analysisLabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.tab.AnalysisFrame.chooseLabel.setText(_translate("MainWindow", "Choose the analysis you would like to conduct:"))
        Ui_MainWindow.DisableAnalysisButtons(self)
        Ui_MainWindow.DisableQuaMeterArguments(self)
        Ui_MainWindow.DisableSwaMeArguments(self)
        Ui_MainWindow.tab.UploadFrame.browse.setEnabled(True)
