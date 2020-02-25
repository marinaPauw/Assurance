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
from sklearn.ensemble import RandomForestClassifier
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import FileInput
import UI_MainWindow
import re
import pandas as pd
import numpy as np
import unittest
import RandomForest

app = QtWidgets.QApplication(sys.argv)

class Test_RandomForest(unittest.TestCase):
    def setUp(self):
        UI_MainWindow.Ui_MainWindow.goodpredictionList = list(range(1,120))
        UI_MainWindow.Ui_MainWindow.badpredictionList = list(range(1,120))
        UI_MainWindow.Ui_MainWindow.tab = QtWidgets.QWidget()
        UI_MainWindow.Ui_MainWindow.TrainingSet = QtWidgets.QWidget()
        UI_MainWindow.Ui_MainWindow.TrainingSet.goodbtn = QtWidgets.QPushButton(
            'This is my selection for desired quality.',
            UI_MainWindow.Ui_MainWindow.TrainingSet)
        UI_MainWindow.Ui_MainWindow.TrainingSet.goodbtn.setEnabled(False)
        UI_MainWindow.Ui_MainWindow.TrainingSet.badbtn = QtWidgets.QPushButton(
            'This is my selection for suboptimal quality.',
            UI_MainWindow.Ui_MainWindow.TrainingSet)
        UI_MainWindow.Ui_MainWindow.TrainingSet.badbtn.setEnabled(False)
    
    
    def test_GoodAndBadAreSame_goodCleared(self):
        RandomForest.RandomForest.GoodAndBadAreSame(self)
        self.assertTrue(UI_MainWindow.Ui_MainWindow.goodpredictionList==[])

    def test_GoodAndBadAreSame_badCleared(self):
        RandomForest.RandomForest.GoodAndBadAreSame(self)
        self.assertTrue(UI_MainWindow.Ui_MainWindow.badpredictionList==[])

if __name__ == '__main__':
    unittest.main()
