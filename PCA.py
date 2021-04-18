import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import globalVars
import math, sys
import statistics
from sklearn import decomposition as sd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, RobustScaler
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import matplotlib.pyplot as plt
import re
import MainParser
import Main
import numpy as np
import pandas as pd
import logging

class PCA(object):
    """description of class"""

    def CreatePCAGraph(data):
        robust_scaler = RobustScaler()
        np.nan_to_num(data)
        NormalisedData = robust_scaler.fit_transform(data)
        pca = sd.PCA()
        pca.fit_transform(NormalisedData)
        global loadings
        loadings = pca.components_
        varianceArray = pca.explained_variance_ratio_
        PCA.componentVariance = pca.explained_variance_ratio_
        temprange = range(1,(len(varianceArray)-1))
        maxDerivative = 0
        secondDerivative =[]
        Elbow = 2
        for element in temprange:
            vvv=abs(varianceArray[element])
            aaa=abs(varianceArray[element-1])
            sss=abs(varianceArray[element+1])
            fff =  abs(sss +aaa- 2 * vvv)
            secondDerivative.append (fff)
            if fff > maxDerivative:
               Elbow = element
               maxDerivative = max(maxDerivative,fff)
        globalVars.var.progress1.setValue(12)
        plotPCA = sd.PCA(n_components=2)
        global plotdata
        plotdata = plotPCA.fit_transform(NormalisedData)
        globalVars.var.pca = sd.PCA(n_components = Elbow)
        loadingspca = sd.PCA().fit(NormalisedData)
        globalVars.var.loadings = loadingspca.components_
        data = globalVars.var.pca.fit_transform(NormalisedData)
        globalVars.var.progress1.setValue(28)
        PCA.finalDf = pd.DataFrame(data)
        global Distances
        Distances = pd.DataFrame()
        plt.rcParams['axes.facecolor'] = 'lightgray'
        plt.rc('axes', axisbelow =True)
        plt.figure()
        plt.grid(color ="ghostwhite")
        lw = 2

    def calculateSampleToVariableRatio(self, data):
        ratio = len(data.iloc[:,0])/len(data.columns)
        return ratio
    
    def CalculateOutliers(self):
        sampleSize = range(len(globalVars.var.database.currentDataset.index))
        PCA.Distances = PCA.calculateDistanceMatrix(self, PCA.finalDf)
        globalVars.var.progress1.setValue(60)
        #self.metrics.index = self.metrics.iloc[:,0]
        medianDistances = PCA.createMedianDistances(self, sampleSize)
        outlierDistance = PCA.calculateOutLierDistances(self, medianDistances,3)
        globalVars.var.progress1.setValue(65)

        for iterator in sampleSize:
            medianDistances["MedianDistance"][iterator] = np.percentile(PCA.Distances[iterator], 50)
        possoutlierDistance = PCA.calculateOutLierDistances(self, medianDistances, 1.5)
        globalVars.var.progress1.setValue(65)
        medianDistances["outlier"]= medianDistances["MedianDistance"].apply(
        lambda x: x >= outlierDistance
        )
        logging.info("The following runs were identified as candidates for probable outliers based on their z-scores:")
        
        medianDistances["possoutlier"]= medianDistances["MedianDistance"].apply(
        lambda x: x >= possoutlierDistance and x < outlierDistance
        )
        logging.info("The following runs were identified as candidates for possible outliers based on their z-scores:")
        PCA.possibleOutliers = medianDistances[medianDistances["possoutlier"]]
        PCA.possOutlierList = PCA.possibleOutliers["Filename"]
        Outliers = medianDistances[medianDistances["outlier"]]
        return Outliers

    def createMedianDistances(self, sampleSize):
        medianDistances = pd.DataFrame()
        if globalVars.var.database.currentDataset.index[0] != 1:
            medianDistances["Filename"] = globalVars.var.database.currentDataset.index
        else:
            medianDistances["Filename"] = globalVars.var.database.currentDataset["Filename"]
        medianDistances["MedianDistance"] = 'default value'
        for iterator in sampleSize:
            medianDistances["MedianDistance"][iterator] = np.percentile(
                PCA.Distances[iterator], 50)
        return medianDistances

    def calculateOutLierDistances(self, medianDistances, integer):
        Q1 = np.percentile(medianDistances["MedianDistance"], 25)
        Q3 = np.percentile(medianDistances["MedianDistance"], 75)
        IQR = Q3 - Q1
        outlierDistance = Q3 + integer*IQR
        return outlierDistance


    def calculateDistanceMatrix(self, df):
        from sklearn.neighbors import DistanceMetric
        dist = DistanceMetric.get_metric('euclidean')
        PCA.Distances = pd.DataFrame(dist.pairwise(df.values),index=df.index, columns=df.index)
        return PCA.Distances


    


