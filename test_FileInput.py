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
        self.inputFile = pd.read_csv("HeunisMetrics.tsv", sep="\t")
    
    def test_FileTypeCheck(self):
        metrics = FileInput.BrowseWindow.filetypeCheck("HeunisMetrics.tsv")
        self.assertTrue(len(metrics.columns)==51)

if __name__ == '__main__':
    unittest.main()
