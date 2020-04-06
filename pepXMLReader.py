import sys
import UI_MainWindow
import pandas as pd
import numpy as np
import os
import re
import dateutil.parser
import time


class pepXMLReader():
    def parsePepXML(self, files):
        # First lets find the quantiles:
        startParseTime = time.perf_counter()
        filenames = []
        for file in files:
            filenames.append(os.path.splitext(os.path.basename(file))[0])
        
        pepTable = pd.DataFrame(index = filenames , columns = ["Filename","Number of Distinct peptides","Number of spectra identified"])
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            with open(file) as thisFile:
                #lines = thisFile.readlines()
                file = thisFile.read()
                allpeptides = re.findall('peptide=\"\w+\"', file)
                uniquepeptides = (list(set(allpeptides))) 
                pepTable.loc[filename] =  [filename, len(uniquepeptides), len(allpeptides)]
        print("Parsing took " + str(time.perf_counter()-startParseTime) + "seconds.")
        return pepTable    
                
         