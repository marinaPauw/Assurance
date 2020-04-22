import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import RandomForest
import pandas as pd
import numpy as np
import UI_MainWindow
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets

class FeaturePlot(FigureCanvas):
    def  __init__(self, model,width=25, height=40, dpi=100):
        global fig
        fig, ax = plt.subplots()
        variables = model._model_json['output']['variable_importances']['variable']
        y_pos = np.arange(len(variables))
        scaled_importance = model._model_json['output']['variable_importances']['scaled_importance']
        ax.barh(y_pos, scaled_importance, align='center', color='green', ecolor='black')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(variables)
        ax.tick_params(axis="y", labelsize=7)
        ax.invert_yaxis()
        ax.set_xlabel('Scaled Importance')
        ax.set_title('Metric Contribution')
        FigureCanvas.__init__(self, fig)
        #self.setParent(parent)
        fig.subplots_adjust(left = 0.2)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.compute_initial_figure()
   
    def compute_initial_figure(self):
        pass
    
    def printForReport(self):
        fig.savefig("FIPlot.png", dpi = 500)
    
         

        
        
        
        
        
        
        
        
        
        