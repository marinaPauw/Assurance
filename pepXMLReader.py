import sys
import UI_MainWindow
import pandas as pd
import xml.etree.ElementTree as ET
import re
import os
import dateutil.parser


class pepXMLReader():
    def parsePepXML(self, files):
        
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
                    if m > 50:
                        scoreHigh= scoreHigh+1
                    elif m < 50 and m>15:
                        scoreMed= scoreMed+1
                    else:
                        scoreLow = scoreLow +1
            series = pd.Series()
            series.name = filename
            UI_MainWindow.Ui_MainWindow.TrainingSetTable =  UI_MainWindow.Ui_MainWindow.TrainingSetTable.append(series)
            UI_MainWindow.Ui_MainWindow.TrainingSetTable.loc[filename] = [filename,date, peptideIDCount, scoreLow, scoreMed, scoreHigh] 
            a=10