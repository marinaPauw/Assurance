import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math, sys
import statistics
import json
import pandas as pd
import numpy as np  
import numbers
import math
import matplotlib.pyplot as plt
import statistics
import scipy
from sklearn import decomposition as sd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, RobustScaler
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import re
import UI_MainWindow
from PyQt5.QtWidgets import QMessageBox


class Legend():
    """description of class"""
    def setupUI(self, lgd,parent=None):
                
        #Setting up the tab:
        self.legend = QtWidgets.QWidget()
        self.legend.setWindowTitle("Legend")
        self.legend.vbox = QtWidgets.QVBoxLayout(self.legend)
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch()
        hbox1.addWidget(lgd)
             
        hbox1.addStretch()
        self.legend.vbox.addLayout(hbox1)
        self.legend.show()
