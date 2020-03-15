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
         
         
        Ui_MainWindow.tab.UploadFrame.leftFrame = QFrame(Ui_MainWindow.tab.UploadFrame)
        Ui_MainWindow.tab.UploadFrame.leftFrame.setFrameShape(QFrame.StyledPanel)
        Ui_MainWindow.tab.UploadFrame.leftFrame.setFrameShadow(QFrame.Raised)
        Ui_MainWindow.tab.UploadFrame.leftFrame.setStyleSheet("background-color: rgb(192,192,192); margin:5px;")
        

        Ui_MainWindow.tab.UploadFrame.rightFrame = QFrame(Ui_MainWindow.tab.UploadFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.setFrameShape(QFrame.StyledPanel)
        Ui_MainWindow.tab.UploadFrame.rightFrame.setFrameShadow(QFrame.Raised)
        Ui_MainWindow.tab.UploadFrame.rightFrame.setStyleSheet("background-color: rgb(192,192,192); margin:5px;")

        
        Ui_MainWindow.tab.AnalysisFrame = QFrame(self)
        Ui_MainWindow.tab.AnalysisFrame.setFrameShape(QFrame.StyledPanel)
        Ui_MainWindow.tab.AnalysisFrame.setFrameShadow(QFrame.Raised)
        Ui_MainWindow.tab.AnalysisFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")


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
        #Ui_MainWindow.tab.UploadFrame.leftFrame.Dir = QtWidgets.QRadioButton("Whole Directory")
        

        #Widget stylesheets:
        Ui_MainWindow.tab.UploadFrame.leftFrame.BrowseButton.setStyleSheet("background-color: rgb(240,240,240);")

        #Widget texts:
        Ui_MainWindow.tab.UploadFrame.leftFrame.BrowseButton.setText("Browse ")
        Ui_MainWindow.tab.UploadFrame.leftFrame.files.setText("File:")
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
        QuaMetervbox.addLayout(hbox4)

        #-------------------------------------------------SwaMeLayout--------------------------------------------------------

        #Widget declaring:
        Ui_MainWindow.tab.UploadFrame.rightFrame.SwaMebutton = QtWidgets.QPushButton(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton = QtWidgets.QPushButton(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.Sfiles = QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SfileList = QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.divisionLabel= QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.divisionTextBox= QLineEdit(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.MTLabel= QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.MTTextBox = QLineEdit(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.RTLabel= QtWidgets.QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.RTTextBox = QLineEdit(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SRUNButton = QtWidgets.QPushButton(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRT = QtWidgets.QRadioButton("iRT")
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTtoleranceLabel =QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminintensityLabel =QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminpeptidesLabel =QLabel(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTtoleranceTB =QLineEdit(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminintensityTB =QLineEdit(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.iRTminpeptidesTB =QLineEdit(Ui_MainWindow.tab.UploadFrame.rightFrame)
        Ui_MainWindow.tab.UploadFrame.rightFrame.textedit =QtWidgets.QTextEdit(readOnly=True)
        Ui_MainWindow.IRTinputFile = None


        #Widget stylesheets:
        Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.tab.UploadFrame.rightFrame.SwaMebutton.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton.setFixedHeight(30)
        Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton.setFixedHeight(30)


        #Widget texts:
        Ui_MainWindow.tab.UploadFrame.rightFrame.SBrowseButton.setText("Browse ")
        Ui_MainWindow.tab.UploadFrame.rightFrame.Sfiles.setText("File: ")
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
        
        vbox.setAlignment(QtCore.Qt.AlignLeft)
        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(self)

    def enable_slot():
        PCAGraph.PCAGraph.loadingsToggledOn(Ui_MainWindow)
        Ui_MainWindow.PCA.LoadingsProgressBar.setValue(100)

    def disable_slot():
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
        global metrics
        if inputFile:
            filepath = FileInput.BrowseWindow.FileCheck(inputFile)
            Ui_MainWindow.metrics = FileInput.BrowseWindow.metricsParsing(inputFile)
            #Ui_MainWindow.checkColumnLength(self)
            Ui_MainWindow.metrics.set_index(Ui_MainWindow.metrics.iloc[:,0])
            DataPreparation.DataPrep.ExtractNumericColumns(self, self.metrics)
            DataPreparation.DataPrep.RemoveLowVarianceColumns(self)
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

                        sampleToVariableRatio = PCA.PCA.\
                            calculateSampleToVariableRatio(self, FileInput.BrowseWindow.currentDataset)
        
       
                        PCA.PCA.CreatePCAGraph(FileInput.BrowseWindow.currentDataset)
                        Ui_MainWindow.tab.AnalysisFrame.progress1.setValue(51)
                        # Need to correctly calculate euc distance in N dimension
                        outliers = Ui_MainWindow.CalculateOutliers(self)
                        Ui_MainWindow.outlierlist = outliers["Filename"]

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
                            lambda x: Ui_MainWindow.enable_slot()
                            if x else Ui_MainWindow.disable_slot())
                        Ui_MainWindow.PCA.LoadingsProgressBar = QtWidgets.QProgressBar()
                        Ui_MainWindow.PCA.LoadingsProgressBar.setGeometry(200, 80, 250, 20)

                        vbox2 = QtWidgets.QVBoxLayout(Ui_MainWindow.PCA)
                        hbox = QtWidgets.QHBoxLayout(Ui_MainWindow.PCA)
                        vbox3 = QtWidgets.QVBoxLayout(Ui_MainWindow.PCA)
                        vbox3.addStretch()
                        vbox3.addWidget(Ui_MainWindow.outlierlistLabel)
                        vbox3.addWidget(Ui_MainWindow.OutlierSamples)
                        vbox3.addWidget(Ui_MainWindow.PCA.Checkboxlabel)
                        vbox3.addWidget(Ui_MainWindow.PCA.Checkbox)
                        vbox3.addWidget(Ui_MainWindow.PCA.LoadingsProgressBar)
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
    def onIRTClicked(self):
         Ui_MainWindow.EnableSwaMeIRTArguments(self)
         Ui_MainWindow.IRTinputFile = FileInput.BrowseWindow.GetIRTInputFile(Ui_MainWindow)

    @pyqtSlot()
    def onIndMetricsClicked(self):
        Ui_MainWindow.DisableAnalysisButtons(self)
        Ui_MainWindow.tab.AnalysisFrame.progress2.show()
        Ui_MainWindow.tab.AnalysisFrame.progress2.setValue(10)
        NumericMetrics = FileInput.BrowseWindow.currentDataset
        global element
        lw = 2
        Ui_MainWindow.tab.AnalysisFrame.progress2.setValue(33)
        global iIndex
        last=False
        for element in range(len(NumericMetrics.columns)):
            Ui_MainWindow.indMetrics = QtWidgets.QTabWidget()
            iIndex = self.addTab(Ui_MainWindow.indMetrics,
                                 NumericMetrics.columns[element])
            if element == len(NumericMetrics.columns):
                last = True
            vbox = QtWidgets.QVBoxLayout(Ui_MainWindow.indMetrics)
            hbox1 = QtWidgets.QHBoxLayout(Ui_MainWindow.indMetrics)
            hbox1.addStretch()
            Ui_MainWindow.indMetrics.indPlotLabel = QtWidgets.QLabel(
                  Ui_MainWindow.indMetrics)
            Ui_MainWindow.indMetrics.indPlotLabel.setText(
                  NumericMetrics.columns[element])
            Ui_MainWindow.indMetrics.indPlotLabel.setFont(
                    Ui_MainWindow.boldfont)
            hbox1.addWidget(Ui_MainWindow.indMetrics.indPlotLabel)
            hbox1.addStretch()
            vbox.addLayout(hbox1)
            hbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.indMetrics)
            hbox2.addStretch()
            indMetPlot = IndividualMetrics.MyIndMetricsCanvas(
                    self.metrics,
                    FileInput.BrowseWindow.currentDataset, element, False, False)
            hbox2.addWidget(indMetPlot)
            hbox2.addStretch()
            vbox.addLayout(hbox2)

        #Ui_MainWindow.legend.show()
        Ui_MainWindow.EnableAnalysisButtons(self)
        Ui_MainWindow.tab.progress2.setValue(100)
        self.setCurrentIndex(iIndex)

    def checkColumnNumberForPCA(self):
        if(len(FileInput.BrowseWindow.currentDataset.columns) < 3):
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
                          "You will be asked to select a separated value file (.tsv or .csv) containing two columns. The first should contain the filename and the second the metric on which you would like to separate good quality data from bad, for example ID's. From the corresponding graph you will select which samples are to be used for the guide set.")
        
        FileInput.BrowseWindow.__init__(FileInput.BrowseWindow, Ui_MainWindow)
        TrainingSetFile = FileInput.BrowseWindow.GetTrainingSetFile(Ui_MainWindow)
        if TrainingSetFile:
            filepath = FileInput.BrowseWindow.TrainingSetParse(
                TrainingSetFile)
            Ui_MainWindow.TrainingSetTable = \
                FileInput.BrowseWindow.metricsParsing(TrainingSetFile)
            Ui_MainWindow.TrainingSet = QtWidgets.QTabWidget()
            Ui_MainWindow.sIndex = self.addTab(Ui_MainWindow.TrainingSet,"Setting up the guide set:")
            self.CreateRandomForestTab()
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

    def CreateRandomForestTab(self):
        # Create the tab which will contain the graph:
        TrainingSetPlot = IndividualMetrics.MyIndMetricsCanvas(
            Ui_MainWindow.TrainingSetTable, Ui_MainWindow.TrainingSetTable,
            1, True)  # element = column index used for the y-value
        vbox = QtWidgets.QVBoxLayout(Ui_MainWindow.TrainingSet)
        hbox1 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingSet)
        hbox1.addStretch()
        Ui_MainWindow.TrainingSet.PlotLabel = QtWidgets.QLabel(
            Ui_MainWindow.TrainingSet)
        Ui_MainWindow.TrainingSet.PlotLabel.setText(
            "Graph of input data - Please draw a rectangle over the samples you would like to select for the guide set:")
        font = QtGui.QFont()
        font.setPointSize(18)
        hbox1.addWidget(Ui_MainWindow.TrainingSet.PlotLabel)
        hbox1.addStretch()
        vbox.addLayout(hbox1)
        hbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingSet)
        hbox2.addStretch()
        hbox2.addWidget(TrainingSetPlot)
        hbox2.addStretch()
        vbox.addLayout(hbox2)
        hbox3 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingSet)
        hbox3.addStretch()
        Ui_MainWindow.TrainingSet.goodbtn = QtWidgets.QPushButton(
            'This is my selection for desired quality.',
            Ui_MainWindow.TrainingSet)
        Ui_MainWindow.TrainingSet.goodbtn.setEnabled(False)
        Ui_MainWindow.TrainingSet.badbtn = QtWidgets.QPushButton(
            'This is my selection for suboptimal quality.',
            Ui_MainWindow.TrainingSet)
        Ui_MainWindow.TrainingSet.badbtn.setEnabled(False)
        hbox3.addWidget(Ui_MainWindow.TrainingSet.goodbtn)
        hbox3.addWidget(Ui_MainWindow.TrainingSet.badbtn)
        hbox3.addStretch()
        vbox.addLayout(hbox3)
        hbox4 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingSet)
        vbox.addLayout(hbox4)
        vbox.addStretch()

        # Start prediction
        Ui_MainWindow.TrainingSet.goodbtn.clicked.connect(lambda: RandomForest.RandomForest.computeSelectedSamplesFromArea(RandomForest.RandomForest, "good"))
        Ui_MainWindow.TrainingSet.badbtn.clicked.connect(lambda: RandomForest.RandomForest.computeSelectedSamplesFromArea(RandomForest.RandomForest, "bad"))

    def CalculateOutliers(self):
        sampleSize = range(len(FileInput.BrowseWindow.currentDataset.index))
        PCA.Distances = self.calculateDistanceMatrix(PCA.finalDf)
        Ui_MainWindow.tab.AnalysisFrame.progress1.setValue(60)
        #self.metrics.index = self.metrics.iloc[:,0]
        medianDistances = Ui_MainWindow.createMedianDistances(self, sampleSize)
        outlierDistance = Ui_MainWindow.calculateOutLierDistances(self, medianDistances)
        Ui_MainWindow.tab.AnalysisFrame.progress1.setValue(65)
        Q3 = np.percentile(medianDistances["MedianDistance"], 75)  # Q3

        medianDistances["outlier"] = medianDistances["MedianDistance"].apply(
            lambda x: x >= Q3 + outlierDistance
        )
        print("The following runs were identified as outliers \
        based on their z-scores:")

        Ui_MainWindow.tab.AnalysisFrame.progress1.setValue(75)
        Outliers = medianDistances[medianDistances["outlier"]]
        return Outliers

    def createMedianDistances(self, sampleSize):
        medianDistances = pd.DataFrame()
        medianDistances["Filename"] = FileInput.BrowseWindow.currentDataset.index
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
            self.RandomForest.goodbtn.setEnabled(True)
            self.RandomForest.badbtn.setEnabled(True)
        return

    def moveToSource(self):
        Ui_MainWindow.RandomForest.predictionList.clear()
        Ui_MainWindow.RandomForest.goodbtn.setEnabled(False)
        Ui_MainWindow.RandomForest.badbtn.setEnabled(False)

    def sourceSelectionChanged(self):
        Ui_MainWindow.RandomForest.items = \
            self.RandomForest.sourceList.selectedItems()
        Ui_MainWindow.RandomForest.predictionbtn.setEnabled(True)

    def retranslateUi2(self):
        _translate = QtCore.QCoreApplication.translate
        array = range(1, len(Ui_MainWindow.outlierlist), 1)
        Ui_MainWindow.outlierlistLabel.setText(
            "The following runs were identified as outliers: ")
        Ui_MainWindow.PCA.plotlabel.setText(
            "Principal components analysis of quality metrics for outlier detection:")
        font = QtGui.QFont()
        font.setPointSize(18)
        if(len(Ui_MainWindow.outlierlist) > 0):
            outlierstring = Ui_MainWindow.outlierlist.array[0]
            for element in array:
                outlierstring = outlierstring + "\n" \
                    + Ui_MainWindow.outlierlist.array[element]
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
        Ui_MainWindow.tab.AnalysisFrame.analysisLabel.setText(_translate("MainWindow", "File Analysis"))
        Ui_MainWindow.tab.AnalysisFrame.analysisLabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.tab.AnalysisFrame.chooseLabel.setText(_translate("MainWindow", "Choose the analysis you would like to conduct:"))
        Ui_MainWindow.DisableAnalysisButtons(self)
        Ui_MainWindow.DisableQuaMeterArguments(self)
        Ui_MainWindow.DisableSwaMeArguments(self)
        Ui_MainWindow.tab.UploadFrame.browse.setEnabled(True)
