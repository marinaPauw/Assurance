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
import datetime
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
        IndMetricsTab.sampleBox.addItem("")
        for sample in UI_MainWindow.Ui_MainWindow.metrics[0].index:
            IndMetricsTab.sampleBox.addItem(str(sample))
        IndMetricsTab.sampleBox.activated[str].connect(lambda x: IndMetricsTab.sample_change(self, text=IndMetricsTab.sampleBox.currentText()))
        UI_MainWindow.Ui_MainWindow.progress1.setValue(80)
        
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
        IndMetricsTab.comboBox.setCurrentIndex( UI_MainWindow.Ui_MainWindow.listOfMetrics.index(text))
        UI_MainWindow.Ui_MainWindow.progress1.setValue(100)

    def sample_change(self, text):
        if text in UI_MainWindow.Ui_MainWindow.metrics[0].index:
                UI_MainWindow.Ui_MainWindow.sampleSelected = text
                if UI_MainWindow.Ui_MainWindow.sampleSelected in IndividualMetrics.MyIndMetricsCanvas.table.index:
                        sIndex = IndividualMetrics.MyIndMetricsCanvas.table.index.tolist().index(UI_MainWindow.Ui_MainWindow.sampleSelected)
                elif type(UI_MainWindow.Ui_MainWindow.sampleSelected) == int:
                        sIndex = int(UI_MainWindow.Ui_MainWindow.sampleSelected)
                if hasattr(IndividualMetrics.MyIndMetricsCanvas,"ann"):
                        IndividualMetrics.MyIndMetricsCanvas.ann.remove()
                if hasattr(IndividualMetrics.MyIndMetricsCanvas,"lines"):
                    IndividualMetrics.MyIndMetricsCanvas.lines.remove() 
                IndividualMetrics.MyIndMetricsCanvas.ax.plot(IndividualMetrics.MyIndMetricsCanvas.samplenames,  IndividualMetrics.MyIndMetricsCanvas.table[IndividualMetrics.MyIndMetricsCanvas.element], linestyle="-",marker='o', markerfacecolor = "dimgrey",color = "black")
                IndividualMetrics.MyIndMetricsCanvas.ax.plot(IndividualMetrics.MyIndMetricsCanvas.samplenames[sIndex], IndividualMetrics.MyIndMetricsCanvas.table[IndividualMetrics.MyIndMetricsCanvas.element].loc[UI_MainWindow.Ui_MainWindow.sampleSelected], linestyle="none", marker='o', markerfacecolor='limegreen', markeredgecolor='darkgreen')
                if type(IndividualMetrics.MyIndMetricsCanvas.table[IndividualMetrics.MyIndMetricsCanvas.element].iloc[0])!= datetime.datetime:
                    xlim = IndividualMetrics.MyIndMetricsCanvas.ax.get_xlim()
                    thisylim = IndividualMetrics.MyIndMetricsCanvas.ax.get_ylim()
                    yaxrange = abs(thisylim[1])-abs(thisylim[0])
                    svalue = (IndividualMetrics.MyIndMetricsCanvas.ax.get_xticks()[sIndex])
                    offsets = [svalue,IndividualMetrics.MyIndMetricsCanvas.table[IndividualMetrics.MyIndMetricsCanvas.element].iloc[sIndex]+(yaxrange/6)]
                    stringify = "x:" + str(IndividualMetrics.MyIndMetricsCanvas.samplenames[sIndex]) + "\ny:" + str(MyIndMetricsCanvas.table[IndividualMetrics.MyIndMetricsCanvas.element].iloc[sIndex])
                    IndividualMetrics.MyIndMetricsCanvas.ann = IndividualMetrics.MyIndMetricsCanvas.ax.annotate(stringify, xy=(svalue,IndividualMetrics.MyIndMetricsCanvas.table[IndividualMetrics.MyIndMetricsCanvas.element].iloc[sIndex]), xytext=(offsets[0], offsets[1]), color="k", 
                            size=10,ha = 'center', va="center", bbox=dict(facecolor='white', edgecolor='blue', pad=3.0))           
                else:
                    xlim = IndividualMetrics.MyIndMetricsCanvas.ax.get_xlim()
                    diffBetweenDpAndMin = IndividualMetrics.MyIndMetricsCanvas.table[IndividualMetrics.MyIndMetricsCanvas.element].iloc[sIndex] - IndividualMetrics.MyIndMetricsCanvas.table[IndividualMetrics.MyIndMetricsCanvas.element].min()
                    diffinDays = diffBetweenDpAndMin.days
                    yaxmin = IndividualMetrics.MyIndMetricsCanvas.ax.get_yticks().min()
                    yaxrange = IndividualMetrics.MyIndMetricsCanvas.ax.get_yticks().max() -yaxmin 
                    ylabel = str(IndividualMetrics.MyIndMetricsCanvas.table[IndividualMetrics.MyIndMetricsCanvas.element].iloc[sIndex]).split(" ")[0]
                    yVal = yaxmin + diffinDays
                    svalue = (IndividualMetrics.MyIndMetricsCanvas.ax.get_xticks()[sIndex])
                    offsets = [svalue,yVal+(yaxrange/6)]
                    stringify = "x:" + str(IndividualMetrics.MyIndMetricsCanvas.samplenames[sIndex]) + "\ny:" + str(ylabel)
                    IndividualMetrics.MyIndMetricsCanvas.ann = IndividualMetrics.MyIndMetricsCanvas.ax.annotate(stringify, xy=(svalue,IndividualMetrics.MyIndMetricsCanvas.table[IndividualMetrics.MyIndMetricsCanvas.element].iloc[sIndex]), xytext=(offsets[0], offsets[1]), color="k", 
                        size=10,ha = 'center', va="center", bbox=dict(facecolor='white', edgecolor='blue', pad=3.0))           
                 
                IndividualMetrics.MyIndMetricsCanvas.fig.canvas.draw()    
                samples = list(UI_MainWindow.Ui_MainWindow.metrics[0].index)
                IndMetricsTab.sampleBox.setCurrentIndex(samples.index(text)+1) #Because the first one is
                UI_MainWindow.Ui_MainWindow.progress1.setValue(100)
