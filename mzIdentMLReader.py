import sys
import UI_MainWindow
import pandas as pd
import numpy as np
import os
import re
import dateutil.parser
import time


class mzIdentMLReader():
    def parsemzID(self, files):
        # First lets find the quantiles:
        startParseTime = time.perf_counter()
        filenames = []
        for file in files:
            filenames.append(os.path.splitext(os.path.basename(file))[0])
        
        pepTable = pd.DataFrame(index = filenames , columns = ["Filename","Number of distinct peptides","Number of spectra identified"])
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            with open(file) as thisFile:
                #lines = thisFile.readlines()
                file = thisFile.read()
                allpeptides = re.findall('Peptide id=', file)
                spectrumIDs = re.findall("<SpectrumIdentificationResult", file)
                pepTable.loc[filename] =  [filename, len(allpeptides), len(spectrumIDs)]
        print("Parsing took " + str(time.perf_counter()-startParseTime) + "seconds.")
        return pepTable    
                
         