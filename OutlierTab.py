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
import PCA

class OutlierTab(QtWidgets.QTabWidget):

    def createTabWidget(self,now):
                # --------------------------------------Widgets-------------------------------------------
                        OutlierTab.PCA = QtWidgets.QTabWidget()
                        OutlierTab.PCA.plotlabel = QtWidgets.QLabel(OutlierTab.PCA)
                        #OutlierTab.PCA.plotlabel.setGeometry(10, 500, 1000, 300)
                        OutlierTab.PCA.PCAplot = PCAGraph.PCAGraph(now)
                        

                        OutlierTab.outlierlistLabel = QtWidgets.QLabel(OutlierTab.PCA)
                        OutlierTab.OutlierSamples = QtWidgets.QLabel(OutlierTab.PCA)
                        OutlierTab.OutlierSamples.setAlignment(QtCore.Qt.AlignLeft)

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
                        OutlierTab.PCA.Redolabel.setText("Redo analysis without the outliers:")
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
                        vbox3.addWidget(OutlierTab.outlierlistLabel)
                        vbox3.addWidget(OutlierTab.OutlierSamples)
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
                        hboxPlot = QtWidgets.QHBoxLayout(OutlierTab.PCA)
                        hboxPlot.addStretch()

                        hboxPlot.addWidget(OutlierTab.PCA.plotlabel)
                        hboxPlot.addStretch()
                        vbox2.addLayout(hboxPlot)
                        vbox2.setAlignment(QtCore.Qt.AlignCenter)
                        hbox.setAlignment(QtCore.Qt.AlignCenter)
                        vbox2.addLayout(hbox)
                        hbox2 = QtWidgets.QHBoxLayout(OutlierTab.PCA)

                        hbox.addWidget(OutlierTab.PCA.PCAplot)
                        
                        hbox2.setAlignment(QtCore.Qt.AlignCenter)
                        vbox2.addLayout(hbox2)
                        OutlierTab.retranslateUi2(OutlierTab.PCA)
                        UI_MainWindow.Ui_MainWindow.EnableAnalysisButtons(self)
                        UI_MainWindow.Ui_MainWindow.progress1.setValue(100)
                        PCAGraph.fig.canvas.mpl_connect("motion_notify_event",
                                                        OutlierTab.onhover)
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
        closestx = np.unravel_index((np.abs(PCA.plotdata - event.xdata))
                                    .argmin(), PCA.plotdata.shape)
        PCAGraph.annot.xyann = (PCA.plotdata[closestx[0], 0],
                                PCA.plotdata[closestx[0], 1])
        samplenames = DataPreparation.DataPrep.FindRealSampleNames(
            UI_MainWindow.Ui_MainWindow, FileInput.BrowseWindow.currentDataset.index)
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
        
    
    def retranslateUi2(self):
        _translate = QtCore.QCoreApplication.translate
        array = range(1, len(UI_MainWindow.Ui_MainWindow.outlierlist), 1)
        OutlierTab.outlierlistLabel.setText(
            "Suggested outlier candidates: ")
        OutlierTab.PCA.plotlabel.setText(
            "Principal components analysis of quality metrics for outlier detection:")
        font = QtGui.QFont()
        font.setPointSize(18)
        if(len(UI_MainWindow.Ui_MainWindow.outlierlist) > 0):
            outlierstring = UI_MainWindow.Ui_MainWindow.outlierlist.array[0]
            for element in array:
                outlierstring = str(outlierstring) + "\n" + str(UI_MainWindow.Ui_MainWindow.outlierlist.array[element])
        else:
            outlierstring = "No outliers found."
        OutlierTab.OutlierSamples.setText(outlierstring)