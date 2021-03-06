import sys
import UI_MainWindow
from PyQt5 import QtCore
import pandas as pd
import numpy as np
import os
import re
import dateutil.parser
import time
import logging


class pepXMLReader():
    def parsePepXML(self, files):
        # First lets find the quantiles:
        startParseTime = time.perf_counter()
        filenames = []
        for file in files:
            filenames.append(os.path.splitext(os.path.basename(file))[0])
        QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.progress1, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 30))
        pepTable = pd.DataFrame(index = filenames , columns = ["Filename","Number of distinct peptides","Number of spectra identified"])
        count = 0
        for file in files:
            parts = 60/len(files)
            total = 30+count*parts
            QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.progress1, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, total))
            count=count+1
            filename = os.path.splitext(os.path.basename(file))[0]
            with open(file) as thisFile:
                #lines = thisFile.readlines()
                file = thisFile.read()
                allpeptides = re.findall('peptide=\"\w+\"', file)
                uniquepeptides = (list(set(allpeptides))) 
                pepTable.loc[filename] =  [filename, len(uniquepeptides), len(allpeptides)]
        logging.info("Parsing took " + str(time.perf_counter()-startParseTime) + "seconds.")
        QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.progress1, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 90))
        return pepTable    
                
         