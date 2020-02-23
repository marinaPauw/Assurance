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
        self.assertEqual(self.form.filename.text(), "   File...                  ")

    def test_OutliersText(self):
        self.assertEqual(self.form.tab.Outliers.text(), "Detect Outliers")

    def test_uploadLabelText(self):
        self.assertEqual(self.form.tab.uploadLabel.text(), "Upload a file (Either json, csv or tsv format):")

    def test_chooseLabelText(self):
        self.assertEqual(self.form.tab.chooseLabel.text(), "Choose the analysis you would like to conduct:")

    def test_WindowResize(self):
        self.form.resize( 123, 456 )
        size= QtCore.QSize( 123, 456 )
        self.assertEqual( self.form.size(), size )

    # OnBrowseWindowClicked
    def test_checkColumnLengthIfZeroColumns(self):
        self.form.metrics =  pd.DataFrame()
        self.assertWarns(UserWarning,self.form.checkColumnLength())

    # OnOutliersClicked
    def test_columnNumberWarningPCA(self):
        self.form.NumericMetrics =  pd.DataFrame()
        self.assertWarns(UserWarning,self.form.checkColumnNumberForPCA())

    def test_sampleNumberWarningPCA(self):
        self.form.NumericMetrics =  pd.DataFrame()
        self.assertWarns(UserWarning,self.form.checkSampleNumberForPCA())

    def test_sampleToVariableRatio(self):
        self.form.NumericMetrics =  pd.DataFrame()
        self.assertWarns(UserWarning,self.form.checkSampleToVariableRatio(2))

    def test_checkDistanceMatrix(self):
        data = {'value': [ -1.5782318, 1.90400151, -1.81750642, 0.16169671, -0.33636381, 1.88726218, 0.05906165, 0.74575076, 1.32281861, 2.16232488, -1.5342326, -0.29875492, -1.48367378, 0.35191864, 1.96858044,-0.95574512,-0.34930498, -1.0991727, -1.18002339, -0.5556985, -1.41459932, -1.40732026, -1.56738256, -0.90322458,-0.37358033, -0.9736953, -1.67412173, -2.28602132, -2.06741367, -1.41252314, -1.41252314, -1.49970674, -0.30788613, -1.48076975, -0.69621721, 1.34853459, -0.52092122, -0.04453575, -2.01587483, -0.82084765, 0.44273151,-0.91224416, -1.70016427, -1.39520053, -1.8886795, -0.73921581,  -1.66219618, -0.62098067, -1.15633166, -2.04133381, -1.44192053, -0.68263054, -0.73860028, -0.51559758, -0.94644425,-1.30494586, -1.37858754, -0.55526666, -1.26819588, -0.82732795, -1.07834843, -0.38353757, -0.8224644, -0.5762343,  -1.32856322, -0.36393072, -1.20274224, -0.96379291, -0.82368902, -0.86193168, -1.25451409, -0.27777407, -1.04876475, 0.35784166,-1.01387693,  -0.83732026,  -1.51793134, -1.17290017, -0.93440878, -0.66697985, -2.04647118, -1.17899809, -1.2939738, -1.16545727, 0.21506909, -1.54675355, -2.04513628, -0.81476999, -1.05326142, -0.70638496, -1.59719904, 0.54792821, -1.16611598, -1.23292066, -1.23056123, -0.90373257, -1.47841192, 0.47558229, 2.01593569, 0.80569118, -1.38865928, 42.70932779, -1.2619267, -0.64376147, 1.44060502, -1.84809345, -1.43296069, -0.82440381, 1.96932841, 40.75041503, -1.86306501, -0.33340733, -1.84011651, -0.43796638, -0.30589803, -0.7732938, -0.21468299, -0.00267918, 0.58719699, -0.12983957]
                }
        df = pd.DataFrame (data, columns = ['value'])
        firstrow = [0.0,3.48223331,0.23927462,1.73992851,1.24186799,3.4654939799999998,1.63729345,2.32398256,2.90105041,3.74055668,0.043999200000000016,1.27947688,0.09455802000000002,1.93015044,3.54681224,0.62248668,1.2289268199999999,0.47905909999999996,0.39820841000000007,1.0225333,0.16363247999999997,0.17091153999999986,0.010849239999999982,0.6750072199999999,1.20465147,0.6045364999999999,0.09588993000000001,0.7077895200000002,0.48918187000000013,0.16570865999999995,0.16570865999999995,0.07852506000000004,1.27034567,0.09746204999999986,0.8820145899999999,2.92676639,1.05731058,1.5336960499999999,0.43764303000000004,0.7573841499999999,2.02096331,0.66598764,0.12193246999999996,0.18303126999999986,0.3104477000000001,0.8390159899999999,0.08396438000000006,0.95725113,0.42190014,0.46310200999999984,0.13631126999999998,0.89560126,0.83963152,1.06263422,0.63178755,0.27328594000000006,0.1996442599999999,1.02296514,0.31003592,0.7509038499999999,0.49988337000000005,1.19469423,0.7557674,1.0019974999999999,0.24966858000000003,1.21430108,0.3754895599999999,0.61443889,0.75454278,0.71630012,0.32371770999999994,1.30045773,0.52946705,1.93607346,0.5643548700000001,0.7409115399999999,0.06030045999999989,0.40533163000000005,0.6438230199999999,0.9112519499999999,0.4682393800000002,0.39923370999999985,0.2842579999999999,0.41277452999999986,1.79330089,0.03147824999999993,0.46690447999999996,0.7634618099999999,0.5249703800000001,0.87184684,0.018967240000000052,2.12616001,0.4121158199999999,0.34531113999999996,0.34767057,0.67449923,0.09981987999999986,2.05381409,3.5941674900000002,2.38392298,0.18957252000000002,44.28755959,0.3163050999999999,0.93447033,3.0188368199999998,0.26986164999999995,0.14527110999999993,0.75382799,3.54756021,42.32864683,0.28483320999999995,1.24482447,0.26188471000000013,1.14026542,1.27233377,0.8049379999999999,1.36354881,1.57555262,2.16542879,1.44839223]
        dist = self.form.calculateDistanceMatrix(df)
        self.assertTrue((firstrow == dist.iloc[:,0]).all())

    def test_calculateOutLierDistances(self):
        
        medianDistances = pd.DataFrame( list(range(1,120)), columns = ["MedianDistance"])
        mD = self.form.calculateOutLierDistances( medianDistances)
        mylist = list(range(1,120))
        self.assertEqual(mD,178)

if __name__ == '__main__':
    unittest.main()
