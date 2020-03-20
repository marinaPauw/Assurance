import sys
import UI_MainWindow
import pandas as pd
import xml.etree.ElementTree as ET
import re
import os


class pepXMLReader():
    def parsePepXML(self, files):
        
        table = pd.DataFrame(columns = ["Filename","IDCount","scoreLow","scoreMed","scoreHigh"])
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            openFile = open(file, "r")
            lines = openFile.readlines()
            peptideIDCount = 0
            scoreLow = 0
            scoreMed = 0
            scoreHigh = 0
            for line in lines:
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
            series = pd.Series([filename,peptideIDCount, scoreLow, scoreMed, scoreHigh])
            series.name = filename
            table.append(series)        
        return table