import unittest
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtTest import QTest
import Assurance
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
import matplotlib.pyplot as plt
import re
import FileInput
import IndividualMetrics
import PCA
import PCAGraph
import DataPreparation
import RandomForest
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix

app = QtWidgets.QApplication(sys.argv)

class Test_test_Ui_Mainwindow(unittest.TestCase):
    global MainWindow

    def setUp(self):
        self.form = Assurance.UI_MainWindow.Ui_MainWindow()
        self.form.setupUi()

    def test_WindowTitle(self):
        #QTest.mouseClick(self.form.tab.browse, Qt.LeftButton)
        #self.assertEqual(self.form.tab, "Browse..")
        self.assertEqual(self.form.windowTitle(), "Assurance")

    def test_WindowMaximized(self):
        self.assertEqual(self.form.size(),QtCore.QSize(200, 100))

    def test_backgroundcolor(self):
        self.assertEqual(self.form.tab.styleSheet(), "background-color: gainsboro;")

    def test_browsebuttonbackgroundcolor(self):
        self.assertEqual(self.form.tab.browse.styleSheet(), "background-color: rgb(240,240,240);")

    def test_outlierbuttonbackgroundcolor(self):
        self.assertEqual(self.form.tab.Outliers.styleSheet(), "background-color: rgb(240,240,240);")

    def test_indmetricsbuttonbackgroundcolor(self):
        self.assertEqual(self.form.tab.IndMetrics.styleSheet(), "background-color: rgb(240,240,240);")

    def test_longitudinalbuttonbackgroundcolor(self):
        self.assertEqual(self.form.tab.Longitudinal.styleSheet(), "background-color: rgb(240,240,240);")



if __name__ == '__main__':
    unittest.main()
