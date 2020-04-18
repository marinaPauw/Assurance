import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
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
import PDFWriter
import tempfile
import datetime


class Ui_MainWindow(QtWidgets.QTabWidget):
    
    def setupUi(self):

        self.setWindowTitle("Assurance")
        self.resize(800,650)
        global now
        global tempDir
        Ui_MainWindow.outliersDetected = False
        Ui_MainWindow.indMetricsGraphed = False
        Ui_MainWindow.RandomForestPerformed = False
        
        now = datetime.datetime.today()
        tempDir = tempfile.TemporaryDirectory()
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
        UploadFrame = QtWidgets.QFrame(self)
        UploadFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        UploadFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        UploadFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")
         
         
        Ui_MainWindow.leftFrame = QtWidgets.QFrame(UploadFrame)
        Ui_MainWindow.leftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Ui_MainWindow.leftFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Ui_MainWindow.leftFrame.setStyleSheet("background-color: rgb(192,192,192); margin:5px;")
        

        Ui_MainWindow.rightFrame = QtWidgets.QFrame(UploadFrame)
        Ui_MainWindow.rightFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Ui_MainWindow.rightFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Ui_MainWindow.rightFrame.setStyleSheet("background-color: rgb(192,192,192); margin:5px;")

        Ui_MainWindow.browseFrame = QtWidgets.QFrame(UploadFrame)
        Ui_MainWindow.browseFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Ui_MainWindow.browseFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Ui_MainWindow.browseFrame.setStyleSheet("background-color: rgb(192,192,192); margin:5px;")
        
        AnalysisFrame = QtWidgets.QFrame(self)
        AnalysisFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        AnalysisFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        AnalysisFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")

        OutputFrame = QtWidgets.QFrame(self)
        OutputFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        OutputFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        OutputFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")


        #-------------------------------------------------QuaMeterLayout--------------------------------------------------------
        
        #Widget declaring:
        Ui_MainWindow.BrowseButton = QtWidgets.QPushButton(self.leftFrame)
        Ui_MainWindow.files = QtWidgets.QLabel(self.leftFrame)
        Ui_MainWindow.fileList= QtWidgets.QLabel(self.leftFrame)
        Ui_MainWindow.cpusLabel= QtWidgets.QLabel(self.leftFrame)
        Ui_MainWindow.cpusTextBox = QtWidgets.QLineEdit(self.leftFrame)
        Ui_MainWindow.CLOLabel= QtWidgets.QLabel(self.leftFrame)
        Ui_MainWindow.CLOTextBox = QtWidgets.QLineEdit(self.leftFrame)
        Ui_MainWindow.CUOLabel= QtWidgets.QLabel(self.leftFrame)
        Ui_MainWindow.CUOTextBox = QtWidgets.QLineEdit(self.leftFrame) 
        Ui_MainWindow.RUNButton = QtWidgets.QPushButton(self.leftFrame)
        textedit =QtWidgets.QTextEdit(readOnly=True)
        

        #Widget stylesheets:
        Ui_MainWindow.BrowseButton.setStyleSheet("background-color: rgb(240,240,240);")

        #Widget texts:
        Ui_MainWindow.BrowseButton.setText("Browse ")
        Ui_MainWindow.files.setText("Folder:")
        Ui_MainWindow.cpusLabel.setText("Number of CPU's: ")
        Ui_MainWindow.CLOLabel.setText("m/z Lower Offset:")
        Ui_MainWindow.CUOLabel.setText("m/z Upper Offset:")
        Ui_MainWindow.RUNButton.setText("RUN")


        #QuaMeterGrid:
        #Layout:
        
        QuaMetervbox = QtWidgets.QVBoxLayout(Ui_MainWindow.leftFrame)
        hbox1 = QtWidgets.QHBoxLayout(Ui_MainWindow.leftFrame)
        Qvbox2 = QtWidgets.QVBoxLayout(Ui_MainWindow.leftFrame)
        QhboxFiles = QtWidgets.QHBoxLayout(Ui_MainWindow.leftFrame)
        QhboxFiles.addWidget( Ui_MainWindow.BrowseButton)
        QhboxFiles.addWidget(Ui_MainWindow.files)     
        QhboxFiles.addWidget(Ui_MainWindow.fileList)
        Qvbox2.addLayout(QhboxFiles)
        hbox1.addLayout(Qvbox2)
        hbox1.addStretch()
        QuaMetervbox.addLayout(hbox1)

        hbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.leftFrame)
        hbox2.addWidget(Ui_MainWindow.cpusLabel)
        hbox2.addWidget(Ui_MainWindow.cpusTextBox)
        QuaMetervbox.addLayout(hbox2)
        hbox3 = QtWidgets.QHBoxLayout()
        hbox3.addWidget(Ui_MainWindow.CLOLabel)
        hbox3.addWidget(Ui_MainWindow.CLOTextBox)
        hbox3.addWidget(Ui_MainWindow.CUOLabel)
        hbox3.addWidget(Ui_MainWindow.CUOTextBox)
        QuaMetervbox.addLayout(hbox3)
        hbox4 = QtWidgets.QHBoxLayout()
        hbox4.addWidget(Ui_MainWindow.RUNButton)
        hbox4.addWidget(textedit)
        QuaMetervbox.addLayout(hbox4)
        
        #-------------------------------------------------SwaMeLayout--------------------------------------------------------

        #Widget declaring:
        Ui_MainWindow.SBrowseButton = QtWidgets.QPushButton(Ui_MainWindow.rightFrame)
        Ui_MainWindow.Sfiles = QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.SfileList = QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.divisionLabel= QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.divisionTextBox= QtWidgets.QLineEdit(Ui_MainWindow.rightFrame)
        Ui_MainWindow.MTLabel= QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.MTTextBox = QtWidgets.QLineEdit(Ui_MainWindow.rightFrame)
        Ui_MainWindow.RTLabel= QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.RTTextBox = QtWidgets.QLineEdit(Ui_MainWindow.rightFrame)
        Ui_MainWindow.SRUNButton = QtWidgets.QPushButton(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRT = QtWidgets.QRadioButton("iRT")
        Ui_MainWindow.iRTtoleranceLabel =QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRTminintensityLabel =QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRTminpeptidesLabel =QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRTtoleranceTB =QtWidgets.QLineEdit(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRTminintensityTB =QtWidgets.QLineEdit(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRTminpeptidesTB =QtWidgets.QLineEdit(Ui_MainWindow.rightFrame)
        Ui_MainWindow.rightFrame.textedit =QtWidgets.QTextEdit(readOnly=True)
        Ui_MainWindow.IRTinputFile = None


        #Widget stylesheets:
        Ui_MainWindow.SBrowseButton.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.SBrowseButton.setFixedHeight(30)
        Ui_MainWindow.SBrowseButton.setFixedHeight(30)


        #Widget texts:
        Ui_MainWindow.SBrowseButton.setText("Browse ")
        Ui_MainWindow.Sfiles.setText("Folder: ")
        Ui_MainWindow.divisionLabel.setText("Number of segments to divide the RT into: ")
        Ui_MainWindow.MTLabel.setText("MassTolerance:")
        Ui_MainWindow.RTLabel.setText("RTTolerance:")
        Ui_MainWindow.SRUNButton.setText("RUN")
        Ui_MainWindow.iRTtoleranceLabel.setText("iRTtolerance")
        Ui_MainWindow.iRTminintensityLabel.setText("MinIRTIntensity")
        Ui_MainWindow.iRTminpeptidesLabel.setText("MinIRTpeptides")

        
        #Layout:
        SwaMevbox = QtWidgets.QVBoxLayout(Ui_MainWindow.rightFrame)
        SwaMehbox1 = QtWidgets.QHBoxLayout(Ui_MainWindow.rightFrame)
        SwaMevbox2 = QtWidgets.QVBoxLayout(Ui_MainWindow.rightFrame)
        SwaMehboxf = QtWidgets.QHBoxLayout(Ui_MainWindow.rightFrame)
        SwaMehboxf.addWidget(Ui_MainWindow.SBrowseButton)
        SwaMehboxf.addWidget(Ui_MainWindow.Sfiles)     
        SwaMehboxf.addWidget(Ui_MainWindow.SfileList)
        SwaMevbox2.addLayout(SwaMehboxf)
        SwaMehbox1.addLayout(SwaMevbox2)
        SwaMehbox1.addStretch()
        SwaMevbox.addLayout(SwaMehbox1)
        SwaMehbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.rightFrame)
        SwaMehbox2.addWidget(Ui_MainWindow.divisionLabel)
        SwaMehbox2.addWidget(Ui_MainWindow.divisionTextBox)
        SwaMevbox.addLayout(SwaMehbox2)
        SwaMehbox3 = QtWidgets.QHBoxLayout(Ui_MainWindow.rightFrame)
        SwaMehbox3.addWidget(Ui_MainWindow.MTLabel)
        SwaMehbox3.addWidget(Ui_MainWindow.MTTextBox)
        SwaMehbox3.addWidget(Ui_MainWindow.RTLabel)
        SwaMehbox3.addWidget(Ui_MainWindow.RTTextBox)
        SwaMevbox.addLayout(SwaMehbox3)
        SwaMehbox4 = QtWidgets.QHBoxLayout(Ui_MainWindow.rightFrame)
        SwaMehbox4.addWidget(Ui_MainWindow.iRT)
        SwaMehbox4.addWidget(Ui_MainWindow.iRTtoleranceLabel)
        SwaMehbox4.addWidget(Ui_MainWindow.iRTtoleranceTB)
        SwaMevbox.addLayout(SwaMehbox4)
        SwaMehbox6 = QtWidgets.QHBoxLayout(Ui_MainWindow.rightFrame)
        SwaMehbox6.addWidget(Ui_MainWindow.iRTminintensityLabel)
        SwaMehbox6.addWidget(Ui_MainWindow.iRTminintensityTB)
        SwaMehbox6.addWidget(Ui_MainWindow.iRTminpeptidesLabel)
        SwaMehbox6.addWidget(Ui_MainWindow.iRTminpeptidesTB)
        SwaMevbox.addLayout(SwaMehbox6)
        SwaMehbox7 = QtWidgets.QHBoxLayout(Ui_MainWindow.rightFrame)
        SwaMehbox7.addWidget(Ui_MainWindow.SRUNButton)
        SwaMehbox7.addWidget(Ui_MainWindow.rightFrame.textedit)
        SwaMevbox.addLayout(SwaMehbox7)
        #------------------------------------------------OutputFrame--------------------------------------------------------
        Ui_MainWindow.pdf = QtWidgets.QPushButton(OutputFrame)
        Ui_MainWindow.pdf.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.pdf.setText("Export to PDF")
        Ui_MainWindow.pdf.progress = QtWidgets.QProgressBar()
        Ui_MainWindow.pdf.progress.setGeometry(200, 80, 250, 20)
        
        outputHBOX = QtWidgets.QHBoxLayout(OutputFrame)
        outputHBOX.addStretch()
        outputHBOX.addWidget(Ui_MainWindow.pdf)
        outputHBOX.addWidget(Ui_MainWindow.pdf.progress)
        outputHBOX.addStretch()
        

        #-------------------------------------------------MainLayout--------------------------------------------------------
          #All the buttons MainWindow:
        Ui_MainWindow.browse = QtWidgets.QPushButton(self.tab)
        Ui_MainWindow.browse.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.Outliers = QtWidgets.QPushButton(self.tab)
        Ui_MainWindow.Outliers.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.IndMetrics = QtWidgets.QPushButton(self.tab)
        Ui_MainWindow.IndMetrics.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.Longitudinal = QtWidgets.QPushButton(self.tab)
        Ui_MainWindow.Longitudinal.setStyleSheet("background-color: rgb(240,240,240);")
        
        

        #clicked.connect
        Ui_MainWindow.browse.clicked.connect(self.onBrowseClicked)
        Ui_MainWindow.Outliers.clicked.connect(self.onOutliersClicked)
        Ui_MainWindow.IndMetrics.clicked.connect(self.onIndMetricsClicked)
        Ui_MainWindow.Longitudinal.clicked.connect(self.onLongitudinalClicked)
        Ui_MainWindow.iRT.toggled.connect(self.onIRTClicked)
        Ui_MainWindow.pdf.clicked.connect(self.onPDFClicked)


        # Labels and progressbars
        InstructionLabel = QtWidgets.QLabel(UploadFrame)
        InstructionLabel.setGeometry(QtCore.QRect(90, 120, 300, 10))
        Ui_MainWindow.filename = QtWidgets.QLabel(UploadFrame)
        InputLabel = QtWidgets.QLabel(UploadFrame)
        uploadLabel = QtWidgets.QLabel(UploadFrame)
        UploadProgress = QtWidgets.QProgressBar()
        UploadProgress.setGeometry(200, 80, 250, 20)
        Ui_MainWindow.progress1 = QtWidgets.QProgressBar(AnalysisFrame)
        Ui_MainWindow.progress1.setGeometry(200, 80, 250, 20)
        analysisLabel = QtWidgets.QLabel(AnalysisFrame)
        Ui_MainWindow.progress2 = QtWidgets.QProgressBar()
        Ui_MainWindow.progress2.setGeometry(200, 80, 250, 20)
        
        #setText:
        Ui_MainWindow.Outliers.setText("Detect Outliers")
        Ui_MainWindow.IndMetrics.setText("Individual Metrics")
        Ui_MainWindow.Longitudinal.setText("Longitudinal Analysis")
        Ui_MainWindow.browse.setText("Browse...")
        Ui_MainWindow.filename.setText("   File...                  ")
        Ui_MainWindow.filename.setStyleSheet("background-color: white;")
        InstructionLabel.setText( "Choose between running QuaMeter and SwaMe directly or upload previous results:")
        InstructionLabel.setFont(Ui_MainWindow.boldfont)
        InputLabel.setText("File Input")
        InputLabel.setFont(Ui_MainWindow.boldfont)
        uploadLabel.setText("Upload a file (Either json, csv or tsv format):")
        uploadLabel.setFont(Ui_MainWindow.boldfont)
        analysisLabel.setText("Experiment Analysis")
        analysisLabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.DisableAnalysisButtons(self)
        
        vbox = QtWidgets.QVBoxLayout(self.browseFrame)
        hbox7 = QtWidgets.QHBoxLayout()
        hbox7.addWidget(uploadLabel)
        vbox.addLayout(hbox7)
        hbox8 = QtWidgets.QHBoxLayout()
        hbox8.addWidget(Ui_MainWindow.browse)
        hbox8.addWidget(Ui_MainWindow.filename)
        vbox.addLayout(hbox8)
        hbox9 = QtWidgets.QHBoxLayout()
        hbox9.addWidget(UploadProgress)
        vbox.addLayout(hbox9)
        Ui_MainWindow.browse.setFixedHeight(30)
        Ui_MainWindow.filename.setFixedHeight(30)
        
        
        #UploadFrame:
        uploadvbox = QtWidgets.QVBoxLayout(UploadFrame)
        actionComboBox = QtWidgets.QComboBox()
        actionComboBox.setStyleSheet('selection-background-color: rgb(240,240,240); selection-color:black; padding: 6px;')
        cbfont = QtGui.QFont()
        cbfont.setPointSize(12)
        actionComboBox.setFont(cbfont)
        actionComboBox.setMinimumHeight(50)
        listOfActions = ["Upload a file","DDA analysis with QuaMeter","DIA analysis with SwaMe"]
        for action in listOfActions:
            actionComboBox.addItem(action)
        actionComboBox.activated[str].connect(self.frame_change)
        
        self.stacked = QtWidgets.QStackedWidget()
        self.stacked.addWidget(self.browseFrame)
        self.stacked.addWidget(self.leftFrame)
        self.stacked.addWidget(self.rightFrame)
        
        
        Instructionshbox = QtWidgets.QHBoxLayout()
        Instructionshbox.addWidget(InstructionLabel)
        Instructionshbox.setAlignment(QtCore.Qt.AlignLeft)
    
        uploadvbox.addWidget(InputLabel)
        uploadvbox.addLayout(Instructionshbox)
        uploadvbox.addWidget(actionComboBox)
        uploadvbox.addWidget(self.stacked)
        
        
       


        #AnalysisFrame
        avbox = QtWidgets.QVBoxLayout(AnalysisFrame)
        hbox6 = QtWidgets.QHBoxLayout()
        hbox6.addWidget(analysisLabel)
        hbox6.setAlignment(QtCore.Qt.AlignLeft)
        avbox.addLayout(hbox6)
        hbox9 = QtWidgets.QHBoxLayout()
        hbox9.addWidget(Ui_MainWindow.Outliers)
        hbox9.addWidget(Ui_MainWindow.IndMetrics)
        hbox9.addWidget(Ui_MainWindow.Longitudinal)
        hbox9.setAlignment(QtCore.Qt.AlignLeft)
        Ui_MainWindow.Outliers.setFixedHeight(40)
        Ui_MainWindow.Outliers.setFixedWidth(130)
        Ui_MainWindow.Longitudinal.setFixedHeight(40)
        Ui_MainWindow.Longitudinal.setFixedWidth(130)
        Ui_MainWindow.IndMetrics.setFixedHeight(40)
        Ui_MainWindow.IndMetrics.setFixedWidth(130)
        avbox.addLayout(hbox9)
        hbox9.setAlignment(QtCore.Qt.AlignCenter)
        hbox10 = QtWidgets.QHBoxLayout()
        hbox10.addWidget(Ui_MainWindow.progress1)
        hbox10.addWidget(Ui_MainWindow.progress2)
        hbox10.setAlignment(QtCore.Qt.AlignLeft)
        avbox.addLayout(hbox10)
        hbox11 = QtWidgets.QHBoxLayout()
        avbox.addLayout(hbox11)
        hbox11.setAlignment(QtCore.Qt.AlignLeft)


        #MainLayout
        vbox = QtWidgets.QVBoxLayout(self.tab)
        hbox0 = QtWidgets.QHBoxLayout()
        hbox0.addWidget(UploadFrame)
        vbox.addLayout(hbox0)
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(AnalysisFrame)
        vbox.addLayout(hbox1)
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(OutputFrame)
        vbox.addLayout(hbox2)
        
        vbox.setAlignment(QtCore.Qt.AlignLeft)
        self.retranslateUi()
        Ui_MainWindow.browse.setEnabled(True)

        QtCore.QMetaObject.connectSlotsByName(self)

    def frame_change(self, text):
        if text == "DDA analysis with QuaMeter":
            self.stacked.setCurrentWidget(self.leftFrame)
        elif text == "DIA analysis with SwaMe":
            self.stacked.setCurrentWidget(self.rightFrame)
        elif text == "Upload a file":
            self.stacked.setCurrentWidget(self.browseFrame)
            
            

    def enable_slot(self):
        PCAGraph.PCAGraph.loadingsToggledOn(self)
        Ui_MainWindow.PCA.LoadingsProgressBar.setValue(100)

    def disable_slot(self):
        PCAGraph.PCAGraph.loadingsToggledOff(self)

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
        Ui_MainWindow.outliersDetected = True
        self.DisableAnalysisButtons()

        Ui_MainWindow.progress1.show()
        Ui_MainWindow.progress1.setValue(10)

       
        self.EnableAnalysisButtons()
        
        FileInput.BrowseWindow.currentDataset = Ui_MainWindow.NumericMetrics[0]
             # Check if you have the correct number of variables/samples
        if self.checkColumnNumberForPCA() == 1:

                if self.checkSampleNumberForPCA() == 1:
                    if len(FileInput.BrowseWindow.currentDataset.columns)>1:

                        #sampleToVariableRatio = PCA.PCA.calculateSampleToVariableRatio(self, FileInput.BrowseWindow.currentDataset)
        
       
                        PCA.PCA.CreatePCAGraph(FileInput.BrowseWindow.currentDataset)
                        Ui_MainWindow.progress1.setValue(51)
                        # Need to correctly calculate euc distance in N dimension
                        outliers = Ui_MainWindow.CalculateOutliers(self)
                        Ui_MainWindow.outlierlist = outliers["Filename"]

                        # --------------------------------------Widgets-------------------------------------------
                        Ui_MainWindow.PCA = QtWidgets.QTabWidget()
                        Ui_MainWindow.PCA.plotlabel = QtWidgets.QLabel(Ui_MainWindow.PCA)
                        #Ui_MainWindow.PCA.plotlabel.setGeometry(10, 500, 1000, 300)
                        Ui_MainWindow.PCA.PCAplot = PCAGraph.PCAGraph(now)
                        

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
                        Ui_MainWindow.PCA.LoadingsProgressBar.setGeometry(200, 80, 50, 20)

                        
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
                        
                        hbox2.setAlignment(QtCore.Qt.AlignCenter)
                        vbox2.addLayout(hbox2)
                        Ui_MainWindow.retranslateUi2(Ui_MainWindow.PCA)
                        Ui_MainWindow.EnableAnalysisButtons(self)
                        Ui_MainWindow.progress1.setValue(100)
                        PCAGraph.fig.canvas.mpl_connect("motion_notify_event",
                                                        Ui_MainWindow.onhover)
                        self.setCurrentIndex(oIndex)
                        Ui_MainWindow.pdf.setEnabled(True)

    def DisableBrowseButtons(self):
        Ui_MainWindow.browse.setEnabled(False)

    def EnableQuaMeterArguments(self):
        
        Ui_MainWindow.files.setEnabled(True)
        Ui_MainWindow.fileList.setEnabled(True)
        Ui_MainWindow.cpusLabel.setEnabled(True)
        Ui_MainWindow.cpusTextBox.setEnabled(True)
        Ui_MainWindow.CLOLabel.setEnabled(True)
        Ui_MainWindow.CLOTextBox.setEnabled(True)
        Ui_MainWindow.CUOLabel.setEnabled(True)
        Ui_MainWindow.CUOTextBox.setEnabled(True) 
        Ui_MainWindow.BrowseButton.setEnabled(True)
        Ui_MainWindow.RUNButton.setEnabled(True)
        #leftFrame.Dir.setEnabled(True)

    def DisableQuaMeterArguments(self):
        Ui_MainWindow.BrowseButton.setEnabled(False)
        Ui_MainWindow.files.setEnabled(False)
        Ui_MainWindow.fileList.setEnabled(False)
        Ui_MainWindow.cpusLabel.setEnabled(False)
        Ui_MainWindow.cpusTextBox.setEnabled(False)
        Ui_MainWindow.CLOLabel.setEnabled(False)
        Ui_MainWindow.CLOTextBox.setEnabled(False)
        Ui_MainWindow.CUOLabel.setEnabled(False)
        Ui_MainWindow.CUOTextBox.setEnabled(False) 
        Ui_MainWindow.BrowseButton.setEnabled(False)
        Ui_MainWindow.RUNButton.setEnabled(False)

    def EnableSwaMeArguments(self):
        
        Ui_MainWindow.SBrowseButton.setEnabled(True)
        Ui_MainWindow.Sfiles.setEnabled(True)
        Ui_MainWindow.SfileList.setEnabled(True)
        Ui_MainWindow.divisionLabel.setEnabled(True)
        Ui_MainWindow.divisionTextBox.setEnabled(True)
        Ui_MainWindow.MTLabel.setEnabled(True)
        Ui_MainWindow.MTTextBox.setEnabled(True)
        Ui_MainWindow.RTLabel.setEnabled(True)
        Ui_MainWindow.RTTextBox.setEnabled(True)
        Ui_MainWindow.SRUNButton.setEnabled(True)
        Ui_MainWindow.iRT.setEnabled(True)
        
    def DisableSwaMeArguments(self):
        Ui_MainWindow.SBrowseButton.setEnabled(False)
        Ui_MainWindow.Sfiles.setEnabled(False)
        Ui_MainWindow.SfileList.setEnabled(False)
        Ui_MainWindow.divisionLabel.setEnabled(False)
        Ui_MainWindow.divisionTextBox.setEnabled(False)
        Ui_MainWindow.MTLabel.setEnabled(False)
        Ui_MainWindow.MTTextBox.setEnabled(False)
        Ui_MainWindow.RTLabel.setEnabled(False)
        Ui_MainWindow.RTTextBox.setEnabled(False)
        Ui_MainWindow.SRUNButton.setEnabled(False)
        Ui_MainWindow.iRT.setEnabled(False)
        Ui_MainWindow.DisableSwaMeIRTArguments(self)

    def EnableSwaMeIRTArguments(self):
        Ui_MainWindow.iRTtoleranceLabel.setEnabled(True)
        Ui_MainWindow.iRTminintensityLabel.setEnabled(True)
        Ui_MainWindow.iRTminpeptidesLabel.setEnabled(True)
        Ui_MainWindow.iRTtoleranceTB.setEnabled(True)
        Ui_MainWindow.iRTminintensityTB.setEnabled(True)
        Ui_MainWindow.iRTminpeptidesTB.setEnabled(True)

    def DisableSwaMeIRTArguments(self):
        Ui_MainWindow.iRTtoleranceLabel.setEnabled(False)
        Ui_MainWindow.iRTminintensityLabel.setEnabled(False)
        Ui_MainWindow.iRTminpeptidesLabel.setEnabled(False)
        Ui_MainWindow.iRTtoleranceTB.setEnabled(False)
        Ui_MainWindow.iRTminintensityTB.setEnabled(False)
        Ui_MainWindow.iRTminpeptidesTB.setEnabled(False)

    def EnableAnalysisButtons(self):
        Ui_MainWindow.browse.setEnabled(True)
        Ui_MainWindow.Outliers.setEnabled(True)
        Ui_MainWindow.IndMetrics.setEnabled(True)
        Ui_MainWindow.Longitudinal.setEnabled(True)

    def DisableAnalysisButtons(self):
        Ui_MainWindow.browse.setEnabled(False)
        Ui_MainWindow.Outliers.setEnabled(False)
        Ui_MainWindow.IndMetrics.setEnabled(False)
        Ui_MainWindow.Longitudinal.setEnabled(False)
        Ui_MainWindow.pdf.setEnabled(False)

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
        Ui_MainWindow.indMetricsGraphed = True
        Ui_MainWindow.DisableAnalysisButtons(self)
        Ui_MainWindow.progress2.show()
        Ui_MainWindow.progress2.setValue(10)
        Ui_MainWindow.indMetrics = QtWidgets.QTabWidget()
        Ui_MainWindow.progress2.setValue(33)
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
        Ui_MainWindow.progress2.setValue(100)
        Ui_MainWindow.pdf.setEnabled(True)

    def createGraph(self, whichds):
        Ui_MainWindow.indMetrics.comboBox = QtWidgets.QComboBox(Ui_MainWindow.indMetrics)
        for metric in Ui_MainWindow.listOfMetrics:
            Ui_MainWindow.indMetrics.comboBox.addItem(metric)
        Ui_MainWindow.indMetrics.comboBox.activated[str].connect(self.metric_change)
        Ui_MainWindow.indMetrics.sampleBox = QtWidgets.QComboBox(Ui_MainWindow.indMetrics)
        for sample in Ui_MainWindow.metrics[0].index:
            Ui_MainWindow.indMetrics.sampleBox.addItem(sample)
        Ui_MainWindow.indMetrics.sampleBox.activated[str].connect(self.sample_change)
        Ui_MainWindow.progress2.setValue(80)
        vbox = QtWidgets.QVBoxLayout(Ui_MainWindow.indMetrics)
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
                            Ui_MainWindow.NumericMetrics[whichds], Ui_MainWindow.element, False)
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
        Ui_MainWindow.progress2.setValue(100)

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
        Ui_MainWindow.progress2.setValue(100)

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
                          "For this supervised approach you will need to provide training and test set data that contains both good and bad quality data. It is imperitive that you have high confidence in the training set and we recommend that you run PCA on the set to ascertain that there are no outliers. \n You will be asked to select a folder which contains corresponding pepxml Ui_MainWindow.files and QuaMeter/SwaMe output Ui_MainWindow.files for training set selection. Then you will be presented with a graph on which you should separate good from bad. Next you will do the same for the test set after which you will be presented with the model fit results.")
        
        FileInput.BrowseWindow.__init__(FileInput.BrowseWindow)
        TrainingSetfiles = FileInput.BrowseWindow.GetTrainingSetFiles(self)
        Ui_MainWindow.TrainingSetTable = pd.DataFrame(columns = ["Filename","Number of distinct peptides","Number of spectra identified"])
        
        if TrainingSetfiles:
            Ui_MainWindow.TrainingSetTable = pepXMLReader.pepXMLReader.parsePepXML(self, TrainingSetfiles)
            Ui_MainWindow.TrainingOrTestSet = QtWidgets.QTabWidget()
            Ui_MainWindow.TrainingOrTestSet.setStyleSheet("margin: 2px")
            Ui_MainWindow.sIndex = self.addTab(Ui_MainWindow.TrainingOrTestSet,"Setting up the training set:")
            
            Ui_MainWindow.CreateTrainingTab(self)
            self.setCurrentIndex(Ui_MainWindow.sIndex)
            Ui_MainWindow.RandomForestPerformed = True
            Ui_MainWindow.pdf.setEnabled(True)
        

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
            # if there are duplicates in the Ui_MainWindow.filenames column like RTsegments
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
        
        #Button:
        Ui_MainWindow.TrainingOrTestSet.badbtn = QtWidgets.QPushButton(
                'This is my selection for suboptimal quality.',
                Ui_MainWindow.TrainingOrTestSet)
        Ui_MainWindow.TrainingOrTestSet.badbtn.setEnabled(False)
        
        
        
        RFSelectionGrid = QtWidgets.QGridLayout(Ui_MainWindow.TrainingOrTestSet)
        RFSelectionGrid.addWidget(Ui_MainWindow.TrainingSetPlot,0,0,1,3)
        RFSelectionGrid.addWidget(Ui_MainWindow.TrainingOrTestSet.badbtn,2,1,2,1)
        
        
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
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.F1Label = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.F1Label.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.F1Label.setText("F1:")
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.F1Label.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.F1results = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.F1results.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.F1results.setText(str(round(performance.F1()[0][1],4)))
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.Accuracy = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.Accuracy.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.Accuracy.setText("RMSE:")
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.Accuracy.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AccuracyResults = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AccuracyResults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AccuracyResults.setText(str(round(performance.accuracy()[0][1],4)))        
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MCCLabel = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MCCLabel.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MCCLabel.setText("MCC:")
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MCCLabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MCCresults = QtWidgets.QLabel()
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MCCresults.setGeometry(QtCore.QRect(90, 120, 300, 10)) 
        Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MCCresults.setText(str(round(performance.mcc()[0][1],4)))        
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
        
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.F1Label,1,0,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.F1results,1,1,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.Accuracy,1,3,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AccuracyResults,1,4,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MCCLabel,1,6,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MCCresults,1,7,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.LLLabel,1,9,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.LLresults,1,10,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AUCLabel,1,12,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.AUCresults,1,13,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.GINILabel,1,15,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.GINIresults,1,16,1,1)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MPCELabel,2,0,2,2)
        pgrid.addWidget(Ui_MainWindow.TrainingOrTestSet.MetricsFrame.MPCEresults,2,2,2,1)
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
        currentrow = 0
        currentcolumn = 0
        for i in range(0,len(badlist)):
            label = QtWidgets.QLabel()
            label.setText(badlist[i])
            if len(badlist[i])>20:
                 badsamplesgrid.addWidget(label,currentrow,0)
                 currentrow = currentrow+1
                 currentcolumn = 0
            else:
                if currentcolumn>4:
                    currentrow = currentrow +1
                badsamplesgrid.addWidget(label,currentrow,currentcolumn)
                currentcolumn = currentcolumn+1
            
        Ui_MainWindow.badlist = badlist
                        
        #Layout within Frame:
        rvbox = QtWidgets.QVBoxLayout(Ui_MainWindow.TrainingOrTestSet.ResultsFrame)
        rhbox1 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingOrTestSet.ResultsFrame)
        rhbox1.addWidget(Ui_MainWindow.TrainingOrTestSet.ResultsFrame.MainLabel)
        rvbox.addLayout(rhbox1) 
        rhbox15 = QtWidgets.QHBoxLayout(Ui_MainWindow.TrainingOrTestSet.ResultsFrame)
        rhbox15.addWidget(Ui_MainWindow.TrainingOrTestSet.ResultsFrame.predictedLabel)
        rvbox.addLayout(rhbox15)       
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
        Ui_MainWindow.progress1.setValue(60)
        #self.metrics.index = self.metrics.iloc[:,0]
        medianDistances = Ui_MainWindow.createMedianDistances(self, sampleSize)
        outlierDistance = Ui_MainWindow.calculateOutLierDistances(self, medianDistances)
        Ui_MainWindow.progress1.setValue(65)

        for iterator in sampleSize:
            medianDistances["MedianDistance"][iterator] = np.percentile(PCA.Distances[iterator], 50)
        print(medianDistances)      
        Q1 = np.percentile(medianDistances["MedianDistance"], 25)
        Q3 =np.percentile(medianDistances["MedianDistance"], 75)
        IQR = Q3-Q1
        outlierDistance = Q3 + 1.5*IQR
        Ui_MainWindow.progress1.setValue(65)
       #Zscores:
        from scipy.stats import zscore
        medianDistances["zScore"] = zscore(medianDistances["MedianDistance"])
        medianDistances["outlier"]= medianDistances["zScore"].apply(
        lambda x: x <= -3.5 or x >= 3.5
        )
        print("The following runs were identified as candidates for possible outliers based on their z-scores:")
        Q3 = np.percentile(medianDistances["MedianDistance"], 75)  # Q3

        Ui_MainWindow.progress1.setValue(75)
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
        
    def onPDFClicked(self):
        PDFWriter.OutputWriter.producePDF(self,now)

    def retranslateUi2(self):
        _translate = QtCore.QCoreApplication.translate
        array = range(1, len(Ui_MainWindow.outlierlist), 1)
        Ui_MainWindow.outlierlistLabel.setText(
            "Suggested outlier candidates: ")
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

        
