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
    def  __init__(self, model):
        global fig
        fig, ax = plt.subplots()
        variables = model._model_json['output']['variable_importances']['variable']
        y_pos = np.arange(len(variables))
        scaled_importance = model._model_json['output']['variable_importances']['scaled_importance']
        ax.barh(y_pos, scaled_importance, align='center', color='green', ecolor='black')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(variables)
        ax.invert_yaxis()
        ax.set_xlabel('Scaled Importance')
        ax.set_title('Variable Importance')
        FigureCanvas.__init__(self, fig)
        #self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        fig.suptitle("Feature importance", fontsize=10)
        self.compute_initial_figure()
        annot = ax.annotate("", xy=(0,0.5),color='green') 
   
    def compute_initial_figure(self):
        pass
    
         

        
        
        
        
        
        
        
        
        
        