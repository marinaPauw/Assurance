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
from matplotlib.backends.backend_qt5agg import ( NavigationToolbar2QT as NavigationToolbar )
import FileInput
import PCA

class OutlierTab(QtWidgets.QTabWidget):

    def createTabWidget(self,now):
                # --------------------------------------Widgets-------------------------------------------
                        OutlierTab.PCA = QtWidgets.QTabWidget()
                        OutlierTab.PCA.PCAplot = PCAGraph.PCAGraph(now)
                        
                        OutlierTab.outliercolorlabel1 = QtWidgets.QLabel(OutlierTab.PCA)
                        OutlierTab.outliercolorlabel2 = QtWidgets.QLabel(OutlierTab.PCA)
                        OutlierTab.outlierlistLabel = QtWidgets.QLabel(OutlierTab.PCA)
                        OutlierTab.OutlierSamples = QtWidgets.QLabel(OutlierTab.PCA)
                        OutlierTab.OutlierSamples.setAlignment(QtCore.Qt.AlignLeft)
                        OutlierTab.possoutlierlistLabel = QtWidgets.QLabel(OutlierTab.PCA)
                        OutlierTab.possOutlierSamples = QtWidgets.QLabel(OutlierTab.PCA)
                        OutlierTab.possOutlierSamples.setAlignment(QtCore.Qt.AlignLeft)

                        oIndex = self.addTab(OutlierTab.PCA, "Outlier detection results")
                        OutlierTab.PCA.layout = QtWidgets.QVBoxLayout()
                        OutlierTab.PCA.Checkboxlabel = QtWidgets.QLabel(OutlierTab.PCA)
                        OutlierTab.PCA.Checkboxlabel.setText("Toggle loadings on/off:")
                        OutlierTab.PCA.Checkbox = QtWidgets.QCheckBox("Loadings",
                                                                         OutlierTab.PCA)
                        OutlierTab.PCA.Checkbox.setChecked(False)
                        OutlierTab.PCA.Checkbox.stateChanged.connect(
                            lambda x: UI_MainWindow.Ui_MainWindow.enable_slot(self)
                            if x else UI_MainWindow.Ui_MainWindow.disable_slot(self))
                        OutlierTab.LoadingsProgressBar = QtWidgets.QProgressBar()
                        OutlierTab.LoadingsProgressBar.setGeometry(200, 80, 50, 20)

                        
                        OutlierTab.PCA.Redolabel = QtWidgets.QLabel(OutlierTab.PCA)
                        OutlierTab.PCA.Redolabel.setText("Redo analysis without the extreme outliers:")
                        OutlierTab.PCA.Redobox = QtWidgets.QCheckBox("Redo",
                                                                         OutlierTab.PCA)
                        OutlierTab.PCA.Redobox.setChecked(False)
                        OutlierTab.PCA.Redobox.stateChanged.connect(
                            lambda x: UI_MainWindow.Ui_MainWindow.enable_reanalysis(self))

                    # --------------------------------------Layout-------------------------------------------

                        vbox2 = QtWidgets.QVBoxLayout(OutlierTab.PCA)
                        hbox = QtWidgets.QHBoxLayout(OutlierTab.PCA)
                        vbox3 = QtWidgets.QVBoxLayout(OutlierTab.PCA)
                        vbox3.addStretch()
                        vbox3.addWidget(OutlierTab.outliercolorlabel1)
                        vbox3.addWidget(OutlierTab.outliercolorlabel2)
                        vbox3.addWidget(OutlierTab.outlierlistLabel)
                        vbox3.addWidget(OutlierTab.OutlierSamples)
                        vbox3.addWidget(OutlierTab.possoutlierlistLabel)
                        vbox3.addWidget(OutlierTab.possOutlierSamples)
                        vbox3.addWidget(OutlierTab.PCA.Checkboxlabel)
                        vbox3.addWidget(OutlierTab.PCA.Checkbox)
                        vbox3.addWidget(OutlierTab.LoadingsProgressBar)
                        vbox3.addWidget(OutlierTab.PCA.Redolabel)
                        vbox3.addWidget(OutlierTab.PCA.Redobox)
                        vbox3.addStretch()
                        vbox3.setAlignment(QtCore.Qt.AlignLeft)

                        hbox.addLayout(vbox3)
                        vbox4 = QtWidgets.QVBoxLayout(OutlierTab.PCA)
                        OutlierTab.PCA.Emptyspace = QtWidgets.QLabel(OutlierTab.PCA)
                        OutlierTab.PCA.Emptyspace.setText(" ")
                        vbox4.addWidget(OutlierTab.PCA.Emptyspace)
                        hbox.addLayout(vbox4)
                        vbox2.setAlignment(QtCore.Qt.AlignCenter)
                        hbox.setAlignment(QtCore.Qt.AlignCenter)
                        vbox2.addLayout(hbox)
                        hbox2 = QtWidgets.QHBoxLayout(OutlierTab.PCA)
                        plotvbox = QtWidgets.QVBoxLayout()
                        plotvbox.addWidget(OutlierTab.PCA.PCAplot)
                        OutlierTab.mpl_toolbar = NavigationToolbar(OutlierTab.PCA.PCAplot,OutlierTab.PCA )
                        OutlierTab.mpl_toolbar.hide()
                        #plotvbox.addWidget(mpl_toolbar)
                        hbox.addLayout(plotvbox)
                        hbox2.setAlignment(QtCore.Qt.AlignCenter)
                        vbox2.addLayout(hbox2)
                        OutlierTab.retranslateUi2(OutlierTab.PCA)
                        UI_MainWindow.Ui_MainWindow.EnableAnalysisButtons(self)
                        UI_MainWindow.Ui_MainWindow.progress1.setValue(100)
                        OutlierTab.original_xlim = PCAGraph.ax.get_xlim()
                        OutlierTab.original_ylim = PCAGraph.ax.get_ylim()
                        PCAGraph.fig.canvas.mpl_connect("button_press_event",
                                                        OutlierTab.home)
                        PCAGraph.fig.canvas.mpl_connect("motion_notify_event",
                                                        OutlierTab.onhover)
                        PCAGraph.fig.canvas.mpl_connect('scroll_event', OutlierTab.zoom_fun)
                        self.setCurrentIndex(oIndex)
                        UI_MainWindow.Ui_MainWindow.pdf.setEnabled(True)
                        
    def onhover(event):
            vis = PCAGraph.annot.get_visible()
            if event.inaxes == PCAGraph.ax:
                cont, ind = PCAGraph.fig.contains(event)
                if cont:
                    OutlierTab.update_annot(event)
                    PCAGraph.annot.set_visible(True)
                    PCAGraph.fig.canvas.draw_idle()
                    return
            if vis:
                PCAGraph.annot.set_visible(False)
                PCAGraph.fig.canvas.draw_idle()
            
    def update_annot(event):
        pos = {event.xdata, event.ydata}
        #closestx = np.unravel_index((np.abs(PCA.plotdata-[event.xdata, event.ydata]))
                                    #.argmin(), PCA.plotdata.shape)
        minx = 1000
        miny = 1000
        chosensample = 1
        for sample in range(1,len(PCA.plotdata)):
            if abs(PCA.plotdata[sample,0] - event.xdata) < minx and abs(PCA.plotdata[sample,1] - event.ydata) < miny:
                minx = abs(PCA.plotdata[sample,0] - event.xdata)
                miny = abs(PCA.plotdata[sample,1] - event.ydata)
                chosensample = sample
        PCAGraph.annot.xyann = (PCA.plotdata[chosensample, 0],
                                PCA.plotdata[chosensample, 1])
        samplenames = DataPreparation.DataPrep.FindRealSampleNames(
            UI_MainWindow.Ui_MainWindow, FileInput.BrowseWindow.currentDataset.index)
        if(len(samplenames) != len(set(samplenames))):
            # if there are duplicates in the Ui_MainWindow.filenames column like RTsegments
            # or per swath metrics
            sampleNameColumn1Combination = samplenames[chosensample] + "-" \
                + str(FileInput.BrowseWindow.currentDataset.iloc[chosensample, 1])
            text = sampleNameColumn1Combination.format(PCA.plotdata[chosensample, 0],
                                                       PCA.plotdata[chosensample, 1])
        else:
            text = samplenames[chosensample].format(
                PCA.plotdata[chosensample, 0],
                PCA.plotdata[chosensample, 1])
        PCAGraph.annot.set_text(text)
        PCAGraph.annot.update_positions(PCAGraph.fig)
    
    def retranslateUi2(self):
        _translate = QtCore.QCoreApplication.translate
        OutlierTab.outliercolorlabel1.setText("Possible outliers in blue")
        OutlierTab.outliercolorlabel2.setText("Probable outliers in red")
        OutlierTab.outliercolorlabel1.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
        OutlierTab.outliercolorlabel2.setFont(UI_MainWindow.Ui_MainWindow.boldfont)
        OutlierTab.outliercolorlabel1.setStyleSheet( "color : blue; ")
        OutlierTab.outliercolorlabel2.setStyleSheet( "color : red; ")
        
        OutlierTab.outlierlistLabel.setText(
            "Candidates for probable outliers: ")
        font = QtGui.QFont()
        font.setPointSize(18)
        if(len(UI_MainWindow.Ui_MainWindow.outlierlist) > 0):
            outlierstring = ""
            for element in UI_MainWindow.Ui_MainWindow.outlierlist:
                outlierstring = str(outlierstring) + "\n" + str(element)
        else:
            outlierstring = "No probable outliers found."
        OutlierTab.OutlierSamples.setText(outlierstring)
        OutlierTab.possoutlierlistLabel.setText(
            "Candidates for possible outliers: ")
        font = QtGui.QFont()
        font.setPointSize(18)
        if(len(PCA.PCA.possOutlierList) > 0):
            outlierstring = ""
            for element in PCA.PCA.possOutlierList:
                outlierstring = str(outlierstring) + "\n" + str(element)
        else:
            outlierstring = "No possible outliers found."
        OutlierTab.possOutlierSamples.setText(outlierstring)
        
        
    def zoom_fun(event):
        # get the current x and y limits
            cur_xlim = PCAGraph.ax.get_xlim()
            cur_ylim = PCAGraph.ax.get_ylim()
            cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
            cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location
            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1/1.5
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = 1.5
            else:
                # deal with something that should never happen
                scale_factor = 1
                print (event.button)
            # set new limits
            PCAGraph.ax.set_xlim([xdata - cur_xrange*scale_factor,
                        xdata + cur_xrange*scale_factor])
            PCAGraph.ax.set_ylim([ydata - cur_yrange*scale_factor,
                        ydata + cur_yrange*scale_factor])
            PCAGraph.annot.set_text("") 
            PCAGraph.annot =  PCAGraph.ax.annotate("", xy=(event.xdata ,event.ydata ),color='green')
            OutlierTab.LoadingsProgressBar.hide() 
            if hasattr(PCAGraph, "loadingsAnnot"):
                for ii in PCAGraph.loadingsTextAnnot:
                    xvalue = ii._x
                    yvalue = ii._y
                    if(xvalue < PCAGraph.ax.get_xlim()[0]):
                        ii.set_visible(False)
                    elif(xvalue > PCAGraph.ax.get_xlim()[1]):
                        ii.set_visible(False)
                    elif (yvalue<PCAGraph.ax.get_ylim()[0]):
                        ii.set_visible(False)
                    elif (yvalue > PCAGraph.ax.get_ylim()[1]):
                        ii.set_visible(False)
                    else:
                        ii.set_visible(True)
                        
            PCAGraph.fig.canvas.draw()
            
    def home(self):
        PCAGraph.ax.set_xlim(OutlierTab.original_xlim)
        PCAGraph.ax.set_ylim(OutlierTab.original_ylim)
        PCAGraph.fig.canvas.draw()
            
            