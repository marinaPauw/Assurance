
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
import sys
import statistics
import json
import pandas as pd
import numpy as np
import numbers
import math
import matplotlib.pyplot as plt
import statistics
import scipy
from sklearn import decomposition as sd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import re
import UI_MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    global MainWindow
    MainWindow = UI_MainWindow.Ui_MainWindow()
    MainWindow.setupUi()
    MainWindow.show()
    sys.exit(app.exec_())
          