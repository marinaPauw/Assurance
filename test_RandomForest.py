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
import MainParser
import Main
import re
import pandas as pd
import numpy as np
import unittest
import RandomForest

app = QtWidgets.QApplication(sys.argv)

class Test_RandomForest(unittest.TestCase):
    def setUp(self):
        globalVars.var.goodpredictionList = list(range(1,120))
        globalVars.var.badpredictionList = list(range(1,120))
        globalVars.var.tab = QtWidgets.QWidget()
        globalVars.var.TrainingSet = QtWidgets.QWidget()
        globalVars.var.TrainingSet.goodbtn = QtWidgets.QPushButton(
            'This is my selection for desired quality.',
            globalVars.var.TrainingSet)
        globalVars.var.TrainingSet.goodbtn.setEnabled(False)
        globalVars.var.TrainingSet.badbtn = QtWidgets.QPushButton(
            'This is my selection for suboptimal quality.',
            globalVars.var.TrainingSet)
        globalVars.var.TrainingSet.badbtn.setEnabled(False)
    
    
    def test_GoodAndBadAreSame_goodCleared(self):
        RandomForest.RandomForest.GoodAndBadAreSame(self)
        self.assertTrue(globalVars.var.goodpredictionList==[])

    def test_GoodAndBadAreSame_badCleared(self):
        RandomForest.RandomForest.GoodAndBadAreSame(self)
        self.assertTrue(globalVars.var.badpredictionList==[])

if __name__ == '__main__':
    unittest.main()
