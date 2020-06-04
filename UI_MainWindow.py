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
#import FileInput
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
import RandomForestResultsTab
import FeatureImportancePlot
import PDFWriter
import tempfile
import datetime
import OutlierTab
import indMetricsTab
import maxQuantTxTReader
import mzIdentMLReader
import FileInput
import os
import Threads
import Datasets
import ctypes
import subprocess


class Ui_MainWindow(QtWidgets.QTabWidget):
    def setupUi(self):
        sys.stdout = open("mylog.txt", "w")
        sys.stderr = open("myerr.txt", "w")
        self.setWindowIcon(QtGui.QIcon('AssuranceIcon.png'))
        myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        Ui_MainWindow.threadpool = QtCore.QThreadPool()
        self.setWindowTitle("Assurance")
        self.resize(800,650)
        #print(str(os.environ["JAVA_HOME"]))
        Ui_MainWindow.Nulvalues = []
        Ui_MainWindow.firstOutlierlist = []
        Ui_MainWindow.secondOutlierlist = []
        Ui_MainWindow.firstpossOutlierlist = []
        Ui_MainWindow.secondpossOutlierlist = []
        Ui_MainWindow.TrainingError = False
        Ui_MainWindow.h2oError= False
        
        #Create an object for datasets:
        database = Datasets.Datasets()
        
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
        #Ui_MainWindow.cpusLabel= QtWidgets.QLabel(self.leftFrame)
        #Ui_MainWindow.cpusTextBox = QtWidgets.QLineEdit(self.leftFrame)
        Ui_MainWindow.CLOLabel= QtWidgets.QLabel(self.leftFrame)
        Ui_MainWindow.CLOTextBox = QtWidgets.QLineEdit(self.leftFrame)
        Ui_MainWindow.CUOLabel= QtWidgets.QLabel(self.leftFrame)
        Ui_MainWindow.CUOTextBox = QtWidgets.QLineEdit(self.leftFrame) 
        Ui_MainWindow.RUNButton = QtWidgets.QPushButton(self.leftFrame)
        Ui_MainWindow.textedit =QtWidgets.QTextEdit(readOnly=True)
        

        #Widget stylesheets:
        Ui_MainWindow.BrowseButton.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
        Ui_MainWindow.RUNButton.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
       # Ui_MainWindow.cpusTextBox.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
        Ui_MainWindow.CLOTextBox.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
        Ui_MainWindow.CUOTextBox.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
        Ui_MainWindow.fileList.setStyleSheet("padding: 3px;")
        Ui_MainWindow.textedit.setStyleSheet("background-color: rgb(240,240,240);padding: 1px;")

        #Widget texts:
        Ui_MainWindow.BrowseButton.setText("Browse ")
        Ui_MainWindow.files.setText("Folder:")
        #Ui_MainWindow.cpusLabel.setText("Number of CPU's: ")
        Ui_MainWindow.CLOLabel.setText("m/z Lower Offset:")
        Ui_MainWindow.CUOLabel.setText("m/z Upper Offset:")
        Ui_MainWindow.RUNButton.setText("Run")

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
        #Multiple cpus not included at this moment
        #hbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.leftFrame)
        #hbox2.addWidget(Ui_MainWindow.cpusLabel)
        #hbox2.addWidget(Ui_MainWindow.cpusTextBox)
        #QuaMetervbox.addLayout(hbox2)
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
        Ui_MainWindow.iRT =  QtWidgets.QPushButton(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRTFilelist = QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRTtoleranceLabel =QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRTminintensityLabel =QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRTminpeptidesLabel =QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRTtoleranceTB =QtWidgets.QLineEdit(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRTminintensityTB =QtWidgets.QLineEdit(Ui_MainWindow.rightFrame)
        Ui_MainWindow.iRTminpeptidesTB =QtWidgets.QLineEdit(Ui_MainWindow.rightFrame)
        Ui_MainWindow.minintensityLabel =QtWidgets.QLabel(Ui_MainWindow.rightFrame)
        Ui_MainWindow.minintensityTB =QtWidgets.QLineEdit(Ui_MainWindow.rightFrame)
        Ui_MainWindow.Stextedit =QtWidgets.QTextEdit(readOnly=True)
        Ui_MainWindow.IRTinputFile = None


        #Widget stylesheets:
        Ui_MainWindow.SBrowseButton.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Ui_MainWindow.SRUNButton.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Ui_MainWindow.SfileList.setStyleSheet(" padding: 3px;")
        Ui_MainWindow.divisionTextBox.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Ui_MainWindow.MTTextBox.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Ui_MainWindow.RTTextBox.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Ui_MainWindow.Stextedit.setStyleSheet("background-color: rgb(240,240,240); padding: 1px;")
        Ui_MainWindow.iRT.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Ui_MainWindow.iRTtoleranceTB.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Ui_MainWindow.iRTminintensityTB.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Ui_MainWindow.iRTminpeptidesTB.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Ui_MainWindow.minintensityTB.setStyleSheet("background-color: rgb(240,240,240); padding: 3px;")
        Ui_MainWindow.SBrowseButton.setFixedHeight(30)
        Ui_MainWindow.SBrowseButton.setFixedHeight(30)

        #For error logging:
        Ui_MainWindow.errors = []
        
        #Clicked.connect
        Ui_MainWindow.SBrowseButton.clicked.connect(SwaMe.SwaMe.onSwaMeBrowseClicked)
        Ui_MainWindow.SRUNButton.clicked.connect(SwaMe.SwaMe.onSwaMeRUNClicked)

        #Widget texts:
        Ui_MainWindow.SBrowseButton.setText("Browse:")
        Ui_MainWindow.Sfiles.setText("Folder: ")
        Ui_MainWindow.divisionLabel.setText("Number of RT segments: ")
        Ui_MainWindow.MTLabel.setText("MassTolerance (m/z):")
        Ui_MainWindow.RTLabel.setText("RTTolerance (min):")
        Ui_MainWindow.SRUNButton.setText("Run")
        Ui_MainWindow.iRTtoleranceLabel.setText("iRTtolerance (min):")
        Ui_MainWindow.iRTminintensityLabel.setText("Minimum IRTIntensity:")
        Ui_MainWindow.minintensityLabel.setText("Minimum Intensity:")
        Ui_MainWindow.iRTminpeptidesLabel.setText("Minimum number of fragments per iRTpeptide:")
        Ui_MainWindow.iRT.setText("iRT")
        Ui_MainWindow.iRTFilelist.setText("File...")
        
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
        SwaMehbox3 = QtWidgets.QHBoxLayout(Ui_MainWindow.rightFrame)
        SwaMehbox3.addWidget(Ui_MainWindow.divisionLabel)
        SwaMehbox3.addWidget(Ui_MainWindow.divisionTextBox)
        SwaMehbox3.addWidget(Ui_MainWindow.MTLabel)
        SwaMehbox3.addWidget(Ui_MainWindow.MTTextBox)
        SwaMehbox3.addWidget(Ui_MainWindow.RTLabel)
        SwaMehbox3.addWidget(Ui_MainWindow.RTTextBox)
        SwaMehbox3.addWidget(Ui_MainWindow.minintensityLabel)
        SwaMehbox3.addWidget(Ui_MainWindow.minintensityTB)
        SwaMevbox.addLayout(SwaMehbox3)
        SwaMehbox2 = QtWidgets.QHBoxLayout(Ui_MainWindow.rightFrame)
        SwaMehbox2.addWidget(Ui_MainWindow.iRT)
        SwaMehbox2.addWidget(Ui_MainWindow.iRTFilelist)
        SwaMevbox.addLayout(SwaMehbox2)
        SwaMehbox4 = QtWidgets.QHBoxLayout(Ui_MainWindow.rightFrame)
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
        Ui_MainWindow.pdf.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
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
        Ui_MainWindow.browse.clicked.connect(lambda:self.onBrowseClicked(database))
        Ui_MainWindow.Outliers.clicked.connect(self.onOutliersClicked)
        Ui_MainWindow.IndMetrics.clicked.connect(self.onIndMetricsClicked)
        Ui_MainWindow.Longitudinal.clicked.connect(self.onLongitudinalClicked)
        Ui_MainWindow.iRT.clicked.connect(self.onIRTClicked)
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
        self.DisableAnalysisButtons()
        Ui_MainWindow.browse.setEnabled(True)

        QtCore.QMetaObject.connectSlotsByName(self)

    def frame_change(self, text):
        if text == "DDA analysis with QuaMeter":
            self.stacked.setCurrentWidget(self.leftFrame)
        elif text == "DIA analysis with SwaMe":
            self.stacked.setCurrentWidget(self.rightFrame)
        elif text == "Upload a file":
            self.stacked.setCurrentWidget(self.browseFrame)
            
    def progress_fn(self,n):
        Ui_MainWindow.UploadProgress.setValue(n)

    def enable_slot(self):
        PCAGraph.PCAGraph.loadingsToggledOn(self)
        OutlierTab.OutlierTab.LoadingsProgressBar.setValue(100)

    def disable_slot(self):
        PCAGraph.PCAGraph.loadingsToggledOff(self)

    @QtCore.pyqtSlot()    
    def onBrowseClicked(self, database):
              
        FileInput.BrowseWindow.__init__(Ui_MainWindow)
        inputFiles = FileInput.BrowseWindow.GetInputFile(Ui_MainWindow)
        #Threading
        tbrowse = Threads.SideThread(lambda: self.ParseFiles(inputFiles, database))
        tbrowse.signals.result.connect(self.ThreadingFix)
        self.threadpool.start(tbrowse)
        
        
    def ParseFiles(self, inputFiles, database):                
            FileInput.BrowseWindow.parseInputFiles(self, inputFiles)
            QtCore.QMetaObject.invokeMethod(self.UploadProgress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 20))
        
            try:
                Ui_MainWindow.assuranceDirectory = os.getcwd()
                os.chdir(os.path.dirname(os.path.abspath(inputFiles[0])))
            except:
                print("Changing the directory didn't work.")
            database.metrics = Ui_MainWindow.metrics
            if type(database.metrics) != bool:
                QtCore.QMetaObject.invokeMethod(Ui_MainWindow.UploadProgress, "setValue",
                                    QtCore.Qt.QueuedConnection,
                                    QtCore.Q_ARG(int, 30))
                if "Filename " in database.metrics[0].columns:
                    database.metrics[0] = database.metrics[0].rename(columns={"Filename ": 'Filename'})               
                if  "Filename" in database.metrics[0].columns:
                    filenames = database.metrics[0]["Filename"]
                    if ".mzml" in filenames[0].lower():
                        for item in range(0,len(filenames)):
                                if ".mzml" in filenames[item].lower():
                                    filenames[item] = filenames[item].split('.')[0]
                                if item == round(len(filenames)/4):
                                    QtCore.QMetaObject.invokeMethod(Ui_MainWindow.UploadProgress, "setValue",
                                    QtCore.Qt.QueuedConnection,
                                    QtCore.Q_ARG(int, 50))
                                elif item == round(len(filenames)/2):
                                    QtCore.QMetaObject.invokeMethod(Ui_MainWindow.UploadProgress, "setValue",
                                    QtCore.Qt.QueuedConnection,
                                    QtCore.Q_ARG(int, 70))
                    database.metrics[0].index = filenames
                    QtCore.QMetaObject.invokeMethod(Ui_MainWindow.UploadProgress, "setValue",
                                    QtCore.Qt.QueuedConnection,
                                    QtCore.Q_ARG(int, 80))
                Nm = DataPreparation.DataPrep.ExtractNumericColumns(self, database.metrics[0])
                
                QtCore.QMetaObject.invokeMethod(Ui_MainWindow.UploadProgress, "setValue",
                                    QtCore.Qt.QueuedConnection,
                                    QtCore.Q_ARG(int, 90))
                database.NumericMetrics = []
                database.NumericMetrics.append(DataPreparation.DataPrep.RemoveLowVarianceColumns(self, Nm))
                
                #database.NumericMetrics[0].index = database.metrics[0].index
                
                
                QtCore.QMetaObject.invokeMethod(Ui_MainWindow.UploadProgress, "setValue",
                                    QtCore.Qt.QueuedConnection,
                                    QtCore.Q_ARG(int, 100))
            return database
            
       
    
    
    
    def ThreadingFix(self, database):
        if FileInput.BrowseWindow.NullError:
            QtWidgets.QMessageBox.warning(self,"Error","Some format error occurred. Are there perhaps two spaces next to each other in the file? In a tsv these can be seen as two columns.")
        if len(Ui_MainWindow.Nulvalues) >0:
            QtWidgets.QMessageBox.warning(self, "Warning","There were metrics that did not have values in them:" + str(Ui_MainWindow.Nulvalues))
        Ui_MainWindow.EnableAnalysisButtons(self)
        
        if type(database)==Datasets.Datasets:
            Ui_MainWindow.metrics = database.metrics
            Ui_MainWindow.NumericMetrics = database.NumericMetrics
            Ui_MainWindow.EnableAnalysisButtons(self)
        elif type(database)==bool:
            Ui_MainWindow.Message(self,"An error occurred. Please check that the input files are either mzQC, tsv or csv quality files. Multiple files of the same type are allowed.")
            database = Datasets.Datasets()
            Ui_MainWindow.UploadProgress.setValue(0)
            self.onBrowseClicked(database)

    @QtCore.pyqtSlot()
    def onOutliersClicked(self):
        self.DisableAnalysisButtons()

        Ui_MainWindow.progress1.show()
        Ui_MainWindow.progress1.setValue(10)

       
        self.EnableAnalysisButtons()
        if not hasattr(FileInput.BrowseWindow,"currentDataset"):
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
                        if len(Ui_MainWindow.firstOutlierlist)<1:#Either there were no outliers and the reanalysis is pointless, or this is the first.
                            Ui_MainWindow.firstOutlierlist = outliers["Filename"]
                        elif len(Ui_MainWindow.secondOutlierlist)<1:#Either there were no outliers and the reanalysis is pointless, or this is the second.
                            Ui_MainWindow.secondOutlierlist = outliers["Filename"]
                        if len(Ui_MainWindow.firstpossOutlierlist)<1:#Either there were no outliers and the reanalysis is pointless, or this is the first.
                            Ui_MainWindow.firstpossOutlierlist = PCA.PCA.possOutlierList
                        elif len(Ui_MainWindow.secondpossOutlierlist)<1:#Either there were no outliers and the reanalysis is pointless, or this is the second.
                            Ui_MainWindow.secondpossOutlierlist = PCA.PCA.possOutlierList
                        OutlierTab.OutlierTab.createTabWidget(self,now)
                        Ui_MainWindow.outliersDetected = True

    def setProgressVal(self, val):
        OutlierTab.OutlierTab.LoadingsProgressBar.setValue(val)                        

    def EnableBrowseButtons(self):
        Ui_MainWindow.browse.setEnabled(True)

    def DisableBrowseButtons(self):
        Ui_MainWindow.browse.setEnabled(False)

    def EnableQuaMeterArguments(self):
        
        Ui_MainWindow.files.setEnabled(True)
        Ui_MainWindow.fileList.setEnabled(True)
        #Ui_MainWindow.cpusLabel.setEnabled(True)
        #Ui_MainWindow.cpusTextBox.setEnabled(True)
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
        #Ui_MainWindow.cpusLabel.setEnabled(False)
        #Ui_MainWindow.cpusTextBox.setEnabled(False)
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
        Ui_MainWindow.minintensityLabel.setEnabled(True)
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
        Ui_MainWindow.minintensityLabel.setEnabled(False)
        Ui_MainWindow.DisableSwaMeIRTArguments(self)

    def EnableSwaMeIRTArguments(self):
        Ui_MainWindow.iRTtoleranceLabel.setEnabled(True)
        Ui_MainWindow.iRTminintensityLabel.setEnabled(True)
        Ui_MainWindow.iRTminpeptidesLabel.setEnabled(True)
        Ui_MainWindow.iRTtoleranceTB.setEnabled(True)
        Ui_MainWindow.iRTminintensityTB.setEnabled(True)
        Ui_MainWindow.iRTminpeptidesTB.setEnabled(True)
        Ui_MainWindow.minintensityTB.setEnabled(True)
        Ui_MainWindow.iRTFilelist.setEnabled(True)
        

    def DisableSwaMeIRTArguments(self):
        Ui_MainWindow.iRTtoleranceLabel.setEnabled(False)
        Ui_MainWindow.iRTminintensityLabel.setEnabled(False)
        Ui_MainWindow.iRTminpeptidesLabel.setEnabled(False)
        Ui_MainWindow.iRTtoleranceTB.setEnabled(False)
        Ui_MainWindow.iRTminintensityTB.setEnabled(False)
        Ui_MainWindow.iRTminpeptidesTB.setEnabled(False)
        Ui_MainWindow.minintensityTB.setEnabled(False)
        Ui_MainWindow.iRTFilelist.setEnabled(False)

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
        PCAGraph.PCAGraph.printForReport(self, now)# Print it now before reanalysis
        FileInput.BrowseWindow.currentDataset = FileInput.BrowseWindow.currentDataset.drop(Ui_MainWindow.outlierlist)
        Ui_MainWindow.onOutliersClicked(self)

    @pyqtSlot()
    def onIRTClicked(self):
         Ui_MainWindow.EnableSwaMeIRTArguments(self)
         Ui_MainWindow.IRTinputFile = FileInput.BrowseWindow.GetIRTInputFile(Ui_MainWindow)
         Ui_MainWindow.iRTFilelist.setText(Ui_MainWindow.IRTinputFile)

    @pyqtSlot()
    def onIndMetricsClicked(self):
        Ui_MainWindow.DisableAnalysisButtons(self)
        Ui_MainWindow.progress1.setValue(10)
        Ui_MainWindow.indMetrics = QtWidgets.QTabWidget()
        
       
        Ui_MainWindow.listOfMetrics = list()
        if "StartTimeStamp" in Ui_MainWindow.metrics[0].columns:
            Ui_MainWindow.listOfMetrics.append("StartTimeStamp")
        for dataset in range(len(Ui_MainWindow.NumericMetrics)): # For each dataset in all the datasets we have
            for element in Ui_MainWindow.NumericMetrics[dataset].columns:
                    Ui_MainWindow.listOfMetrics.append(element)
                    
        Ui_MainWindow.element = Ui_MainWindow.listOfMetrics[0]
        #-------------- widgets ---------------------------------------
        
        Ui_MainWindow.progress1.setValue(33)
        whichds = 0
        for dataset in range(len(Ui_MainWindow.NumericMetrics)):
                if Ui_MainWindow.element in Ui_MainWindow.NumericMetrics[dataset].columns:
                    whichds = dataset
                    break
        Ui_MainWindow.sampleSelected = Ui_MainWindow.NumericMetrics[0].index[0]
        indMetricsTab.IndMetricsTab.createTab(self, whichds)
        Ui_MainWindow.progress1.setValue(100)
        Ui_MainWindow.pdf.setEnabled(True)
        Ui_MainWindow.indMetricsGraphed = True

    
    def checkColumnNumberForPCA(self):
        if(len(Ui_MainWindow.NumericMetrics[0].columns) < 3):
            self.Message("There are less than three \
                              numeric columns in the dataset. PCA will not \
                              be performed.")
            self.progress1.setValue(0)
            self.EnableAnalysisButtons()
            return 0
        else: 
            return 1

    def checkSampleNumberForPCA(self):
        if(len(FileInput.BrowseWindow.currentDataset.index) < 4):
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
        Ui_MainWindow.DisableAnalysisButtons(self)
        Ui_MainWindow.predictionArea = [0, 0, 0, 0]
        # Bools to keep track:
        Ui_MainWindow.goodPredicted = False
        Ui_MainWindow.badPredicted = False
        Ui_MainWindow.goodpredictionList = []
        Ui_MainWindow.badpredictionList = []
        
        #Make a messagebox to ask how you wanna do this:
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle("Assurance - Longitudinal analysis")
        msgBox.setText("For this supervised approach you will need to set aside files that have not been included in the main dataset which will be randomly divided into test and training sets. You need to divide those files into examples of good and bad quality. How would you like to do so?")
        msgBox.addButton(QtWidgets.QPushButton('Select from graph of IDs'), QtWidgets.QMessageBox.YesRole)
        msgBox.addButton(QtWidgets.QPushButton('Select from table of quality metrics'), QtWidgets.QMessageBox.YesRole)
        msgBox.addButton(QtWidgets.QPushButton('Cancel'), QtWidgets.QMessageBox.RejectRole)
        ret = msgBox.exec_()

        if ret == 0: # They want the graph
            
            tpep = Threads.SideThread(self.GetTrainingSetTable)
            tpep.signals.result.connect(self.OnParserThreadFinish)
            self.threadpool.start(tpep)
            
            
        
        elif ret == 1:# They want the table
            FileInput.BrowseWindow.GetTrainingQualityFiles(self)
            if FileInput.BrowseWindow.NullError:
                QtWidgets.QMessageBox.warning(self,"Error","Is it possible there may be unnecessary spaces in your tsv? Two spaces next to each other will create a NaN column.Fix the file and upload it again.")
                FileInput.BrowseWindow.__init__(Ui_MainWindow)
                FileInput.BrowseWindow.GetTrainingQualityFiles(Ui_MainWindow)
            if hasattr(Ui_MainWindow,"Numerictrainingmetrics"):
                if len(Ui_MainWindow.Numerictrainingmetrics)>0:
                    Ui_MainWindow.TrainingOrTestSet = QtWidgets.QTabWidget()
                    Ui_MainWindow.TrainingOrTestSet.setStyleSheet("margin: 2px;")
                    Ui_MainWindow.sIndex = self.addTab(Ui_MainWindow.TrainingOrTestSet,"Setting up the training set:")
                    RandomForest.RandomForest.createTable(self)
                    self.setCurrentIndex(Ui_MainWindow.sIndex)
                    Ui_MainWindow.RandomForestPerformed = True
                    Ui_MainWindow.pdf.setEnabled(True)
                else:
                    QtWidgets.QMessageBox.warning(self,"Error","Something went wrong.")
            else:
                Ui_MainWindow.EnableAnalysisButtons(self) 
            
        elif ret == 2:#Cancelled
            Ui_MainWindow.EnableAnalysisButtons(self)
            
            
    def GetTrainingSetTable(self):
            FileInput.BrowseWindow.__init__(FileInput.BrowseWindow)
            TrainingSetfiles = FileInput.BrowseWindow.GetTrainingSetFiles(self)
            QtCore.QMetaObject.invokeMethod(Ui_MainWindow.progress1, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 20))
            Ui_MainWindow.TrainingSetTable = pd.DataFrame(columns = ["Filename","Number of distinct peptides","Number of spectra identified"])
            
            if TrainingSetfiles:
                if "pepxml" in TrainingSetfiles[0].lower():
                    Ui_MainWindow.TrainingSetTable = pepXMLReader.pepXMLReader.parsePepXML(self, TrainingSetfiles)
                elif ".txt" in TrainingSetfiles[0].lower():
                    Ui_MainWindow.TrainingSetTable =maxQuantTxTReader.maxQuantTxtReader.parseTxt(self, TrainingSetfiles[0])
                elif ".mzid" in TrainingSetfiles[0].lower():
                    Ui_MainWindow.TrainingSetTable =mzIdentMLReader.mzIdentMLReader.parsemzID(self, TrainingSetfiles)
                else:
                    return False
                
                if len(Ui_MainWindow.TrainingSetTable.index)>2:
                    return Ui_MainWindow.TrainingSetTable
                else:
                    return False
            else:
                return False
                       
    def OnParserThreadFinish(self, results):
            if type(results)!=bool: 
                Ui_MainWindow.TrainingSetTable = results
                Ui_MainWindow.TrainingOrTestSet = QtWidgets.QTabWidget()
                Ui_MainWindow.TrainingOrTestSet.setStyleSheet("margin: 2px")
                Ui_MainWindow.sIndex = self.addTab(Ui_MainWindow.TrainingOrTestSet,"Setting up the training set:")
                Ui_MainWindow.CreateTrainingTab(self)
                Ui_MainWindow.progress1.setValue(100)
                self.setCurrentIndex(Ui_MainWindow.sIndex)
                Ui_MainWindow.RandomForestPerformed = True
                Ui_MainWindow.pdf.setEnabled(True)   
            else:
                self.Message("An error occurred. The ID approach requires id files to make a graph out of (pepXML, mzID or summary.txt), then corresponding quality tsvs or json files. The samples in the quality files should correspond to the samples in the ID files and the variables should correspond to the original analysis files.")
                Ui_MainWindow.progress1.setValue(0)
                self.onLongitudinalClicked()
                
                

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
        
        #ProgressBar
        Ui_MainWindow.TrainingOrTestSet.progress2 = QtWidgets.QProgressBar()
        
        RFSelectionGrid = QtWidgets.QGridLayout(Ui_MainWindow.TrainingOrTestSet)
        RFSelectionGrid.addWidget(Ui_MainWindow.TrainingSetPlot,0,0,1,3)
        RFSelectionGrid.addWidget(Ui_MainWindow.TrainingOrTestSet.badbtn,2,1,2,1)
        RFSelectionGrid.addWidget(Ui_MainWindow.TrainingOrTestSet.progress2,3,1,2,1)
                
        self.TrainingOrTestSet.badbtn.clicked.connect(lambda: self.RandomForestSelection())
        
    def RFFinished(self,results):
        if Ui_MainWindow.TrainingError:
            QtWidgets.QMessageBox.warning(self, "Error","The training set did not contain enough of both good and bad data to perform the analysis")
            Ui_MainWindow.EnableAnalysisButtons(self)
            self.setCurrentIndex(0)
            return
        elif Ui_MainWindow.TrainingError:
            QtWidgets.QMessageBox.warning(self, "Error","H2O init failed. Try downgrading your java jdk to 8 and make sure the h2o jar is still in the h2o folder of the Assurance download. You can also check myerr.txt for more information.")
            Ui_MainWindow.EnableAnalysisButtons(self)
            self.setCurrentIndex(0)
            return
        RandomForestResultsTab.LongitudinalTab.printModelResults(self)
        Ui_MainWindow.EnableAnalysisButtons(self)
        
            
    
    def RandomForestSelection(self):
        Ui_MainWindow.TrainingOrTestSet.badbtn.setEnabled(False)
        tRF = Threads.SideThread(lambda: RandomForest.RandomForest.RFFromGraph(self))
        tRF.signals.result.connect(self.RFFinished)
        Ui_MainWindow.threadpool.start(tRF)
    
    def onPDFClicked(self):
        Ui_MainWindow.DisableAnalysisButtons(self)
        tPDF = Threads.SideThread(lambda: PDFWriter.OutputWriter.producePDF(self,now))
        tPDF.signals.result.connect(self.PDFFinished)
        Ui_MainWindow.threadpool.start(tPDF)
    
    def PDFFinished(self):
        Ui_MainWindow.EnableAnalysisButtons(self)    

    @QtCore.pyqtSlot()
    def Message(self, words):
        QtWidgets.QMessageBox.warning(self, "Message",words)
    
        
