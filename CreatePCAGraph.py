import sys
from PyQt5 import QtCore, QtGui, QtWidgets
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
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import re
import MainParser
import numpy as np
import pandas as pd
from Main import Main
import globalVars

class PCAGraphCreation():
    def CreatePCAGraph(NumericMetrics):
        # Now test for variance and remove anything with low variance. (run \
        # numpy.var() on each column))
        np.set_printoptions(suppress=True)
        threshold = 0.01
        for iii in NumericMetrics:
            print(NumericMetrics[iii].var())
            if (NumericMetrics[iii].var() < threshold):
                NumericMetrics = NumericMetrics.drop(iii, axis=1)

        print("Low variance columns removed. There are now", \
              len(NumericMetrics.columns), "columns")
        # Need to figure ut how many dimensions are needed:
        # NormalisedData = preprocessing.scale(NumericMetrics)
        robust_scaler = RobustScaler()
        NormalisedData = robust_scaler.fit_transform(NumericMetrics)
        pca = sd.PCA(n_components=len(NumericMetrics.columns))
        pca.fit_transform(NormalisedData)
        global loadings
        loadings = pca.components_
        varianceArray = pca.explained_variance_ratio_
        temprange = range(1, (len(varianceArray) - 1))
        maxDerivative = 0
        secondDerivative = []
        global Elbow
        for element in temprange:
            vvv = varianceArray[element]
            aaa = varianceArray[element - 1]
            sss = varianceArray[element + 1]
            fff = sss + aaa - 2 * vvv
            secondDerivative.append(fff)
            if fff > maxDerivative:
                Elbow = element
                maxDerivative = max(maxDerivative, fff)
        Main.tab.progress1.setValue(12)
        plotPCA = sd.PCA(n_components=2)
        global plotdata
        plotdata = plotPCA.fit_transform(NormalisedData)
        Main.pca = sd.PCA(n_components=Elbow)
        loadingspca = sd.PCA().fit(NormalisedData)
        Main.loadings = loadingspca.components_
        data = Main.pca.fit_transform(NormalisedData)
        Main.tab.progress1.setValue(28)
        finalDf = pd.DataFrame(data)
        Distances = pd.DataFrame()
        plt.rcParams['axes.facecolor'] = 'lightgray'
        plt.rc('axes', axisbelow=True)
        plt.figure()
        plt.grid(color="ghostwhite")
        lw = 2
