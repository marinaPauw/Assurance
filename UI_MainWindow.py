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
        self.showMaximized()

        # fonts and style:
        Ui_MainWindow.boldfont = QtGui.QFont()
        Ui_MainWindow.boldfont.setBold(True)

        # Setting up the home tab:
        Ui_MainWindow.tab = QtWidgets.QWidget()
        self.setCurrentIndex(0)
        self.tab.main_layout = QtWidgets.QVBoxLayout()
        self.addTab(self.tab, "Home")
        self.tab.setStyleSheet("background-color: gainsboro;")
        
        #All the buttons:
        self.tab.QuaMeterbutton = QtWidgets.QPushButton(self.tab)
        self.tab.QuaMeterbutton.setStyleSheet("background-color: rgb(240,240,240);")
        self.tab.SwaMebutton = QtWidgets.QPushButton(self.tab)
        self.tab.SwaMebutton.setStyleSheet("background-color: rgb(240,240,240);")
        self.tab.browse = QtWidgets.QPushButton(self.tab)
        self.tab.browse.setStyleSheet("background-color: rgb(240,240,240);")
        self.tab.Outliers = QtWidgets.QPushButton(self.tab)
        self.tab.Outliers.setStyleSheet("background-color: rgb(240,240,240);")
        self.tab.IndMetrics = QtWidgets.QPushButton(self.tab)
        self.tab.IndMetrics.setStyleSheet("background-color: rgb(240,240,240);")
        self.tab.Longitudinal = QtWidgets.QPushButton(self.tab)
        self.tab.Longitudinal.setStyleSheet("background-color: rgb(240,240,240);")
        self.tab.QuaMeterbutton.clicked.connect(self.onQuaMeterClicked)
        self.tab.SwaMebutton.clicked.connect(self.onSwaMeClicked)
        self.tab.browse.clicked.connect(self.onBrowseClicked)
        self.tab.Outliers.clicked.connect(self.onOutliersClicked)
        self.tab.IndMetrics.clicked.connect(self.onIndMetricsClicked)
        self.tab.Longitudinal.clicked.connect(self.onLongitudinalClicked)

        # Labels and progressbars
        Ui_MainWindow.filename = QtWidgets.QLabel(self.tab)
        Ui_MainWindow.filename.setGeometry(QtCore.QRect(90, 120, 300, 20))
        self.tab.uploadLabel = QtWidgets.QLabel()
        self.tab.progress1 = QtWidgets.QProgressBar()
        self.tab.progress1.setGeometry(200, 80, 250, 20)
        self.tab.chooseLabel = QtWidgets.QLabel()
        self.tab.progress2 = QtWidgets.QProgressBar()
        self.tab.progress2.setGeometry(200, 80, 250, 20)

        vbox = QtWidgets.QVBoxLayout(self.tab)
        vbox.addStretch()
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(Ui_MainWindow.tab.QuaMeterbutton)
        hbox.addWidget(Ui_MainWindow.tab.SwaMebutton)
        hbox.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addLayout(hbox)
        hbox6 = QtWidgets.QHBoxLayout()
        hbox6.addWidget(self.tab.uploadLabel)
        hbox6.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addLayout(hbox6)

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(Ui_MainWindow.filename)
        hbox2.addWidget(Ui_MainWindow.tab.browse)
        Ui_MainWindow.tab.browse.setFixedHeight(30)
        vbox.addLayout(hbox2)
        hbox2.setAlignment(QtCore.Qt.AlignLeft)
        hbox7 = QtWidgets.QHBoxLayout()
        hbox7.addWidget(self.tab.chooseLabel)
        hbox7.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addLayout(hbox7)
        hbox3 = QtWidgets.QHBoxLayout()
        vbox.setSpacing(80)
        hbox3.addWidget(self.tab.Outliers)
        hbox3.addWidget(self.tab.progress1)
        hbox3.setAlignment(QtCore.Qt.AlignLeft)
        self.tab.Outliers.setFixedHeight(50)
        self.tab.Outliers.setFixedWidth(150)
        vbox.addLayout(hbox3)
        hbox3.setAlignment(QtCore.Qt.AlignCenter)
        hbox9 = QtWidgets.QHBoxLayout()
        hbox9.addWidget(self.tab.IndMetrics)
        hbox9.addWidget(self.tab.progress2)
        hbox9.setAlignment(QtCore.Qt.AlignLeft)
        self.tab.IndMetrics.setFixedHeight(50)
        self.tab.IndMetrics.setFixedWidth(150)
        vbox.addLayout(hbox9)
        hbox4 = QtWidgets.QHBoxLayout()
        hbox4.addWidget(self.tab.Longitudinal)
        self.tab.Longitudinal.setFixedHeight(50)
        self.tab.Longitudinal.setFixedWidth(150)
        vbox.addLayout(hbox4)
        hbox4.setAlignment(QtCore.Qt.AlignLeft)
        vbox.setAlignment(QtCore.Qt.AlignLeft)
        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(self)

    def enable_slot():
        PCAGraph.PCAGraph.loadingsToggledOn()
        Ui_MainWindow.PCA.LoadingsProgressBar.setValue(100)

    def disable_slot():
        PCAGraph.PCAGraph.loadingsToggledOff()

    @pyqtSlot()
    def onQuaMeterClicked(self):
        Ui_MainWindow.DisableButtons(self)
        QuaMeter.QuaMeter.setupUI(self)


    @pyqtSlot()
    def onSwaMeClicked(self):
        Ui_MainWindow.DisableButtons(self)
        SwaMe.SwaMe.setupUI(self)

    @pyqtSlot()
    def onBrowseClicked(self):
        Ui_MainWindow.DisableButtons(self)
        FileInput.BrowseWindow.__init__(FileInput.BrowseWindow, Ui_MainWindow)
        inputFile = FileInput.BrowseWindow.GetInputFile(Ui_MainWindow)
        global metrics
        if inputFile:
            filepath = FileInput.BrowseWindow.FileCheck(inputFile)
            Ui_MainWindow.metrics = FileInput.BrowseWindow.metricsParsing(inputFile)
            Ui_MainWindow.checkColumnLength(self)
            Ui_MainWindow.metrics.set_index(Ui_MainWindow.metrics.iloc[:,0])
            DataPreparation.DataPrep.ExtractNumericColumns(self.metrics)
            DataPreparation.DataPrep.RemoveLowVarianceColumns(self)
        Ui_MainWindow.EnableButtons(self)
        
    def checkColumnLength(self):
       if(len(Ui_MainWindow.metrics.columns)<1):
                QMessageBox.warning(self.tab,"Error:" ,"After removing low variance columns, there were no columns left from which to conduct any sort of analysis.")
                self.onBrowseClicked()
      

    @pyqtSlot()
    def onOutliersClicked(self):
        self.DisableButtons()

        Ui_MainWindow.tab.progress1.show()
        Ui_MainWindow.tab.progress1.setValue(10)

        # Check if you have the correct number of variables/samples
        self.checkColumnNumberForPCA()
        self.checkSampleNumberForPCA()
        self.EnableButtons()
        
        sampleToVariableRatio = PCA.PCA.\
            calculateSampleToVariableRatio(self, Ui_MainWindow.NumericMetrics)
        
        self.checkSampleToVariableRatio(sampleToVariableRatio);
       
        # Create PCA

        PCA.PCA.CreatePCAGraph(Ui_MainWindow.NumericMetrics)
        Ui_MainWindow.tab.progress1.setValue(51)
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
        Ui_MainWindow.EnableButtons(self)
        Ui_MainWindow.tab.progress1.setValue(100)
        PCAGraph.fig.canvas.mpl_connect("motion_notify_event",
                                        Ui_MainWindow.onhover)
        self.setCurrentIndex(oIndex)

    def EnableButtons(self):
        Ui_MainWindow.tab.browse.setEnabled(True)
        Ui_MainWindow.tab.Outliers.setEnabled(True)
        Ui_MainWindow.tab.IndMetrics.setEnabled(True)
        Ui_MainWindow.tab.Longitudinal.setEnabled(True)

    def DisableButtons(self):
        Ui_MainWindow.tab.browse.setEnabled(False)
        Ui_MainWindow.tab.Outliers.setEnabled(False)
        Ui_MainWindow.tab.IndMetrics.setEnabled(False)
        Ui_MainWindow.tab.Longitudinal.setEnabled(False)

    @pyqtSlot()
    def onIndMetricsClicked(self):
        # First open a pop-up window informing the user
        # that this takes a moment:
        Ui_MainWindow.DisableButtons(self)
        Ui_MainWindow.tab.progress2.show()
        Ui_MainWindow.tab.progress2.setValue(10)
        NumericMetrics = Ui_MainWindow.NumericMetrics
        global element
        lw = 2
        Ui_MainWindow.tab.progress2.setValue(33)
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
                    Ui_MainWindow.NumericMetrics, element, False, False)
            hbox2.addWidget(indMetPlot)
            hbox2.addStretch()
            vbox.addLayout(hbox2)

        #Ui_MainWindow.legend.show()
        Ui_MainWindow.EnableButtons(self)
        Ui_MainWindow.tab.progress2.setValue(100)
        self.setCurrentIndex(iIndex)

    def checkColumnNumberForPCA(self):
        if(len(self.NumericMetrics.columns) < 3):
            QMessageBox.warning(self, "Warning:", "There are less than three \
                              numeric columns in the dataset. PCA will not \
                              be performed.")

    def checkSampleNumberForPCA(self):
        if(len(self.NumericMetrics.index) < 4):
            QMessageBox.warning(self, "Warning:", "There are less than three samples in the dataset. PCA will not be performed.")
            
    def checkSampleToVariableRatio(self, sampleToVariableRatio):
         if(sampleToVariableRatio < 5):
            if(len(self.NumericMetrics.index) < 100):
                QMessageBox.warning(self, "Warning:",
                                  "Consider consulting PCA literature to ascertain whether the ratio of sample size to number of variables is sufficient to perform PCA in this dataset.")


    def enable_legend(metric):
        IndividualMetrics.MyIndMetricsCanvas.ShowLegend(metric)

    def disable_legend(metric):
        IndividualMetrics.MyIndMetricsCanvas.HideLegend(metric)

    @pyqtSlot()
    def onLongitudinalClicked(self):
        Ui_MainWindow.DisableButtons(self)
        Ui_MainWindow.predictionArea = [0, 0, 0, 0]
        # Bools to keep track:
        Ui_MainWindow.goodPredicted = False
        Ui_MainWindow.badPredicted = False
        Ui_MainWindow.goodpredictionList = []
        Ui_MainWindow.badpredictionList = []

        # InputtingFile:
        QMessageBox.about(Ui_MainWindow.tab,  "You have selected Longitudinal analysis.",
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
            Ui_MainWindow, Ui_MainWindow.metrics.iloc[:, 0])
        if(len(samplenames) != len(set(samplenames))):
            # if there are duplicates in the filenames column like RTsegments
            # or per swath metrics
            sampleNameColumn1Combination = samplenames[closestx[0]] + "-" \
                + str(self.metrics.iloc[closestx[0], 1])
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
        sampleSize = range(len(Ui_MainWindow.NumericMetrics.index))
        PCA.Distances = self.calculateDistanceMatrix(PCA.finalDf)
        Ui_MainWindow.tab.progress1.setValue(60)
        self.metrics.index = self.metrics.iloc[:,0]
        medianDistances = Ui_MainWindow.createMedianDistances(self, sampleSize)
        outlierDistance = Ui_MainWindow.calculateOutLierDistances(self, medianDistances)
        Ui_MainWindow.tab.progress1.setValue(65)

        # Zscores:
        from scipy.stats import zscore
        medianDistances["zScore"] = zscore(medianDistances["MedianDistance"])
        medianDistances["outlier"] = medianDistances["zScore"].apply(
            lambda x: x <= -3.5 or x >= 3.5
        )
        print("The following runs were identified as outliers \
        based on their z-scores:")

        Ui_MainWindow.tab.progress1.setValue(75)
        Outliers = medianDistances[medianDistances["outlier"]]
        return Outliers

    def createMedianDistances(self, sampleSize):
        medianDistances = pd.DataFrame()
        medianDistances["Filename"] = self.metrics.index
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
        Ui_MainWindow.tab.Outliers.setText(_translate("MainWindow",
                                           "Detect Outliers"))
        Ui_MainWindow.tab.IndMetrics.setText(_translate("MainWindow",
                                             "Individual metrics"))
        Ui_MainWindow.tab.Longitudinal.setText(_translate("MainWindow",
                                               "Longitudinal analysis"))
        Ui_MainWindow.tab.browse.setText(_translate("MainWindow", "Browse: "))
        Ui_MainWindow.tab.QuaMeterbutton.setText(_translate("MainWindow", "Generate quality metrics with QuaMeter ID-Free"))
        Ui_MainWindow.tab.SwaMebutton.setText(_translate("MainWindow", "Generate quality metrics with SwaMe"))
        Ui_MainWindow.filename.setText(_translate("MainWindow", "   File...                  "))
        Ui_MainWindow.filename.setStyleSheet("background-color: white;")
        Ui_MainWindow.tab.uploadLabel.setText(_translate("MainWindow", "Upload a file (Either json, csv or tsv format):"))
        Ui_MainWindow.tab.uploadLabel.setFont(Ui_MainWindow.boldfont)
        Ui_MainWindow.tab.chooseLabel.setText(_translate("MainWindow", "Choose the analysis you would like to conduct:"))
        Ui_MainWindow.DisableButtons(self)
        Ui_MainWindow.tab.browse.setEnabled(True)
