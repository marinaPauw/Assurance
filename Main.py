import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
import statistics
import scipy
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import matplotlib.pyplot as plt
import re
#import MainParser
import QuaMeter
import IndividualMetrics
import PCA
import PCAGraph
from Datasets import Datasets
import RandomForest
import numpy as np
import pandas as pd
import SwaMe
import pepXMLReader
import RFSelectionPlots
import RandomForestResultsTab
import FeatureImportancePlot
import PDFWriter
import tempfile
import datetime
import OutlierTab
from indMetricsTab import IndMetricsTab
import maxQuantTxTReader
import mzIdentMLReader
import MainParser
import os
import Threads
import ctypes
import subprocess
import logging
import globalVars


class Main(QtWidgets.QTabWidget):
    def setupUi(self):
        super(Main, self).__init__()
        #sys.stdout = open("mylog.txt", "w")
        logging.basicConfig(level=logging.DEBUG, filename="mylog.txt", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
        sys.stderr = open("myerr.txt", "w")
        #Set the icon in the lefthand corner
        self.setWindowIcon(QtGui.QIcon('AssuranceIcon.png'))
        #Set the taskbar icon
        #myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
        #ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.threadpool = QtCore.QThreadPool()
        self.setWindowTitle("Assurance")
        self.resize(800,650)
        Main.Nulvalues = []
        Main.firstOutlierlist = []
        Main.secondOutlierlist = []
        Main.firstpossOutlierlist = []
        Main.secondpossOutlierlist = []
        Main.TrainingError = False
        Main.h2oError= False
        
        #Instantiate a datasets object:
        globalVars.var.database = Datasets()
        
        global now
        global tempDir
        globalVars.var.outliersDetected = False
        Main.indMetricsGraphed = False
        Main.RandomForestPerformed = False
        
        now = datetime.datetime.today()
        tempDir = tempfile.TemporaryDirectory()
        # fonts and style:
        Main.boldfont = QtGui.QFont()
        Main.boldfont.setBold(True)

        # Setting up the home tab:
        Main.tab = QtWidgets.QWidget()
        self.setCurrentIndex(0)
        self.tab.Main_layout = QtWidgets.QVBoxLayout()
        self.addTab(self.tab, "Home")
        self.tab.setStyleSheet("background-color: gainsboro;")

         #--------------------------------------------------------------Frames:-------------------------------------------------------
        UploadFrame = QtWidgets.QFrame(self)
        UploadFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        UploadFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        UploadFrame.setStyleSheet("background-color: rgb(245,245,245); margin:5px;")
         
         
        Main.leftFrame = QtWidgets.QFrame(UploadFrame)
        Main.leftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Main.leftFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Main.leftFrame.setStyleSheet("background-color: rgb(192,192,192); margin:5px;")
        

        Main.rightFrame = QtWidgets.QFrame(UploadFrame)
        Main.rightFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Main.rightFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Main.rightFrame.setStyleSheet("background-color: rgb(192,192,192); margin:5px;")

        Main.browseFrame = QtWidgets.QFrame(UploadFrame)
        Main.browseFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Main.browseFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        Main.browseFrame.setStyleSheet("background-color: rgb(192,192,192); margin:5px;")
        
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
        Main.BrowseButton = QtWidgets.QPushButton(self.leftFrame)
        Main.files = QtWidgets.QLabel(self.leftFrame)
        Main.fileList= QtWidgets.QLabel(self.leftFrame)
        #Main.cpusLabel= QtWidgets.QLabel(self.leftFrame)
        #Main.cpusTextBox = QtWidgets.QLineEdit(self.leftFrame)
        Main.CLOLabel= QtWidgets.QLabel(self.leftFrame)
        Main.CLOTextBox = QtWidgets.QLineEdit(self.leftFrame)
        Main.CUOLabel= QtWidgets.QLabel(self.leftFrame)
        Main.CUOTextBox = QtWidgets.QLineEdit(self.leftFrame) 
        Main.RUNButton = QtWidgets.QPushButton(self.leftFrame)
        Main.textedit =QtWidgets.QTextEdit(readOnly=True)
        

        #Widget stylesheets:
        Main.BrowseButton.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
        Main.RUNButton.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
       # Main.cpusTextBox.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
        Main.CLOTextBox.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
        Main.CUOTextBox.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
        Main.fileList.setStyleSheet("padding: 3px;")
        Main.textedit.setStyleSheet("background-color: rgb(240,240,240);padding: 1px;")

        #Widget texts:
        Main.BrowseButton.setText("Browse ")
        Main.files.setText("Folder:")
        #Main.cpusLabel.setText("Number of CPU's: ")
        Main.CLOLabel.setText("m/z Lower Offset:")
        Main.CUOLabel.setText("m/z Upper Offset:")
        Main.RUNButton.setText("Run")

        #Clicked.connect
        Main.BrowseButton.clicked.connect(QuaMeter.QuaMeter.onQuaMeterBrowseClicked)
        Main.RUNButton.clicked.connect(QuaMeter.QuaMeter.onQuaMeterRUNClicked)
        #QuaMeterGrid:
        #Layout:
        
        QuaMetervbox = QtWidgets.QVBoxLayout(Main.leftFrame)
        hbox1 = QtWidgets.QHBoxLayout(Main.leftFrame)
        Qvbox2 = QtWidgets.QVBoxLayout(Main.leftFrame)
        QhboxFiles = QtWidgets.QHBoxLayout(Main.leftFrame)
        QhboxFiles.addWidget( Main.BrowseButton)
        QhboxFiles.addWidget(Main.files)     
        QhboxFiles.addWidget(Main.fileList)
        Qvbox2.addLayout(QhboxFiles)
        hbox1.addLayout(Qvbox2)
        hbox1.addStretch()
        QuaMetervbox.addLayout(hbox1)
        #Multiple cpus not included at this moment
        #hbox2 = QtWidgets.QHBoxLayout(Main.leftFrame)
        #hbox2.addWidget(Main.cpusLabel)
        #hbox2.addWidget(Main.cpusTextBox)
        #QuaMetervbox.addLayout(hbox2)
        hbox3 = QtWidgets.QHBoxLayout()
        hbox3.addWidget(Main.CLOLabel)
        hbox3.addWidget(Main.CLOTextBox)
        hbox3.addWidget(Main.CUOLabel)
        hbox3.addWidget(Main.CUOTextBox)
        QuaMetervbox.addLayout(hbox3)
        hbox4 = QtWidgets.QHBoxLayout()
        hbox4.addWidget(Main.RUNButton)
        hbox4.addWidget(Main.textedit)
        QuaMetervbox.addLayout(hbox4)
        
        #-------------------------------------------------SwaMeLayout--------------------------------------------------------

        #Widget declaring:
        Main.SBrowseButton = QtWidgets.QPushButton(Main.rightFrame)
        Main.Sfiles = QtWidgets.QLabel(Main.rightFrame)
        Main.SfileList = QtWidgets.QLabel(Main.rightFrame)
        Main.divisionLabel= QtWidgets.QLabel(Main.rightFrame)
        Main.divisionTextBox= QtWidgets.QLineEdit(Main.rightFrame)
        Main.MTLabel= QtWidgets.QLabel(Main.rightFrame)
        Main.MTTextBox = QtWidgets.QLineEdit(Main.rightFrame)
        Main.RTLabel= QtWidgets.QLabel(Main.rightFrame)
        Main.RTTextBox = QtWidgets.QLineEdit(Main.rightFrame)
        Main.SRUNButton = QtWidgets.QPushButton(Main.rightFrame)
        Main.iRT =  QtWidgets.QPushButton(Main.rightFrame)
        Main.iRTFilelist = QtWidgets.QLabel(Main.rightFrame)
        Main.iRTtoleranceLabel =QtWidgets.QLabel(Main.rightFrame)
        Main.iRTminintensityLabel =QtWidgets.QLabel(Main.rightFrame)
        Main.iRTminpeptidesLabel =QtWidgets.QLabel(Main.rightFrame)
        Main.iRTtoleranceTB =QtWidgets.QLineEdit(Main.rightFrame)
        Main.iRTminintensityTB =QtWidgets.QLineEdit(Main.rightFrame)
        Main.iRTminpeptidesTB =QtWidgets.QLineEdit(Main.rightFrame)
        Main.minintensityLabel =QtWidgets.QLabel(Main.rightFrame)
        Main.minintensityTB =QtWidgets.QLineEdit(Main.rightFrame)
        Main.Stextedit =QtWidgets.QTextEdit(readOnly=True)
        Main.IRTinputFile = None


        #Widget stylesheets:
        Main.SBrowseButton.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Main.SRUNButton.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Main.SfileList.setStyleSheet(" padding: 3px;")
        Main.divisionTextBox.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Main.MTTextBox.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Main.RTTextBox.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Main.Stextedit.setStyleSheet("background-color: rgb(240,240,240); padding: 1px;")
        Main.iRT.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Main.iRTtoleranceTB.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Main.iRTminintensityTB.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Main.iRTminpeptidesTB.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Main.minintensityTB.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Main.SBrowseButton.setFixedHeight(30)
        Main.SBrowseButton.setFixedHeight(30)

        #For error logging:
        Main.errors = []
        
        #Clicked.connect
        Main.SBrowseButton.clicked.connect(SwaMe.SwaMe.onSwaMeBrowseClicked)
        Main.SRUNButton.clicked.connect(SwaMe.SwaMe.onSwaMeRUNClicked)

        #Widget texts:
        Main.SBrowseButton.setText("Browse:")
        Main.Sfiles.setText("Folder: ")
        Main.divisionLabel.setText("Number of RT segments: ")
        Main.MTLabel.setText("MassTolerance (m/z):")
        Main.RTLabel.setText("RTTolerance (min):")
        Main.SRUNButton.setText("Run")
        Main.iRTtoleranceLabel.setText("iRTtolerance (min):")
        Main.iRTminintensityLabel.setText("Minimum IRTIntensity:")
        Main.minintensityLabel.setText("Minimum Intensity:")
        Main.iRTminpeptidesLabel.setText("Minimum number of fragments per iRTpeptide:")
        Main.iRT.setText("iRT")
        Main.iRTFilelist.setText("File...")
        
        #Layout:
        SwaMevbox = QtWidgets.QVBoxLayout(Main.rightFrame)
        SwaMehbox1 = QtWidgets.QHBoxLayout(Main.rightFrame)
        SwaMevbox2 = QtWidgets.QVBoxLayout(Main.rightFrame)
        SwaMehboxf = QtWidgets.QHBoxLayout(Main.rightFrame)
        SwaMehboxf.addWidget(Main.SBrowseButton)
        SwaMehboxf.addWidget(Main.Sfiles)     
        SwaMehboxf.addWidget(Main.SfileList)
        SwaMevbox2.addLayout(SwaMehboxf)
        SwaMehbox1.addLayout(SwaMevbox2)
        SwaMehbox1.addStretch()
        SwaMevbox.addLayout(SwaMehbox1)
        SwaMehbox3 = QtWidgets.QHBoxLayout(Main.rightFrame)
        SwaMehbox3.addWidget(Main.divisionLabel)
        SwaMehbox3.addWidget(Main.divisionTextBox)
        SwaMehbox3.addWidget(Main.MTLabel)
        SwaMehbox3.addWidget(Main.MTTextBox)
        SwaMehbox3.addWidget(Main.RTLabel)
        SwaMehbox3.addWidget(Main.RTTextBox)
        SwaMehbox3.addWidget(Main.minintensityLabel)
        SwaMehbox3.addWidget(Main.minintensityTB)
        SwaMevbox.addLayout(SwaMehbox3)
        SwaMehbox2 = QtWidgets.QHBoxLayout(Main.rightFrame)
        SwaMehbox2.addWidget(Main.iRT)
        SwaMehbox2.addWidget(Main.iRTFilelist)
        SwaMevbox.addLayout(SwaMehbox2)
        SwaMehbox4 = QtWidgets.QHBoxLayout(Main.rightFrame)
        SwaMehbox4.addWidget(Main.iRTtoleranceLabel)
        SwaMehbox4.addWidget(Main.iRTtoleranceTB)
        SwaMehbox4.addWidget(Main.iRTminintensityLabel)
        SwaMehbox4.addWidget(Main.iRTminintensityTB)
        SwaMehbox4.addWidget(Main.iRTminpeptidesLabel)
        SwaMehbox4.addWidget(Main.iRTminpeptidesTB)
        SwaMevbox.addLayout(SwaMehbox4)
        SwaMehbox7 = QtWidgets.QHBoxLayout(Main.rightFrame)
        SwaMehbox7.addWidget(Main.SRUNButton)
        SwaMehbox7.addWidget(Main.Stextedit)
        SwaMevbox.addLayout(SwaMehbox7)
        #------------------------------------------------OutputFrame--------------------------------------------------------
        Main.pdf = QtWidgets.QPushButton(OutputFrame)
        Main.pdf.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
        Main.pdf.setText("Export to PDF")
        Main.pdf.progress = QtWidgets.QProgressBar()
        Main.pdf.progress.setGeometry(200, 80, 250, 20)
        
        outputHBOX = QtWidgets.QHBoxLayout(OutputFrame)
        outputHBOX.addStretch()
        outputHBOX.addWidget(Main.pdf)
        outputHBOX.addWidget(Main.pdf.progress)
        outputHBOX.addStretch()
        

        #-------------------------------------------------MainLayout--------------------------------------------------------
          #All the buttons MainWindow:
        Main.browse = QtWidgets.QPushButton(self.tab)
        Main.browse.setStyleSheet("background-color: rgb(240,240,240);")
        globalVars.var.outliers = QtWidgets.QPushButton(self.tab)
        globalVars.var.outliers.setStyleSheet("background-color: rgb(240,240,240);")
        Main.IndMetrics = QtWidgets.QPushButton(self.tab)
        Main.IndMetrics.setStyleSheet("background-color: rgb(240,240,240);")
        Main.Longitudinal = QtWidgets.QPushButton(self.tab)
        Main.Longitudinal.setStyleSheet("background-color: rgb(240,240,240);")
        
        

        #clicked.connect
        Main.browse.clicked.connect(lambda: self.onBrowseClicked())
        globalVars.var.outliers.clicked.connect(self.onOutliersClicked)
        Main.IndMetrics.clicked.connect(self.onIndMetricsClicked)
        Main.Longitudinal.clicked.connect(self.onLongitudinalClicked)
        Main.iRT.clicked.connect(self.onIRTClicked)
        Main.pdf.clicked.connect(self.onPDFClicked)


        # Labels and progressbars
        InstructionLabel = QtWidgets.QLabel(UploadFrame)
        InstructionLabel.setGeometry(QtCore.QRect(90, 120, 300, 10))
        Main.filenameDisplay = QtWidgets.QLabel(UploadFrame)
        InputLabel = QtWidgets.QLabel(UploadFrame)
        uploadLabel = QtWidgets.QLabel(UploadFrame)
        Main.UploadProgress = QtWidgets.QProgressBar()
        Main.UploadProgress.setGeometry(200, 80, 200, 20)
        Main.progress1 = QtWidgets.QProgressBar(AnalysisFrame)
        analysisLabel = QtWidgets.QLabel(AnalysisFrame)
        
        #setText:
        globalVars.var.outliers.setText("Detect Outliers")
        Main.IndMetrics.setText("Plot Individual Metrics")
        Main.Longitudinal.setText("Analyze Longitudinal Data")
        Main.browse.setText("Browse...")
        Main.filenameDisplay.setText("   File...                  ")
        Main.filenameDisplay.setStyleSheet("background-color: white;")
        InstructionLabel.setText( "Choose between uploading quality metrics or generating them by running QuaMeter ID-Free or SwaMe directly:")
        InstructionLabel.setFont(Main.boldfont)
        InputLabel.setText("File Input")
        InputLabel.setFont(Main.boldfont)
        uploadLabel.setText("Upload a file (Either json, csv or tsv format):")
        uploadLabel.setFont(Main.boldfont)
        analysisLabel.setText("Experiment Analysis")
        analysisLabel.setFont(Main.boldfont)
        Main.DisableAnalysisButtons(self)
        
        vbox = QtWidgets.QVBoxLayout(self.browseFrame)
        hbox7 = QtWidgets.QHBoxLayout()
        hbox7.addWidget(uploadLabel)
        vbox.addLayout(hbox7)
        hbox8 = QtWidgets.QHBoxLayout()
        hbox8.addWidget(Main.browse)
        hbox8.addWidget(Main.filenameDisplay)
        vbox.addLayout(hbox8)
        hbox9 = QtWidgets.QHBoxLayout()
        hbox9.addWidget(Main.UploadProgress)
        vbox.addLayout(hbox9)
        Main.browse.setFixedHeight(30)
        Main.filenameDisplay.setFixedHeight(30)
        
        
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
        hbox9.addWidget(globalVars.var.outliers)
        hbox9.addWidget(Main.IndMetrics)
        hbox9.addWidget(Main.Longitudinal)
        hbox9.setAlignment(QtCore.Qt.AlignLeft)
        globalVars.var.outliers.setFixedHeight(40)
        globalVars.var.outliers.setFixedWidth(200)
        Main.Longitudinal.setFixedHeight(40)
        Main.Longitudinal.setFixedWidth(200)
        Main.IndMetrics.setFixedHeight(40)
        Main.IndMetrics.setFixedWidth(200)
        avbox.addLayout(hbox9)
        hbox9.setAlignment(QtCore.Qt.AlignCenter)
        hbox10 = QtWidgets.QHBoxLayout()
        hbox10.addWidget(Main.progress1)
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
        self.DisableAnalysisButtons()
        Main.browse.setEnabled(True)

        QtCore.QMetaObject.connectSlotsByName(self)

    def frame_change(self, text):
        if text == "DDA analysis with QuaMeter":
            self.stacked.setCurrentWidget(self.leftFrame)
        elif text == "DIA analysis with SwaMe":
            self.stacked.setCurrentWidget(self.rightFrame)
        elif text == "Upload a file":
            self.stacked.setCurrentWidget(self.browseFrame)
            
    def progress_fn(self,n):
        Main.UploadProgress.setValue(n)

    def enable_slot(self):
        PCAGraph.PCAGraph.loadingsToggledOn(self)
        OutlierTab.OutlierTab.LoadingsProgressBar.setValue(100)

    def disable_slot(self):
        PCAGraph.PCAGraph.loadingsToggledOff(self)

    @QtCore.pyqtSlot()    
    def onBrowseClicked(self):
        self.parser = MainParser.Parser()
        self.parser.GetInputFile()
        #Threading
        tbrowse = Threads.SideThread(lambda: self.ParseFiles())
        tbrowse.signals.result.connect(self.ThreadingFix)
        globalVars.var.threadpool.start(tbrowse)        
        
    def ParseFiles(self):                
            try:
                self.parser.parseInputFiles()
            except Exception as ex:
                logging.info(ex)
                QtWidgets.QMessageBox.warning(self, "Error","Failed to parse file, please doublecheck file column integrity.")
            QtCore.QMetaObject.invokeMethod(self.UploadProgress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 20))
        
            try:
                self.assuranceDirectory = os.getcwd()
                os.chdir(os.path.dirname(os.path.abspath(self.parser.possibleInputFiles[0])))
            except:
                logging.info("Changing the directory didn't work.")
            logging.info(type(self.database.metrics))
            QtCore.QMetaObject.invokeMethod(self.UploadProgress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 28))
            try: 
                if type(globalVars.var.database.metrics) != bool:
                        QtCore.QMetaObject.invokeMethod(Main.UploadProgress, "setValue",
                                            QtCore.Qt.QueuedConnection,
                                            QtCore.Q_ARG(int, 30))
                        logging.info(globalVars.var.database.metrics[0].columns)
                        if "Filename " in globalVars.var.database.metrics[0].columns:
                            globalVars.var.database.metrics[0] = globalVars.var.database.metrics[0].rename(columns={"Filename ": 'Filename'})               
                        if  "Filename" in globalVars.var.database.metrics[0].columns:

                            globalVars.var.database.metrics[0]['Filename'].replace( { r"[\.mzML]+" : '' }, inplace= True, regex = True)
                            globalVars.var.database.metrics[0].index = globalVars.var.database.metrics[0]['Filename']
                            QtCore.QMetaObject.invokeMethod(Main.UploadProgress, "setValue",
                                            QtCore.Qt.QueuedConnection,
                                            QtCore.Q_ARG(int, 80))                    
                        
                        QtCore.QMetaObject.invokeMethod(Main.UploadProgress, "setValue",
                                            QtCore.Qt.QueuedConnection,
                                            QtCore.Q_ARG(int, 90))
                        attrs = vars(globalVars.var.database)
                        logging.info(', '.join("%s: %s" % item for item in attrs.items()))
                        globalVars.var.database.ExtractNumericColumns(False)
                        globalVars.var.database.RemoveLowVarianceColumns(False)                      
                        
                        QtCore.QMetaObject.invokeMethod(Main.UploadProgress, "setValue",
                                            QtCore.Qt.QueuedConnection,
                                            QtCore.Q_ARG(int, 100))
            except Exception as ex:
                logging.info(ex)
                QtWidgets.QMessageBox.warning(self, "Error","Something went wrong while parsing the file.")
                    
    def ThreadingFix(self):
        if len(Main.Nulvalues) >0:
            QtWidgets.QMessageBox.warning(self, "Warning","There were metrics that did not have values in them:" + str(Main.Nulvalues))
        Main.EnableAnalysisButtons(self)
        
        if len(globalVars.var.database.metrics)>0:
            Main.EnableAnalysisButtons(self)
        else:
            Main.Message(self,"An error occurred. Please check that the input files are either mzQC, tsv or csv quality files. Multiple files of the same type are allowed.")
            Main.UploadProgress.setValue(0)
            self.onBrowseClicked()

    @QtCore.pyqtSlot()
    def onOutliersClicked(self):
        self.DisableAnalysisButtons()

        Main.progress1.show()
        Main.progress1.setValue(10)

       
        self.EnableAnalysisButtons()
        if not hasattr(globalVars.var.database,"currentDataset"):
            globalVars.var.database.currentDataset = globalVars.var.database.numericMetrics[0]
             # Check if you have the correct number of variables/samples
        if self.checkColumnNumberForPCA() == 1:

                if self.checkSampleNumberForPCA() == 1:
                    if len(globalVars.var.database.currentDataset.columns)>1:

                        #sampleToVariableRatio = PCA.PCA.calculateSampleToVariableRatio(self, Main.globalVars.var.database.currentDataset)
                        PCA.PCA.CreatePCAGraph(globalVars.var.database.currentDataset)
                        Main.progress1.setValue(51)
                        # Need to correctly calculate euc distance in N dimension
                        outliers = PCA.PCA.CalculateOutliers(self)
                        globalVars.var.outlierlist = outliers["Filename"]
                        if len(Main.firstOutlierlist)<1:#Either there were no outliers and the reanalysis is pointless, or this is the first.
                            Main.firstOutlierlist = outliers["Filename"]
                        elif len(Main.secondOutlierlist)<1:#Either there were no outliers and the reanalysis is pointless, or this is the second.
                            Main.secondOutlierlist = outliers["Filename"]
                        if len(Main.firstpossOutlierlist)<1:#Either there were no outliers and the reanalysis is pointless, or this is the first.
                            Main.firstpossOutlierlist = PCA.PCA.possOutlierList
                        elif len(Main.secondpossOutlierlist)<1:#Either there were no outliers and the reanalysis is pointless, or this is the second.
                            Main.secondpossOutlierlist = PCA.PCA.possOutlierList
                        OutlierTab.OutlierTab.createTabWidget(self,now)
                        globalVars.var.outliersDetected = True

    def setProgressVal(self, val):
        OutlierTab.OutlierTab.LoadingsProgressBar.setValue(val)                        

    def EnableBrowseButtons(self):
        Main.browse.setEnabled(True)

    def DisableBrowseButtons(self):
        Main.browse.setEnabled(False)

    def EnableQuaMeterArguments(self):
        
        Main.files.setEnabled(True)
        Main.fileList.setEnabled(True)
        #Main.cpusLabel.setEnabled(True)
        #Main.cpusTextBox.setEnabled(True)
        Main.CLOLabel.setEnabled(True)
        Main.CLOTextBox.setEnabled(True)
        Main.CUOLabel.setEnabled(True)
        Main.CUOTextBox.setEnabled(True) 
        Main.BrowseButton.setEnabled(True)
        Main.RUNButton.setEnabled(True)
        #leftFrame.Dir.setEnabled(True)

    def DisableQuaMeterArguments(self):
        Main.BrowseButton.setEnabled(False)
        Main.files.setEnabled(False)
        #Main.cpusLabel.setEnabled(False)
        #Main.cpusTextBox.setEnabled(False)
        Main.CLOLabel.setEnabled(False)
        Main.CLOTextBox.setEnabled(False)
        Main.CUOLabel.setEnabled(False)
        Main.CUOTextBox.setEnabled(False) 
        Main.BrowseButton.setEnabled(False)
        Main.RUNButton.setEnabled(False)

    def EnableSwaMeArguments(self):
        
        Main.SBrowseButton.setEnabled(True)
        Main.Sfiles.setEnabled(True)
        Main.SfileList.setEnabled(True)
        Main.divisionLabel.setEnabled(True)
        Main.divisionTextBox.setEnabled(True)
        Main.MTLabel.setEnabled(True)
        Main.MTTextBox.setEnabled(True)
        Main.RTLabel.setEnabled(True)
        Main.RTTextBox.setEnabled(True)
        Main.minintensityLabel.setEnabled(True)
        Main.SRUNButton.setEnabled(True)
        Main.iRT.setEnabled(True)
        
    def DisableSwaMeArguments(self):
        Main.SBrowseButton.setEnabled(False)
        Main.Sfiles.setEnabled(False)
        Main.SfileList.setEnabled(False)
        Main.divisionLabel.setEnabled(False)
        Main.divisionTextBox.setEnabled(False)
        Main.MTLabel.setEnabled(False)
        Main.MTTextBox.setEnabled(False)
        Main.RTLabel.setEnabled(False)
        Main.RTTextBox.setEnabled(False)
        Main.SRUNButton.setEnabled(False)
        Main.iRT.setEnabled(False)
        Main.minintensityLabel.setEnabled(False)
        Main.DisableSwaMeIRTArguments(self)

    def EnableSwaMeIRTArguments(self):
        Main.iRTtoleranceLabel.setEnabled(True)
        Main.iRTminintensityLabel.setEnabled(True)
        Main.iRTminpeptidesLabel.setEnabled(True)
        Main.iRTtoleranceTB.setEnabled(True)
        Main.iRTminintensityTB.setEnabled(True)
        Main.iRTminpeptidesTB.setEnabled(True)
        Main.minintensityTB.setEnabled(True)
        Main.iRTFilelist.setEnabled(True)
        

    def DisableSwaMeIRTArguments(self):
        Main.iRTtoleranceLabel.setEnabled(False)
        Main.iRTminintensityLabel.setEnabled(False)
        Main.iRTminpeptidesLabel.setEnabled(False)
        Main.iRTtoleranceTB.setEnabled(False)
        Main.iRTminintensityTB.setEnabled(False)
        Main.iRTminpeptidesTB.setEnabled(False)
        Main.minintensityTB.setEnabled(False)
        Main.iRTFilelist.setEnabled(False)

    def EnableAnalysisButtons(self):
        Main.browse.setEnabled(True)
        globalVars.var.outliers.setEnabled(True)
        Main.IndMetrics.setEnabled(True)
        Main.Longitudinal.setEnabled(True)

    def DisableAnalysisButtons(self):
        Main.browse.setEnabled(False)
        globalVars.var.outliers.setEnabled(False)
        Main.IndMetrics.setEnabled(False)
        Main.Longitudinal.setEnabled(False)
        Main.pdf.setEnabled(False)

    @pyqtSlot()
    def enable_reanalysis(self):
        PCAGraph.PCAGraph.printForReport(self, now)# Print it now before reanalysis
        globalVars.var.database.currentDataset = globalVars.var.database.currentDataset.drop(globalVars.var.outlierlist)
        Main.onOutliersClicked(self)

    @pyqtSlot()
    def onIRTClicked(self):
         Main.EnableSwaMeIRTArguments(self)
         Main.IRTinputFile = self.parser.GetIRTInputFile()
         Main.iRTFilelist.setText(Main.IRTinputFile)

    @pyqtSlot()
    def onIndMetricsClicked(self):
        Main.DisableAnalysisButtons(self)
        Main.progress1.setValue(10)
        Main.indMetrics = QtWidgets.QTabWidget()
        
       
        Main.listOfMetrics = list()
        if "StartTimeStamp" in globalVars.var.database.metrics[0].columns:
            Main.listOfMetrics.append("StartTimeStamp")
        for dataset in range(len(globalVars.var.database.numericMetrics)): # For each dataset in all the globalVars.var.database we have
            for element in globalVars.var.database.numericMetrics[dataset].columns:
                    Main.listOfMetrics.append(element)
                    
        Main.element = Main.listOfMetrics[0]
        #-------------- widgets ---------------------------------------
        
        Main.progress1.setValue(33)
        whichds = 0
        for dataset in range(len(globalVars.var.database.numericMetrics)):
                if Main.element in globalVars.var.database.numericMetrics[dataset].columns:
                    whichds = dataset
                    break
        Main.sampleSelected = globalVars.var.database.numericMetrics[0].index[0]
        Main.itab = QtWidgets.QTabWidget()
        Main.iIndex = self.addTab(Main.itab,
                                 "Individual metrics")
        Main.indMetricsTab = IndMetricsTab()
        Main.indMetricsTab.createGraph(whichds)        
        self.setCurrentIndex(Main.iIndex)
        Main.EnableAnalysisButtons(self)
        Main.progress1.setValue(100)
        Main.pdf.setEnabled(True)
        Main.indMetricsGraphed = True

    def SwitchIndMetricsTab(self, whichds, text):
        globalVars.var.itab = QtWidgets.QTabWidget()
        self.iIndex =self.addTab(globalVars.var.itab,
                                 "Individual metrics")        
        
        self.indMetricsTab.createGraph(whichds)      
        tableIndex = list(globalVars.var.database.metrics[0].index)
        #self.indMetricsTab.sampleBox.setCurrentIndex(tableIndex.index(Main.sampleSelected)+1)                 
        self.indMetricsTab.comboBox.setCurrentIndex( Main.listOfMetrics.index(text))       
        self.setCurrentIndex(self.iIndex)
        Main.progress1.setValue(100)

    
    def checkColumnNumberForPCA(self):
        if(len(globalVars.var.database.numericMetrics[0].columns) < 3):
            self.Message("There are less than three \
                              numeric columns in the dataset. PCA will not \
                              be performed.")
            self.progress1.setValue(0)
            self.EnableAnalysisButtons()
            return 0
        else: 
            return 1

    def checkSampleNumberForPCA(self):
        if(len(globalVars.var.database.currentDataset.index) < 4):
            self.Message("There are less than three samples in the dataset. PCA will not be performed.")
            self.progress1.setValue(0)
            self.EnableAnalysisButtons()
            return 0
        else:
            return 1


    def enable_legend(metric):
        IndividualMetrics.MyIndMetricsCanvas.ShowLegend(metric)

    def disable_legend(metric):
        IndividualMetrics.MyIndMetricsCanvas.HideLegend(metric)

    @QtCore.pyqtSlot()
    def onLongitudinalClicked(self):
        Main.DisableAnalysisButtons(self)
        Main.predictionArea = [0, 0, 0, 0]
        # Bools to keep track:
        Main.goodPredicted = False
        Main.badPredicted = False
        Main.goodpredictionList = []
        Main.badpredictionList = []
        
        #Make a messagebox to ask how you wanna do this:
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle("Assurance - Longitudinal analysis")
        msgBox.setText("For this supervised approach you will need to set aside files that have not been included in the Main dataset which will be randomly divided into test and training sets. You need to divide those files into examples of good and bad quality. How would you like to do so?")
        msgBox.addButton(QtWidgets.QPushButton('Select from graph of IDs'), QtWidgets.QMessageBox.YesRole)
        msgBox.addButton(QtWidgets.QPushButton('Select from table of quality metrics'), QtWidgets.QMessageBox.YesRole)
        msgBox.addButton(QtWidgets.QPushButton('Cancel'), QtWidgets.QMessageBox.RejectRole)
        ret = msgBox.exec_()

        if ret == 0: # They want the graph
            
            tpep = Threads.SideThread(self.GetTrainingSetTable)
            tpep.signals.result.connect(self.OnParserThreadFinish)
            self.threadpool.start(tpep)
            
            
        
        elif ret == 1:# They want the table
            self.parser.GetTrainingQualityFiles()
            if self.parser.NullError:
                QtWidgets.QMessageBox.warning(self,"Error","Is it possible there may be unnecessary spaces in your tsv? Two spaces next to each other will create a NaN column.Fix the file and upload it again.")
                self.parser.GetTrainingQualityFiles(Main)
            if hasattr(globalVars.var,"Numerictrainingmetrics"):
                if len(globalVars.var.Numerictrainingmetrics)>0:
                    Main.TrainingOrTestSet = QtWidgets.QTabWidget()
                    Main.TrainingOrTestSet.setStyleSheet("margin: 2px;")
                    Main.sIndex = self.addTab(Main.TrainingOrTestSet,"Setting up the training set:")
                    RandomForest.RandomForest.createTable(self)
                    self.setCurrentIndex(Main.sIndex)
                    Main.RandomForestPerformed = True
                    Main.pdf.setEnabled(True)
                else:
                    QtWidgets.QMessageBox.warning(self,"Error","Something went wrong.")
            else:
                Main.EnableAnalysisButtons(self) 
            
        elif ret == 2:#Cancelled
            Main.EnableAnalysisButtons(self)
            
            
    def GetTrainingSetTable(self):
            self.parser.GetTrainingSetFiles(self)
            QtCore.QMetaObject.invokeMethod(Main.progress1, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 20))
            Main.TrainingSetTable = pd.DataFrame(columns = ["Filename","Number of distinct peptides","Number of spectra identified"])
            
            if len(self.parser.trainingsetFiles)>0:
                if "pepxml" in self.parser.trainingsetFiles[0].lower():
                    Main.TrainingSetTable = pepXMLReader.pepXMLReader.parsePepXML(self, self.parser.trainingsetFiles)
                elif ".txt" in self.parser.trainingsetFiles[0].lower():
                    Main.TrainingSetTable =maxQuantTxTReader.maxQuantTxtReader.parseTxt(self, self.parser.trainingsetFiles[0])
                elif ".mzid" in self.parser.trainingsetFiles[0].lower():
                    Main.TrainingSetTable =mzIdentMLReader.mzIdentMLReader.parsemzID(self, self.parser.trainingsetFiles)
                else:
                    return False
                
                if len(Main.TrainingSetTable.index)>2:
                    return Main.TrainingSetTable
                else:
                    return False
            else:
                return False
                       
    def OnParserThreadFinish(self, results):
            if type(results)!=bool: 
                Main.TrainingSetTable = results
                Main.TrainingOrTestSet = QtWidgets.QTabWidget()
                Main.TrainingOrTestSet.setStyleSheet("margin: 2px")
                Main.sIndex = self.addTab(Main.TrainingOrTestSet,"Setting up the training set:")
                Main.CreateTrainingTab(self)
                Main.progress1.setValue(100)
                self.setCurrentIndex(Main.sIndex)
                Main.RandomForestPerformed = True
                Main.pdf.setEnabled(True)   
            else:
                self.Message("An error occurred. The ID approach requires id files to make a graph out of (pepXML, mzID or summary.txt), then corresponding quality tsvs or json files. The samples in the quality files should correspond to the samples in the ID files and the variables should correspond to the original analysis files.")
                Main.progress1.setValue(0)
                self.onLongitudinalClicked()
                
                

    def CreateTrainingTab(self):
        # Create the tab which will contain the graph:
        Main.tplot = FigureCanvas
        try:
                Main.TrainingSetPlot 
                Main.TrainingSetPlot .clear()
        except:
                Main.TrainingSetPlot  = None
        Main.TrainingSetPlot = RFSelectionPlots.RFSelectionPlots( Main.TrainingSetTable, "training") # element = column index used for the y-value
        
        #Button:
        Main.TrainingOrTestSet.badbtn = QtWidgets.QPushButton(
                'This is my selection for suboptimal quality.',
                Main.TrainingOrTestSet)
        Main.TrainingOrTestSet.badbtn.setEnabled(False)
        
        #ProgressBar
        Main.TrainingOrTestSet.progress2 = QtWidgets.QProgressBar()
        
        RFSelectionGrid = QtWidgets.QGridLayout(Main.TrainingOrTestSet)
        RFSelectionGrid.addWidget(Main.TrainingSetPlot,0,0,1,3)
        RFSelectionGrid.addWidget(Main.TrainingOrTestSet.badbtn,2,1,2,1)
        RFSelectionGrid.addWidget(Main.TrainingOrTestSet.progress2,3,1,2,1)
                
        self.TrainingOrTestSet.badbtn.clicked.connect(lambda: self.RandomForestSelection())
        
    def RFFinished(self,results):
        if Main.h2oError:
            QtWidgets.QMessageBox.warning(self, "Error","H2O init failed. Try downgrading your java jdk to 8 and make sure the h2o jar is still in the h2o folder of the Assurance download. You can also check myerr.txt for more information.")
            Main.EnableAnalysisButtons(self)
            self.setCurrentIndex(0)
            return
        if hasattr(RandomForest.RandomForest, "performance"):
            RandomForestResultsTab.LongitudinalTab.printModelResults(self)
        else:
            QtWidgets.QMessageBox.warning(self, "Error","Something went wrong with h2o analysis.")
            Main.EnableAnalysisButtons(self)
            self.setCurrentIndex(0)
        
        Main.EnableAnalysisButtons(self)
        
            
    
    def RandomForestSelection(self):
        Main.TrainingOrTestSet.badbtn.setEnabled(False)
        tRF = Threads.SideThread(lambda: RandomForest.RandomForest.RFFromGraph(self))
        tRF.signals.result.connect(self.RFFinished)
        self.threadpool.start(tRF)
    
    def onPDFClicked(self):
        Main.DisableAnalysisButtons(self)
        tPDF = Threads.SideThread(lambda: PDFWriter.OutputWriter.producePDF(self,now))
        tPDF.signals.result.connect(self.PDFFinished)
        globalVars.var.threadpool.start(tPDF)
    
    def PDFFinished(self):
        Main.EnableAnalysisButtons(self)    

    @QtCore.pyqtSlot()
    def Message(self, words):
        QtWidgets.QMessageBox.warning(self, "Message",words)
    
        
