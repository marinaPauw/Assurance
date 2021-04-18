import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math, sys
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
import Main
from Datasets import Datasets
import MainParser
import pandas as pd
import json
import numpy as np
import unittest

class Test_test_MainParser(unittest.TestCase):
    def setUp(self):
        Datasets.metrics = "HeunisMetrics.tsv"
        globalVars.var.tab = QtWidgets.QWidget()
        globalVars.var.tab.browse = QtWidgets.QPushButton(globalVars.var.tab)
        globalVars.var.tab.Outliers = QtWidgets.QPushButton(globalVars.var.tab)
        globalVars.var.tab.Longitudinal = QtWidgets.QPushButton(globalVars.var.tab)
        globalVars.var.tab.IndMetrics = QtWidgets.QPushButton(globalVars.var.tab)
        globalVars.var.filename = QtWidgets.QLabel(globalVars.var.tab)
        column1 = list(range(1,40))
        self.TrainingSet = pd.DataFrame()
        self.TrainingSet = pd.DataFrame(columns=['A','B','C','D','E'], index=range(1, 6))
    
    def test_FileTypeCheck(self):
        self.assertTrue(len(Datasets.metrics.columns)==51)
    
    def test_TrainingSetWarning(self):
        #Datasets.metrics = Datasets.metrics
        self.assertWarns(UserWarning, MainParser.Parser.TrainingSetFileMatchNames(globalVars.var, self.TrainingSet))

 
if __name__ == '__main__':
    unittest.main()
