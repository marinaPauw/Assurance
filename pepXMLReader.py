import sys
import UI_MainWindow
import pandas as pd
import numpy as np
import os
import re
import dateutil.parser


class pepXMLReader():
    def parsePepXML(self, files):
        # First lets find the quantiles:
        filenames = []
        for file in files:
            filenames.append(os.path.splitext(os.path.basename(file))[0])
        
        pepTable = pd.DataFrame(index = filenames , columns = ["Filename","Dates","Number of Distinct peptides","Number of spectra identified"])
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            with open(file) as thisFile:
                lines = thisFile.readlines()
            spectrumCount = 0
            uniquepeptides = list()
            for line in lines:
                if "date" in line:
                    tempDate = re.search('date="(.+?)"', line)
                    if isinstance(tempDate, re.Match):
                        tempDate = tempDate.group(1)
                        date = dateutil.parser.parse(tempDate)
                if "search_hit" in line:
                    spectrumCount = spectrumCount+1
                    m = re.search('peptide="(.+?)"', line)
                    if m not in uniquepeptides:
                        uniquepeptides.append(m)
                        
            pepTable.loc[filename] =  [filename,date, len(uniquepeptides), spectrumCount]
        return pepTable