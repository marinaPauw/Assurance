import sys
from fpdf import FPDF
import os
import UI_MainWindow
import IndividualMetrics
from PyQt5 import QtWidgets, QtCore
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfFileMerger
import glob
import PCAGraph
import RandomForest
import FeatureImportancePlot

class OutputWriter(object):
    def producePDF(self, now ):
        QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 3))
        if "AssuranceReport" not in os.getcwd():
            dirName = str(now) +"_AssuranceReport"
            dirName = dirName.replace(" ", "_")
            dirName = dirName.replace(":", "-")
            OutputWriter.createDir(self,dirName)
            OutputWriter.changeDir(self,dirName)
        else:
            dirName = str(now) +"_AssuranceReport"
            dirName = dirName.replace(" ", "_")
            dirName = dirName.replace(":", "-")
        pdf = FPDF()  
        #-----------------------Cover page-------------------------
        pdf.add_page(orientation='P')
        pdf.set_font('helvetica', 'B',size=12)
        pdf.cell(200, 12, txt="Assurance Results", ln=1, align="C")
        pdf.set_font('helvetica', size=10)
        reportDate = "Date Assurance analysis started: " + str(now)
        pdf.cell(200, 10, txt=reportDate, ln=1, align="L")
        pdf.cell(200, 10, txt="Files analysed: ", ln=1, align="L")
        pdf.set_text_color(105,105,105)
        if "Filename" in UI_MainWindow.Ui_MainWindow.metrics[0].columns:
            currentcolumn = 0  
            for filename in UI_MainWindow.Ui_MainWindow.metrics[0]['Filename']:
                          
                if len(filename)>20:
                    if currentcolumn >0:
                        pdf.ln()
                    pdf.cell(200, 10, txt=str(filename), ln=1, align="C")
                    currentcolumn =0
                else:
                    if currentcolumn>4:
                        pdf.ln()
                        pdf.cell(50, 10, txt=str(filename), ln=0, align="C")
                        currentcolumn = 1
                    else:
                        pdf.cell(50, 10, txt=str(filename), ln=0, align="C")
                        currentcolumn = currentcolumn+1    
        
        elif "Dataset" in UI_MainWindow.Ui_MainWindow.metrics[0].columns:
            currentcolumn = 0  
            for filename in UI_MainWindow.Ui_MainWindow.metrics[0]['Dataset']:
                          
                if len(filename)>20:
                    if currentcolumn >0:
                        pdf.ln()
                    pdf.cell(200, 10, txt=str(filename), ln=1, align="C")
                    currentcolumn =0
                else:
                    if currentcolumn>4:
                        pdf.ln()
                        pdf.cell(50, 10, txt=str(filename), ln=0, align="C")
                        currentcolumn = 1
                    else:
                        pdf.cell(50, 10, txt=str(filename), ln=0, align="C")
                        currentcolumn = currentcolumn+1    
            
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, txt='Assurance version: v1.0.0', ln=1, align="L")
        QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 15))
        #---------------------------PCA-----------------------------
        if UI_MainWindow.Ui_MainWindow.outliersDetected:
            pdf.add_page(orientation='P')
            #Heading:
            pdf.set_font('helvetica', size=10)
            pdf.cell(200, 10, txt="Outlier detection with PCA", ln=1, align="C")
            
            #Outliers:
            if len(UI_MainWindow.Ui_MainWindow.firstOutlierlist)>0:
                pdf.cell(200, 10, txt="The following samples were identified as probable outliers:", ln=1, align="C")
                for element in UI_MainWindow.Ui_MainWindow.firstOutlierlist:
                    pdf.cell(50, 10, txt=str(element), ln=1, align="L")
            elif len(UI_MainWindow.Ui_MainWindow.firstOutlierlist)==0:
               pdf.cell(200, 10, txt="No samples were identified as probable outliers:", ln=1, align="C")
            if len(UI_MainWindow.Ui_MainWindow.firstpossOutlierlist)>0:
                pdf.cell(200, 10, txt="The following samples were identified as possible outliers:", ln=1, align="C")
                for element in UI_MainWindow.Ui_MainWindow.firstpossOutlierlist:
                    pdf.cell(50, 10, txt=str(element), ln=1, align="L")
            elif len(UI_MainWindow.Ui_MainWindow.firstpossOutlierlist)==0:
               pdf.cell(200, 10, txt="No samples were identified as possible outliers:", ln=1, align="C")
            
                 
            #Create images:
            if not os.path.exists("outlierDetection1.png"):
                PCAGraph.PCAGraph.printForReport(self, now)
                        
            image_path = os.path.join(os.getcwd(),"outlierDetection1.png")
            pdf.image(image_path, w=200)
            QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 20))
            
            image_path = os.path.join(os.getcwd(),"outlierDetection2.png")
            pdf.image(image_path, w=200)
            if os.path.exists("outlierDetectionAfterReanlysis1.png"):
                    pdf.add_page(orientation='P')
                    #Outliers:
                    if len(UI_MainWindow.Ui_MainWindow.secondOutlierlist)>0:
                        pdf.cell(200, 10, txt="The following samples were identified as probable outliers in the reanalysis:", ln=1, align="C")
                        for element in UI_MainWindow.Ui_MainWindow.secondOutlierlist:
                            pdf.cell(50, 10, txt=str(element), ln=1, align="L")
                    elif len(UI_MainWindow.Ui_MainWindow.secondOutlierlist)==0:
                        pdf.cell(200, 10, txt="No samples were identified as probable outliers in the reanalysis:", ln=1, align="C")
                    if len(UI_MainWindow.Ui_MainWindow.secondpossOutlierlist)>0:
                        pdf.cell(200, 10, txt="The following samples were identified as possible outliers in the reanalysis:", ln=1, align="C")
                        for element in UI_MainWindow.Ui_MainWindow.secondpossOutlierlist:
                            pdf.cell(50, 10, txt=str(element), ln=1, align="L")
                    elif len(UI_MainWindow.Ui_MainWindow.secondpossOutlierlist)==0:
                        pdf.cell(200, 10, txt="No samples were identified as possible outliers in the reanalysis:", ln=1, align="C")
                        
                    image_path = os.path.join(os.getcwd(),"outlierDetectionAfterReanlysis1.png")
                    pdf.image(image_path, w=200)
            if os.path.exists("outlierDetectionAfterReanlysis2.png"):
                    image_path = os.path.join(os.getcwd(),"outlierDetectionAfterReanlysis2.png")
                    pdf.image(image_path, w=200)
            
            QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 30))
            try:
                if UI_MainWindow.Ui_MainWindow.RandomForestPerformed == False and UI_MainWindow.Ui_MainWindow.indMetricsGraphed == True:
                    pdfName = "00AssuranceReport.pdf"
                    pdf.output(pdfName) 
                elif UI_MainWindow.Ui_MainWindow.RandomForestPerformed == False and UI_MainWindow.Ui_MainWindow.indMetricsGraphed == False:
                    pdfName = "AssuranceReport.pdf"
                    pdf.output(pdfName) 
            except:
                pdfName = dirName + ".pdf"
                    
        else:
            if UI_MainWindow.Ui_MainWindow.RandomForestPerformed == False and UI_MainWindow.Ui_MainWindow.indMetricsGraphed == True:
                pdfName = "00AssuranceReport.pdf"
                pdf.output(pdfName) 
            
        QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 33))
        
            
        
            
        #---------------------------Random Forest----------------------
            
        if(UI_MainWindow.Ui_MainWindow.RandomForestPerformed):
            pdf.add_page(orientation='P')
            #Heading:
            pdf.set_font('helvetica', size=16)
            pdf.cell(200, 10, txt="Supervised classification with Random Forest", ln=1, align="C")
            pdf.set_font('helvetica', size=10)
            pdf.cell(200, 10, txt="The training set consisted of the following samples:", ln=1, align="C")
            
            #Find the names of training samples:
            trainingSampleNames = []
            for element in RandomForest.RandomForest.train[RandomForest.RandomForest.train.columns[0]]:
                for item in range(0,len(UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0])):
                    if element == UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0][UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].columns[0]].iloc[item]:
                        match = UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0][UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].columns[0]].iloc[item]
                        if match not in trainingSampleNames:
                            trainingSampleNames.append(match)
                
            QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 36))
            testSampleNames = []
            for element in RandomForest.RandomForest.test[RandomForest.RandomForest.test.columns[0]]:
                for item in range(0,len(UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0])):
                    if element == UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0][UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].columns[0]].iloc[item]:
                        match = UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0][UI_MainWindow.Ui_MainWindow.Numerictrainingmetrics[0].columns[0]].iloc[item]
                        if match not in testSampleNames:
                            testSampleNames.append(match)
            
            QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 40))
            pdf.set_text_color(105,105,105)
            currentcolumn = 0  
            for filename in trainingSampleNames:
                          
                if len(filename)>20:
                    if currentcolumn >0:
                        pdf.ln()
                    pdf.cell(200, 10, txt=str(filename), ln=1, align="C")
                    currentcolumn =0
                else:
                    if currentcolumn>4:
                        pdf.ln()
                        pdf.cell(50, 10, txt=str(filename), ln=0, align="C")
                        currentcolumn = 1
                    else:
                        pdf.cell(50, 10, txt=str(filename), ln=0, align="C")
                        currentcolumn = currentcolumn+1    
            
            pdf.set_text_color(0, 0, 0)
            pdf.ln()
            pdf.cell(200, 10, txt="The test set consisted of the following samples:", ln=1, align="C")
            QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 44))
            pdf.set_text_color(105,105,105)
            currentcolumn = 0  
            for filename in testSampleNames:
                          
                if len(filename)>20:
                    if currentcolumn >0:
                        pdf.ln()
                    pdf.cell(200, 10, txt=str(filename), ln=1, align="C")
                    currentcolumn =0
                else:
                    if currentcolumn>4:
                        pdf.ln()
                        pdf.cell(50, 10, txt=str(filename), ln=0, align="C")
                        currentcolumn = 1
                    else:
                        pdf.cell(50, 10, txt=str(filename), ln=0, align="C")
                        currentcolumn = currentcolumn+1    
            pdf.set_text_color(0, 0, 0)
            pdf.ln()
            pdf.set_font('helvetica','B', size=14)
            pdf.cell(200, 10, txt="Performance metrics:", ln=1, align="C")
            pdf.set_font('helvetica', size=10)
            pdf.cell(50, 10, txt="F1:", ln=0, align="C")
            pdf.set_text_color(105,105,105)
            pdf.cell(50, 10, txt=str(round(RandomForest.RandomForest.performance.F1()[0][1],4)), ln=0, align="C")
            pdf.set_text_color(0, 0, 0)
            pdf.cell(50, 10, txt="Accuracy:", ln=0, align="C")
            pdf.set_text_color(105,105,105)
            pdf.cell(50, 10, txt=str(round(RandomForest.RandomForest.performance.accuracy()[0][1],4)), ln=0, align="C")
            pdf.set_text_color(0, 0, 0)
            pdf.cell(50, 10, txt="MCC:", ln=0, align="C")
            pdf.set_text_color(105,105,105)
            pdf.cell(50, 10, txt=str(round(RandomForest.RandomForest.performance.mcc()[0][1],4)), ln=1, align="C")
            pdf.set_text_color(0, 0, 0)
            pdf.cell(50, 10, txt="logloss:", ln=0, align="C")
            pdf.set_text_color(105,105,105)
            pdf.cell(50, 10, txt=str(round(RandomForest.RandomForest.performance._metric_json["logloss"],4)), ln=0, align="C")
            pdf.set_text_color(0, 0, 0)
            pdf.ln()
            
            pdf.cell(200, 10, txt="The following samples were predicted by Random Forest to resemble the group labelled 'bad' quality:", ln=1, align="C")
            
            for filename in UI_MainWindow.Ui_MainWindow.badlist:
                          
                if len(filename)>20:
                    if currentcolumn >0:
                        pdf.ln()
                    pdf.cell(200, 10, txt=str(filename), ln=1, align="C")
                    currentcolumn =0
                else:
                    if currentcolumn>4:
                        pdf.ln()
                        pdf.cell(50, 10, txt=str(filename), ln=0, align="C")
                        currentcolumn = 1
                    else:
                        pdf.cell(50, 10, txt=str(filename), ln=0, align="C")
                        currentcolumn = currentcolumn+1            
                    
            QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 50))
                    
            #Print Graphs:
            FeatureImportancePlot.FeaturePlot.printForReport(self)
            RandomForest.RandomForest.printForReport(self)
            pdf.ln()
            #Read in Graphs:
            image_path = os.path.join(os.getcwd(),"RFPlot.png")
            pdf.image(image_path, w=200)
            QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 55))
            pdf.ln()
            image_path = os.path.join(os.getcwd(),"FIPlot.png")
            pdf.image(image_path, w=200)         
            QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 63))     
           
            try:
                if UI_MainWindow.Ui_MainWindow.indMetricsGraphed == True:
                    pdfName = "00AssuranceReport.pdf"
                    pdf.output(pdfName) 
                elif UI_MainWindow.Ui_MainWindow.indMetricsGraphed == False:
                    pdfName = "AssuranceReport.pdf"
                    pdf.output(pdfName) 
            except:
                pdfName = dirName + ".pdf"
            QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 66))
                  

        #---------------------------Individual metrics----------------
                            
        if(UI_MainWindow.Ui_MainWindow.indMetricsGraphed):
            OutputWriter.saveGraphPDFs(self)
            #import all the pdfs:
            paths = glob.glob('*.pdf')
            paths.sort()
            OutputWriter.merger('AssuranceReport.pdf', paths)
            
        OutputWriter.deleteExtraFiles(self, dirName)
        QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 100))

        
    
    def merger(output_path, input_paths):
        pdf_merger = PdfFileMerger()
        file_handles = []
    
        for path in input_paths:
            pdf_merger.append(path)
        
        with open(output_path, 'wb') as fileobj:
            pdf_merger.write(fileobj)
        pdf_merger.close()
    
        
    def saveGraphPDFs(self):
            #Here we run through all the metrics to produce grphs for the pdf
        progressCounter2 = 0
        
        for metric in UI_MainWindow.Ui_MainWindow.listOfMetrics:
            for dataset in range(len(UI_MainWindow.Ui_MainWindow.metrics)):
                if UI_MainWindow.Ui_MainWindow.element in UI_MainWindow.Ui_MainWindow.metrics[dataset].columns:
                    whichds = dataset
                    break
            graph = IndividualMetrics.MyIndMetricsCanvas(UI_MainWindow.Ui_MainWindow.metrics[whichds],
                            UI_MainWindow.Ui_MainWindow.metrics[whichds], metric, True)
            
            del graph
            progressCounter2= progressCounter2+(30/len(UI_MainWindow.Ui_MainWindow.listOfMetrics))
            QtCore.QMetaObject.invokeMethod(UI_MainWindow.Ui_MainWindow.pdf.progress, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, 66+progressCounter2))
            
    def createDir(self, dirName):
        
        try:
            # Create target Directory
            os.mkdir(dirName)
        except:
                logging.info("Directory creation " , dirName ,  " failed") 
                
    def changeDir(self, dirName):
        try:
            # Change to target Directory
            os.chdir(dirName)
        except:
            logging.info("Directory couldn't be changed to " , dirName) 
            
    def deleteExtraFiles(self,dirName):
        try:
            if dirName in os.getcwd():
                pdfs = glob.glob("*.pdf")
                for f in pdfs:
                    if f != "AssuranceReport.pdf":
                        os.remove(f)
                        
                pngs = glob.glob("*.png")
                for f in pngs:
                    os.remove(f)
        except:
            logging.info("Could not delete extra pdfs..")
    