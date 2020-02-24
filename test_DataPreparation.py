import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
import sys
import statistics
import scipy
from sklearn import decomposition as sd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, RobustScaler
from matplotlib.figure import Figure
import datetime
import matplotlib.pyplot as plt
import re
import FileInput
import UI_MainWindow
import DataPreparation
import numpy as np
import pandas as pd
import unittest

#app = QtWidgets.QApplication(sys.argv)

class Test_test_DataPreparation(unittest.TestCase):
    def setUp(self):
        df = pd.read_csv("HeunisMetrics.tsv", sep="\t")
        UI_MainWindow.Ui_MainWindow.NumericMetrics = pd.DataFrame()
        DataPreparation.DataPrep.ExtractNumericColumns(df)
    
    def test_ExtractNumericColumns(self):
        self.assertTrue(len(UI_MainWindow.Ui_MainWindow.NumericMetrics.columns)==44)

    def test_removeLowVarianceColumns(self):
         DataPreparation.DataPrep.RemoveLowVarianceColumns(self)
         self.assertTrue(len(UI_MainWindow.Ui_MainWindow.NumericMetrics.columns)==25)

    def test_FindRealSampleNames(self):
        rawSampleNames = ["abc.mzML","def.wiff.scan","ghi.wiff.scan.mzML"]
        realSampleNames = DataPreparation.DataPrep.FindRealSampleNames(self, rawSampleNames)
        truth = ["abc","def","ghi"]
        self.assertTrue(realSampleNames == truth )


if __name__ == '__main__':
    unittest.main()