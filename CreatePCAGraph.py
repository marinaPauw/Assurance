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
import FileInput
import numpy as np
import pandas as pd

class PCAGraphCreation():
    def CreatePCAGraph(NumericMetrics):
    #Now test for variance and remove anything with low variance. (run numpy.var() on each column))
        np.set_printoptions(suppress=True)
        NumericMetrics = Ui_MainWindow.NumericMetrics
        var = NumericMetrics.var()
        threshold = 0.01
        for iii in NumericMetrics:
            print (NumericMetrics[iii].var())
            if (NumericMetrics[iii].var()<threshold):
                NumericMetrics = NumericMetrics.drop(iii, axis=1)
        
        print("Low variance columns removed. There are now", len(NumericMetrics.columns) ,"columns")
        ################Need to figure ut how many dimensions are needed:
        #NormalisedData = preprocessing.scale(NumericMetrics)
        robust_scaler = RobustScaler()
        NormalisedData = robust_scaler.fit_transform(NumericMetrics)
        pca = sd.PCA(n_components=len(NumericMetrics.columns))
        pca.fit_transform(NormalisedData)
        global loadings
        loadings = pca.components_
        varianceArray = pca.explained_variance_ratio_
        temprange = range(1,(len(varianceArray)-1))
        maxDerivative = 0
        secondDerivative =[]
        global Elbow
        for element in temprange:
            vvv=varianceArray[element]
            aaa=varianceArray[element-1]
            sss=varianceArray[element+1]
            fff =  sss +aaa- 2 * vvv
            secondDerivative.append (fff)
            if fff > maxDerivative:
               Elbow = element
               maxDerivative = max(maxDerivative,fff)
        Ui_MainWindow.tab.progress1.setValue(12)
        plotPCA = sd.PCA(n_components=2)
        global plotdata
        plotdata = plotPCA.fit_transform(NormalisedData)
        Ui_MainWindow.pca = sd.PCA(n_components = Elbow)
        loadingspca = sd.PCA().fit(NormalisedData)
        Ui_MainWindow.loadings = loadingspca.components_
        data = Ui_MainWindow.pca.fit_transform(NormalisedData)
        Ui_MainWindow.tab.progress1.setValue(28)
        finalDf = pd.DataFrame(data)
        Distances = pd.DataFrame()
        plt.rcParams['axes.facecolor'] = 'lightgray'
        plt.rc('axes', axisbelow =True)
        plt.figure()
        plt.grid(color ="ghostwhite")
        lw = 2

    #def CreatePCAGraph(NumericMetrics):
    #Now test for variance and remove anything with low variance. (run numpy.var() on each column))
     #   np.set_printoptions(suppress=True)
     #   NumericMetrics = Ui_MainWindow.NumericMetrics
     #   var = NumericMetrics.var()
     #   threshold = 0.01
     #   for iii in NumericMetrics:
     #       print (NumericMetrics[iii].var())
     #       if (NumericMetrics[iii].var()<threshold):
      #          NumericMetrics = NumericMetrics.drop(iii, axis=1)
        
    #    print("Low variance columns removed. There are now", len(NumericMetrics.columns) ,"columns")
    #    ################Need to figure ut how many dimensions are needed:
        #NormalisedData = preprocessing.scale(NumericMetrics)
   #     robust_scaler = RobustScaler()
   #     NormalisedData = robust_scaler.fit_transform(NumericMetrics)
   #     pca = sd.PCA(n_components=len(NumericMetrics.columns))
   #     pca.fit_transform(NormalisedData)
   #     global loadings
   #     loadings = pca.components_
   #     varianceArray = pca.explained_variance_ratio_
   #     temprange = range(1,(len(varianceArray)-1))
   #     maxDerivative = 0
   #     secondDerivative =[]
   #     global Elbow
    #    for element in temprange:
   #         vvv=varianceArray[element]
  #          aaa=varianceArray[element-1]
  #          sss=varianceArray[element+1]
     #       fff =  sss +aaa- 2 * vvv
   #         secondDerivative.append (fff)
   #         if fff > maxDerivative:
   #            Elbow = element
   #            maxDerivative = max(maxDerivative,fff)
   #     Ui_MainWindow.tab.progress1.setValue(12)
   #     plotPCA = sd.PCA(n_components=2)
   #     PCAGraph.PCAGraph.plotdata = plotPCA.fit_transform(NormalisedData)
    #    Ui_MainWindow.pca = sd.PCA(n_components = Elbow)
     #   loadingspca = sd.PCA().fit(NormalisedData)
      #  Ui_MainWindow.loadings = loadingspca.components_
       # data = Ui_MainWindow.pca.fit_transform(NormalisedData)
# #       Ui_MainWindow.tab.progress1.setValue(28)
   #     global finalDf
  #      finalDf = pd.DataFrame(data)
   #     global Distances
    #    Distances = pd.DataFrame()
     #   #plt.rcParams['axes.facecolor'] = 'lightgray'
      #  #plt.rc('axes', axisbelow =True)
       # #plt.figure()
        #plt.grid(color ="ghostwhite")
    #    lw = 2
        
