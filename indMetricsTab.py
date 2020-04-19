import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
from scipy.spatial import distance_matrix
import UI_MainWindow
import PCAGraph
import DataPreparation
import FileInput
import IndividualMetrics
import PCA


class IndMetricsTab(QtWidgets.QWidget):
    def createTab(self, whichds):
        IndMetricsTab.itab = QtWidgets.QTabWidget()
        self.iIndex = self.addTab(IndMetricsTab.itab,
                                 "Individual metrics")
        IndMetricsTab.createGraph(self, whichds)

    def createGraph(self, whichds):
        IndMetricsTab.comboBox = QtWidgets.QComboBox()
        for metric in UI_MainWindow.Ui_MainWindow.listOfMetrics:
            IndMetricsTab.comboBox.addItem(metric)
        IndMetricsTab.comboBox.activated[str].connect(lambda x: IndMetricsTab.metric_change(self, text=IndMetricsTab.comboBox.currentText()))
        IndMetricsTab.sampleBox = QtWidgets.QComboBox()
        for sample in UI_MainWindow.Ui_MainWindow.metrics[0].index:
            IndMetricsTab.sampleBox.addItem(str(sample))
        IndMetricsTab.sampleBox.activated[str].connect(lambda x: IndMetricsTab.sample_change(self, text=IndMetricsTab.sampleBox.currentText()))
        UI_MainWindow.Ui_MainWindow.progress2.setValue(80)
        
        #Create layout
        vbox = QtWidgets.QVBoxLayout(IndMetricsTab.itab)
        hbox15 = QtWidgets.QHBoxLayout()
        hbox15.addStretch()
        hbox15.addWidget(IndMetricsTab.sampleBox)
        vbox.addLayout(hbox15)
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addStretch()
        try:
            indMetPlot
            indMetPlot.clear()
        except NameError:
            indMetPlot = None
        indMetPlot = IndividualMetrics.MyIndMetricsCanvas(UI_MainWindow.Ui_MainWindow.NumericMetrics[whichds],
                            UI_MainWindow.Ui_MainWindow.NumericMetrics[whichds], UI_MainWindow.Ui_MainWindow.element, False)
        hbox2.addWidget(indMetPlot)
        hbox2.addStretch()
        vbox.addLayout(hbox2)
        hbox3 =  QtWidgets.QHBoxLayout()
        hbox3.addStretch()
        hbox3.addWidget(IndMetricsTab.comboBox)
        hbox3.addStretch()
        vbox.addLayout(hbox3)
        vbox.setContentsMargins(30, 20, 30, 100)
        self.setCurrentIndex(self.iIndex)
        UI_MainWindow.Ui_MainWindow.EnableAnalysisButtons(self)

    def metric_change(self, text):
        UI_MainWindow.Ui_MainWindow.element = text
        whichds = 0
        for dataset in range(len(UI_MainWindow.Ui_MainWindow.NumericMetrics)):
                if UI_MainWindow.Ui_MainWindow.element in UI_MainWindow.Ui_MainWindow.NumericMetrics[dataset].columns:
                    whichds = dataset
                    break
        UI_MainWindow.Ui_MainWindow.removeTab(self, self.iIndex)
        IndMetricsTab.createTab(self, whichds)
        UI_MainWindow.Ui_MainWindow.progress2.setValue(100)

    def sample_change(self, text):
        UI_MainWindow.Ui_MainWindow.sampleSelected = text
        for dataset in range(len(UI_MainWindow.Ui_MainWindow.NumericMetrics)):
                if UI_MainWindow.Ui_MainWindow.element in UI_MainWindow.Ui_MainWindow.metrics[dataset].columns:
                    whichds = dataset
                    break

        UI_MainWindow.Ui_MainWindow.removeTab(self , self.iIndex)
        IndMetricsTab.createTab(self, whichds)
        UI_MainWindow.Ui_MainWindow.progress2.setValue(100)
