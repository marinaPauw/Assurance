import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5 import MainWindow
import numpy as np
from scipy.spatial import distance_matrix
import Main
import PCAGraph
from Datasets import Datasets
import MainParser
import IndividualMetrics
from matplotlib.backends.backend_qt5agg import ( NavigationToolbar2QT as NavigationToolbar )
from matplotlib import backend_bases
import datetime
import globalVars

class IndMetricsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()    

    def createGraph(self, whichds): 
        #Widgets
        self.tickBox = QtWidgets.QCheckBox()
        self.tBoxLabel = QtWidgets.QLabel()
        self.tBoxLabel.setText("Hide unselected tick marks")
        self.comboBox = QtWidgets.QComboBox()
        for metric in globalVars.var.listOfMetrics:
            self.comboBox.addItem(metric)
        self.comboBox.activated[str].connect(lambda x: self.metric_change(text=self.comboBox.currentText()))
        self.sampleBox = QtWidgets.QComboBox()
        self.sampleBox.addItem("")
        for sample in globalVars.var.database.metrics[0].index:
            self.sampleBox.addItem(str(sample))
        self.sampleBox.activated[str].connect(lambda x: IndMetricsTab.sample_change(self, text=self.sampleBox.currentText()))
        self.tickBox.toggled.connect(self.hideTickMarks)
        Undozoombutton = QtWidgets.QPushButton()
        Undozoombutton.clicked.connect(self.home)
        Undozoombutton.setStyleSheet("background-color: rgb(240,240,240);padding: 3px;")
        Undozoombutton.setText("Undo zoom")
        globalVars.var.progress1.setValue(80)
        
        #Create layout
        vbox = QtWidgets.QVBoxLayout(globalVars.var.itab)
        hbox15 = QtWidgets.QHBoxLayout()
        hbox15.addStretch()
        hbox15.addWidget(self.sampleBox)
        vbox.addLayout(hbox15)
        hbox17 = QtWidgets.QHBoxLayout()
        hbox17.addStretch()
        hbox17.addWidget(self.tBoxLabel)
        hbox17.addWidget(self.tickBox)
        vbox.addLayout(hbox17)
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addStretch()
        plotlabel = QtWidgets.QLabel()
        plotlabel.setText(globalVars.var.element)
        boldfont = QtGui.QFont()
        boldfont.setBold(True)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(14)
        plotlabel.setFont(font)
        try:
            indMetPlot
            indMetPlot.clear()
        except NameError:
            indMetPlot = None
        indMetPlot = IndividualMetrics.MyIndMetricsCanvas(globalVars.var.database.numericMetrics[whichds],
                            globalVars.var.database.numericMetrics[whichds], globalVars.var.element, False)
        self.indMetPlot = indMetPlot
        self.originalylim = indMetPlot.ax.get_ylim()
        self.originalxlim = indMetPlot.ax.get_xlim()
        mpl_toolbar = NavigationToolbar(indMetPlot, globalVars.var.itab)
        self.mpl_toolbar = mpl_toolbar
        plotvbox = QtWidgets.QVBoxLayout()
        plotvbox.addWidget(plotlabel)
        plotvbox.addWidget(indMetPlot)
        toolbarhbox = QtWidgets.QHBoxLayout()
        toolbarhbox.addWidget(mpl_toolbar)
        toolbarhbox.addStretch()
        toolbarhbox.addWidget(self.comboBox)
        toolbarhbox.addStretch()
        toolbarhbox.addWidget(Undozoombutton)
        plotvbox.addLayout(toolbarhbox)
        hbox2.addLayout(plotvbox)
        hbox2.addStretch()
        vbox.addLayout(hbox2)
        
        hbox3 =  QtWidgets.QHBoxLayout()
        hbox3.addStretch()
        hbox3.addWidget(self.comboBox)
        hbox3.addStretch()
        vbox.addLayout(hbox3)
        vbox.setContentsMargins(30, 20, 30, 100)

    def metric_change(self, text):
        globalVars.var.element = text
        whichds = 0
        for dataset in range(len(globalVars.var.database.metrics)):
                if globalVars.var.element in globalVars.var.database.metrics[dataset].columns:
                    whichds = dataset
                    break
        globalVars.var.removeTab(globalVars.var.iIndex)
        globalVars.var.SwitchIndMetricsTab(whichds,text)

    def sample_change(self, text):
        if text in globalVars.var.database.metrics[0].index:
                globalVars.var.sampleSelected = text
                if globalVars.var.sampleSelected in self.table.index:
                        sIndex = self.table.index.tolist().index(globalVars.var.sampleSelected)
                elif type(globalVars.var.sampleSelected) == int:
                        sIndex = int(globalVars.var.sampleSelected)
                if hasattr(self.indMetPlot,"ann"):
                        self.indMetPlot.ann.remove()
                if hasattr(self.indMetPlot,"lines"):
                    self.indMetPlot.lines.remove() 
                self.indMetPlot.ax.plot(self.indMetPlot.samplenames,  self.table[self.indMetPlot.element], linestyle="-",marker='o', markerfacecolor = "dimgrey",color = "black")
                self.indMetPlot.ax.plot(self.indMetPlot.samplenames[sIndex], self.table[self.indMetPlot.element].loc[globalVars.var.sampleSelected], linestyle="none", marker='o', markerfacecolor='limegreen', markeredgecolor='darkgreen')
                if type(self.table[self.indMetPlot.element].iloc[0])!= datetime.datetime:
                    xlim = self.indMetPlot.ax.get_xlim()
                    thisylim = self.indMetPlot.ax.get_ylim()
                    yaxrange = abs(thisylim[1])-abs(thisylim[0])
                    svalue = (self.indMetPlot.ax.get_xticks()[sIndex])
                    offsets = [svalue,self.table[self.indMetPlot.element].iloc[sIndex]+(yaxrange/6)]
                    stringify = "x:" + str(self.indMetPlot.samplenames[sIndex]) + "\ny:" + str(self.table[self.indMetPlot.element].iloc[sIndex])
                    self.indMetPlot.ann = self.indMetPlot.ax.annotate(stringify, xy=(svalue,self.table[self.indMetPlot.element].iloc[sIndex]), xytext=(offsets[0], offsets[1]), color="k", 
                            size=10,ha = 'center', va="center", bbox=dict(facecolor='white', edgecolor='blue', pad=3.0))           
                else:
                    xlim = self.indMetPlot.ax.get_xlim()
                    diffBetweenDpAndMin = self.table[self.indMetPlot.element].iloc[sIndex] - self.table[self.indMetPlot.element].min()
                    diffinDays = diffBetweenDpAndMin.days
                    yaxmin = self.indMetPlot.ax.get_yticks().min()
                    yaxrange = self.indMetPlot.ax.get_yticks().max() -yaxmin 
                    ylabel = str(self.table[self.indMetPlot.element].iloc[sIndex]).split(" ")[0]
                    yVal = yaxmin + diffinDays
                    svalue = (self.indMetPlot.ax.get_xticks()[sIndex])
                    offsets = [svalue,yVal+(yaxrange/6)]
                    stringify = "x:" + str(self.indMetPlot.samplenames[sIndex]) + "\ny:" + str(ylabel)
                    self.indMetPlot.ann = self.indMetPlot.ax.annotate(stringify, xy=(svalue,self.table[self.indMetPlot.element].iloc[sIndex]), xytext=(offsets[0], offsets[1]), color="k", 
                        size=10,ha = 'center', va="center", bbox=dict(facecolor='white', edgecolor='blue', pad=3.0))           
                #Have to check if hide tick marks are selected:
                if self.tickBox.isChecked():
                    #Find index of selected sample:
                    samples = list(self.indMetPlot.samplenames)
                    sIndex = samples.index(globalVars.var.sampleSelected)
                    labels = [""] * len(samples)
                    labels[sIndex] = globalVars.var.sampleSelected
                    self.indMetPlot.ax.set_xticklabels(labels)
           
                 
                self.indMetPlot.fig.canvas.draw()    
                samples = list(globalVars.var.database.metrics[0].index)
                self.sampleBox.setCurrentIndex(samples.index(text)+1) #Because the first one is
                globalVars.var.progress1.setValue(100)
                
    def hideTickMarks(self):
        if self.tickBox.isChecked():
            #Find index of selected sample:
            samples = list(self.indMetPlot.samplenames)
            sIndex = samples.index(globalVars.var.sampleSelected)
            labels = [""] * len(samples)
            labels[sIndex] = globalVars.var.sampleSelected
            self.indMetPlot.ax.set_xticklabels(labels)
           
        else:
            self.indMetPlot.ax.set_xticklabels(self.indMetPlot.samplenames)
        
        self.indMetPlot.fig.canvas.draw()  
        
    def home(self):
        self.indMetPlot.ax.set_xlim(self.originalxlim)
        self.indMetPlot.ax.set_ylim(self.originalylim)
        self.indMetPlot.fig.canvas.draw()
    