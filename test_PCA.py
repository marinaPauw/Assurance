import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
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
import PCA
import DataPreparation
import UI_MainWindow
import numpy as np
import pandas as pd
import csv  
import unittest

class Test_test_PCA(unittest.TestCase):
    def setUp(self):
        df = pd.read_csv("HeunisMetrics.tsv", sep="\t")
        UI_MainWindow.Ui_MainWindow.tab = QtWidgets.QWidget()
        UI_MainWindow.Ui_MainWindow.tab.progress1 = QtWidgets.QProgressBar()
        UI_MainWindow.Ui_MainWindow.NumericMetrics = pd.DataFrame()
        DataPreparation.DataPrep.ExtractNumericColumns(df)
        DataPreparation.DataPrep.RemoveLowVarianceColumns(self)
    
    def test_PCA(self):
        PCA.PCA.CreatePCAGraph(UI_MainWindow.Ui_MainWindow.NumericMetrics)
        firstrow = [-1.578231801283509,1.9040015062664672,-1.8175064198266075,
                    0.16169670606889447,-0.3363638058408478,1.8872621821584656,
                    0.059061651781777434,0.7457507623774591,1.3228186066630903,
                    2.162324880515581,-1.5342325956468008,-0.2987549222116121,
                    -1.4836737760868668,0.35191863849891103,1.9685804404831508,
                    -0.9557451240603125,-0.3493049754439657,-1.0991727045761255,
                    -1.1800233942779004,-0.5556985009347002,-1.414599322495535,
                    -1.407320262584575,-1.5673825595701956,-0.9032245794433764,
                    -0.37358033384209266,-0.9736953004318237,-1.6741217251931673,
                    -2.2860213224343293,-2.0674136736343987,-1.412523144605541,
                    -1.4997067385162588,-0.30788613174672746,-1.4807697542000406,
                    -0.6962172094898303,1.348534590662446,-0.5209212168650847,
                    -0.04453574759659762,-2.0158748289839163,-0.8208476514759921,
                    0.4427315064634844,-0.9122441577107651,-1.700164270783764,
                    -1.3952005347685845,-1.8886795047088119,-0.7392158142462759,
                    -1.662196181282707,-0.6209806670653565,-1.156331655599752,
                    -2.041333808771028,-1.4419205302434563,-0.6826305422497763,
                    -0.7386002804578936,-0.5155975837276421,-0.9464442469147416,
                    0.09221718934774402,-1.304945857729269,-1.37858753504684,
                    -0.5552666598607982,-1.2681958846280073,-0.8273279509698896,
                    -1.0783484332095796,-0.3835375672669962,-0.8224644013109242,
                    -0.5762342980731037,-1.3285632227865796,-0.36393072430609363,
                    -1.2027422365068203,-0.9637929132916251,-0.8236890222832632,
                    -0.8619316829031212,-1.2545140908697656,-0.2777740652857362,
                    -1.0487647547733618,0.35784166108436044,-1.013876930453179,
                    -0.837320259989632,-1.517931339451632,-1.1729001678769317,
                    -0.9344087780921367,-0.666979847426771,-2.046471179244041,
                    -1.1789980889975775,-1.293973799701411,-1.1654572729009756,
                    0.21506909262085663,-1.5467535526287286,-2.0451362787461,
                    -0.8147699875295382,-1.053261418140565,-0.7063849583847857,
                    -1.597199040317161,0.5479282080783776,-1.1661159780998978,
                    -1.2329206594259623,-1.230561229324071,-0.9037325666907015,
                    -1.4784119182948423,0.47558229323726275,2.0159356866476164,
                    0.8056911831578542,-1.3886592778039741,42.709327790060605,
                    -1.2619266950039774,-0.64376146633965,1.4406050195838773,
                    -1.848093447732155,-1.432960686115704,-0.8244038102020488,
                    1.969328413209656,40.75041503328723,-1.8630650129659925,
                    -0.33340732854644944,-1.840116506005107,-0.4379663785527183,
                    -0.30589803027120405,-0.7732937988172596,-0.21468298863546303,
                    -0.002679181306057446,0.5871969898715845,-0.12983956918128578]

        with open('C:\\Users\\pauwmarina\\Desktop\\myfiletemp.tsv', 'wt') as out_file:
            tsv_writer = csv.writer(out_file)
            tsv_writer.writerow(PCA.finalDf.iloc[:,0])
        self.assertTrue((PCA.finalDf.iloc[:,0] == firstrow).all() )

if __name__ == '__main__':
    unittest.main()
