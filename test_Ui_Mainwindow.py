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

# Default tests:
    def test_WindowTitle(self):
        #QTest.mouseClick(self.form.tab.browse, Qt.LeftButton)
        #self.assertEqual(self.form.tab, "Browse..")
        self.assertEqual(self.form.windowTitle(), "Assurance")

    def test_WindowMaximized(self):
        self.assertEqual(self.form.size(),QtCore.QSize(200, 100))

    def test_backgroundcolor(self):
        self.assertEqual(self.form.tab.styleSheet(), "background-color: gainsboro;")

    def test_filenameBackgroundcolor(self):
        self.assertEqual(self.form.filename.styleSheet(), "background-color: white;")

    def test_browsebuttonbackgroundcolor(self):
        self.assertEqual(self.form.tab.browse.styleSheet(), "background-color: rgb(240,240,240);")

    def test_outlierbuttonbackgroundcolor(self):
        self.assertEqual(self.form.tab.Outliers.styleSheet(), "background-color: rgb(240,240,240);")

    def test_indmetricsbuttonbackgroundcolor(self):
        self.assertEqual(self.form.tab.IndMetrics.styleSheet(), "background-color: rgb(240,240,240);")

    def test_longitudinalbuttonbackgroundcolor(self):
        self.assertEqual(self.form.tab.Longitudinal.styleSheet(), "background-color: rgb(240,240,240);")

    def test_filenameGeometry(self):
        self.assertEqual(self.form.filename.geometry(), QtCore.QRect(90, 120, 300, 20))

    def test_progressbar1Geometry(self):
        self.assertEqual(self.form.tab.progress1.geometry(), QtCore.QRect(200, 80, 250, 20))

    def test_progressbar2Geometry(self):
        self.assertEqual(self.form.tab.progress2.geometry(), QtCore.QRect(200, 80, 250, 20))

    def test_browsebtnHeight(self):
        self.assertEqual(self.form.tab.browse.height(), 30)
    
    def test_OutliersHeight(self):
        self.assertEqual(self.form.tab.Outliers.height(), 50)

    def test_OutliersWidth(self):
        self.assertEqual(self.form.tab.Outliers.width(), 150)

    def test_IndMetricsHeight(self):
        self.assertEqual(self.form.tab.IndMetrics.height(), 50)

    def test_IndMetricsWidth(self):
        self.assertEqual(self.form.tab.IndMetrics.width(), 150)

    def test_LongitudinalHeight(self):
        self.assertEqual(self.form.tab.Longitudinal.height(), 50)

    def test_LongitudinalWidth(self):
        self.assertEqual(self.form.tab.Longitudinal.width(), 150)

    def test_BrowseText(self):
        self.assertEqual(self.form.tab.browse.text(), "Browse..")

    def test_IndMetricsText(self):
        self.assertEqual(self.form.tab.IndMetrics.text(), "Individual metrics")

    def test_LongitudinalText(self):
        self.assertEqual(self.form.tab.Longitudinal.text(), "Longitudinal analysis")

    def test_Filename(self):
        self.assertEqual(self.form.filename.text(), "   File...                         ")


    def test_OutliersText(self):
        self.assertEqual(self.form.tab.Outliers.text(), "Detect Outliers")

    def test_uploadLabelText(self):
        self.assertEqual(self.form.tab.uploadLabel.text(), "Upload a file (Either json, csv or tsv format):")

    def test_chooseLabelText(self):
        self.assertEqual(self.form.tab.chooseLabel.text(), "Choose the analysis you would like to conduct:")

    def test_WindowResize( self ):
        self.form.resize( 123, 456 )
        size= QtCore.QSize( 123, 456 )
        self.assertEqual( self.form.size(), size )




if __name__ == '__main__':
    unittest.main()
