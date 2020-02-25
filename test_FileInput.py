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
import UI_MainWindow
import DataPreparation
import FileInput
import pandas as pd
import json
import numpy as np
import unittest

class Test_test_FileInput(unittest.TestCase):
    def setUp(self):
        UI_MainWindow.Ui_MainWindow.metrics = FileInput.BrowseWindow.filetypeCheck("HeunisMetrics.tsv")
        UI_MainWindow.Ui_MainWindow.tab = QtWidgets.QWidget()
        UI_MainWindow.Ui_MainWindow.tab.browse = QtWidgets.QPushButton(UI_MainWindow.Ui_MainWindow.tab)
        UI_MainWindow.Ui_MainWindow.tab.Outliers = QtWidgets.QPushButton(UI_MainWindow.Ui_MainWindow.tab)
        UI_MainWindow.Ui_MainWindow.tab.Longitudinal = QtWidgets.QPushButton(UI_MainWindow.Ui_MainWindow.tab)
        UI_MainWindow.Ui_MainWindow.tab.IndMetrics = QtWidgets.QPushButton(UI_MainWindow.Ui_MainWindow.tab)
        UI_MainWindow.Ui_MainWindow.filename = QtWidgets.QLabel(UI_MainWindow.Ui_MainWindow.tab)
        column1 = list(range(1,40))
        self.TrainingSet = pd.DataFrame()
        self.TrainingSet = pd.DataFrame(columns=['A','B','C','D','E'], index=range(1, 6))
    
    def test_FileTypeCheck(self):
        self.assertTrue(len(UI_MainWindow.Ui_MainWindow.metrics.columns)==51)
    
    def test_TrainingSetWarning(self):
        #UI_MainWindow.Ui_MainWindow.metrics = UI_MainWindow.Ui_MainWindow.metrics
        self.assertWarns(UserWarning, FileInput.BrowseWindow.TrainingSetFileMatchNames(UI_MainWindow.Ui_MainWindow, self.TrainingSet))

 
if __name__ == '__main__':
    unittest.main()
