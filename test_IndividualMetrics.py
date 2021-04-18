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
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets  import RectangleSelector
import matplotlib.pyplot as plt
import numpy as np
import datetime
import Main
import re
import Legend
import pylab
from matplotlib.colors import hsv_to_rgb
from cycler import cycler
import unittest
import IndividualMetrics

class Test_test_IndividualMetrics(unittest.TestCase):
   def test_uniqueList(self):
       listA = [0,0,3,4,5,2,2] 
       uniqueList = [0,3,4,5,2]
       self.assertTrue(uniqueList==IndividualMetrics.MyIndMetricsCanvas.unique(listA))

if __name__ == '__main__':
    unittest.main()
