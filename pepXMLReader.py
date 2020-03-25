import sys
import UI_MainWindow
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import re
import os
import dateutil.parser


class pepXMLReader():
    def parsePepXML(self, files):
        # First lets find the quantiles:
        
        AllHyperscores = list()
        for file in files:
            openFile = open(file, "r")
            lines = openFile.readlines()
            for line in lines:
                if "hyperscore" in line:
                        m = float(re.search('value="(.+?)"', line).group(1))
                        AllHyperscores.append(m)
        Q3 = np.quantile(AllHyperscores, .75)
        Q1 = np.quantile(AllHyperscores, .25)
        
        
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            openFile = open(file, "r")
            lines = openFile.readlines()
            peptideIDCount = 0
            scoreLow = 0
            scoreMed = 0
            scoreHigh = 0
            for line in lines:
                if "date" in line:
                    tempDate = re.search('date="(.+?)"', line)
                    if isinstance(tempDate, re.Match):
                        tempDate = tempDate.group(1)
                        date = dateutil.parser.parse(tempDate)
                if "search_hit" in line:
                    peptideIDCount = peptideIDCount +1
                if "hyperscore" in line:
                    m = float(re.search('value="(.+?)"', line).group(1))
                    if m> Q3:
                        scoreHigh = scoreHigh+1
                    elif m< Q1:
                        scoreLow = scoreLow +1
                    else:
                        scoreMed = scoreMed +1
            series = pd.Series()
            series.name = filename
            UI_MainWindow.Ui_MainWindow.TrainingSetTable =  UI_MainWindow.Ui_MainWindow.TrainingSetTable.append(series)
            UI_MainWindow.Ui_MainWindow.TrainingSetTable.loc[filename] = [filename,date, peptideIDCount, scoreLow, scoreMed, scoreHigh] 
            a=10