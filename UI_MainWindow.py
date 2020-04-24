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
import PDFWriter
import tempfile
import datetime
import OutlierTab
import indMetricsTab
import maxQuantTxTReader
import mzIdentMLReader


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
        Ui_MainWindow.textedit =QtWidgets.QTextEdit(readOnly=True)
        

        #Widget stylesheets:
        Ui_MainWindow.BrowseButton.setStyleSheet("background-color: rgb(240,240,240);")

        #Widget texts:
        Ui_MainWindow.BrowseButton.setText("Browse ")
        Ui_MainWindow.files.setText("Folder:")
        Ui_MainWindow.cpusLabel.setText("Number of CPU's: ")
        Ui_MainWindow.CLOLabel.setText("m/z Lower Offset:")
        Ui_MainWindow.CUOLabel.setText("m/z Upper Offset:")
        Ui_MainWindow.RUNButton.setText("RUN")

        #Clicked.connect
        Ui_MainWindow.BrowseButton.clicked.connect(QuaMeter.QuaMeter.onQuaMeterBrowseClicked)
        Ui_MainWindow.RUNButton.clicked.connect(QuaMeter.QuaMeter.onQuaMeterRUNClicked)
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
        hbox4.addWidget(Ui_MainWindow.textedit)
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
        Ui_MainWindow.Stextedit =QtWidgets.QTextEdit(readOnly=True)
        Ui_MainWindow.IRTinputFile = None


        #Widget stylesheets:
        Ui_MainWindow.SBrowseButton.setStyleSheet("background-color: rgb(240,240,240);")
        Ui_MainWindow.SBrowseButton.setFixedHeight(30)
        Ui_MainWindow.SBrowseButton.setFixedHeight(30)

         #Clicked.connect
        Ui_MainWindow.SBrowseButton.clicked.connect(SwaMe.SwaMe.onSwaMeBrowseClicked)
        Ui_MainWindow.SRUNButton.clicked.connect(SwaMe.SwaMe.onSwaMeRUNClicked)

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
        SwaMehbox4.addWidget(Ui_MainWindow.iRTminintensityLabel)
        SwaMehbox4.addWidget(Ui_MainWindow.iRTminintensityTB)
        SwaMehbox4.addWidget(Ui_MainWindow.iRTminpeptidesLabel)
        SwaMehbox4.addWidget(Ui_MainWindow.iRTminpeptidesTB)
        SwaMevbox.addLayout(SwaMehbox4)
        SwaMehbox7 = QtWidgets.QHBoxLayout(Ui_MainWindow.rightFrame)
        SwaMehbox7.addWidget(Ui_MainWindow.SRUNButton)
        SwaMehbox7.addWidget(Ui_MainWindow.Stextedit)
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
        Ui_MainWindow.UploadProgress = QtWidgets.QProgressBar()
        Ui_MainWindow.UploadProgress.setGeometry(200, 80, 200, 20)
        Ui_MainWindow.progress1 = QtWidgets.QProgressBar(AnalysisFrame)
        analysisLabel = QtWidgets.QLabel(AnalysisFrame)
        
        #setText:
        Ui_MainWindow.Outliers.setText("Detect Outliers")
        Ui_MainWindow.IndMetrics.setText("Plot Individual Metrics")
        Ui_MainWindow.Longitudinal.setText("Analyze Longitudinal Data")
        Ui_MainWindow.browse.setText("Browse...")
        Ui_MainWindow.filename.setText("   File...                  ")
        Ui_MainWindow.filename.setStyleSheet("background-color: white;")
        InstructionLabel.setText( "Choose between uploading quality metrics or generating them by running QuaMeter ID-Free or SwaMe directly:")
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
        hbox9.addWidget(Ui_MainWindow.UploadProgress)
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
        Ui_MainWindow.Outliers.setFixedWidth(200)
        Ui_MainWindow.Longitudinal.setFixedHeight(40)
        Ui_MainWindow.Longitudinal.setFixedWidth(200)
        Ui_MainWindow.IndMetrics.setFixedHeight(40)
        Ui_MainWindow.IndMetrics.setFixedWidth(200)
        avbox.addLayout(hbox9)
        hbox9.setAlignment(QtCore.Qt.AlignCenter)
        hbox10 = QtWidgets.QHBoxLayout()
        hbox10.addWidget(Ui_MainWindow.progress1)
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
        OutlierTab.OutlierTab.LoadingsProgressBar.setValue(100)

    def disable_slot(self):
        PCAGraph.PCAGraph.loadingsToggledOff(self)

    
    @pyqtSlot()
    def onBrowseClicked(self):
        Ui_MainWindow.DisableAnalysisButtons(self)
        FileInput.BrowseWindow.__init__(Ui_MainWindow)
        inputFile = FileInput.BrowseWindow.GetInputFile(Ui_MainWindow)
        if inputFile:
            #filepath = FileInput.BrowseWindow.FileCheck(self, inputFile)
            Ui_MainWindow.metrics = FileInput.BrowseWindow.metricsParsing(self, inputFile)
            if "Filename " in Ui_MainWindow.metrics[0].columns:
                Ui_MainWindow.metrics[0] = Ui_MainWindow.metrics[0].rename(columns={"Filename ": 'Filename'})               
            if  "Filename" in Ui_MainWindow.metrics[0].columns:
                filenames = Ui_MainWindow.metrics[0]["Filename"]
                if ".mzml" in filenames[0].lower():
                       for item in range(0,len(filenames)):
                            if ".mzml" in filenames[item].lower():
                                filenames[item] = filenames[item].split('.')[0]
                            
                    
                Ui_MainWindow.metrics[0].index = filenames
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
                        outliers = PCA.PCA.CalculateOutliers(self)
                        Ui_MainWindow.outlierlist = outliers["Filename"]
                        OutlierTab.OutlierTab.createTabWidget(self,now)

                        

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
        Ui_MainWindow.progress1.setValue(10)
        Ui_MainWindow.indMetrics = QtWidgets.QTabWidget()
        Ui_MainWindow.progress1.setValue(33)
        
       
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
        indMetricsTab.IndMetricsTab.createTab(self, whichds)
        Ui_MainWindow.progress1.setValue(100)
        Ui_MainWindow.pdf.setEnabled(True)

    
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
        
        #Make a messagebox to ask how you wanna do this:
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("For this supervised approach you will need to set aside files that have not been included in the main dataset which will be randomly divided into test and training sets. You need to divide those files into examples of good and bad quality. How would you like to do so?")
        msgBox.addButton(QtWidgets.QPushButton('Select from graph of IDs'), QtWidgets.QMessageBox.YesRole)
        msgBox.addButton(QtWidgets.QPushButton('Select from table of quality metrics'), QtWidgets.QMessageBox.YesRole)
        msgBox.addButton(QtWidgets.QPushButton('Cancel'), QtWidgets.QMessageBox.RejectRole)
        ret = msgBox.exec_()

        if ret == 0: # They want the graph
            FileInput.BrowseWindow.__init__(FileInput.BrowseWindow)
            TrainingSetfiles = FileInput.BrowseWindow.GetTrainingSetFiles(self)
            Ui_MainWindow.TrainingSetTable = pd.DataFrame(columns = ["Filename","Number of distinct peptides","Number of spectra identified"])
            
            if TrainingSetfiles:
                if "pepxml" in TrainingSetfiles[0].lower():
                    Ui_MainWindow.TrainingSetTable = pepXMLReader.pepXMLReader.parsePepXML(self, TrainingSetfiles)
                elif ".txt" in TrainingSetfiles[0].lower():
                    Ui_MainWindow.TrainingSetTable =maxQuantTxTReader.maxQuantTxtReader.parseTxt(self, TrainingSetfiles[0])
                elif ".mzid" in TrainingSetfiles[0].lower():
                    Ui_MainWindow.TrainingSetTable =mzIdentMLReader.mzIdentMLReader.parsemzID(self, TrainingSetfiles)
                
                Ui_MainWindow.TrainingOrTestSet = QtWidgets.QTabWidget()
                Ui_MainWindow.TrainingOrTestSet.setStyleSheet("margin: 2px")
                Ui_MainWindow.sIndex = self.addTab(Ui_MainWindow.TrainingOrTestSet,"Setting up the training set:")
                Ui_MainWindow.CreateTrainingTab(self)
                self.setCurrentIndex(Ui_MainWindow.sIndex)
                Ui_MainWindow.RandomForestPerformed = True
                Ui_MainWindow.pdf.setEnabled(True)
        
        elif ret == 1:# They want the table
            FileInput.BrowseWindow.GetTrainingQualityFiles(self)
            Ui_MainWindow.TrainingOrTestSet = QtWidgets.QTabWidget()
            Ui_MainWindow.TrainingOrTestSet.setStyleSheet("margin: 2px")
            Ui_MainWindow.sIndex = self.addTab(Ui_MainWindow.TrainingOrTestSet,"Setting up the training set:")
            RandomForest.RandomForest.createTable(self)
            self.setCurrentIndex(Ui_MainWindow.sIndex)
            Ui_MainWindow.RandomForestPerformed = True
            Ui_MainWindow.pdf.setEnabled(True)
            
            
            
        

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
        
    
    def onPDFClicked(self):
        PDFWriter.OutputWriter.producePDF(self,now)


    
        
