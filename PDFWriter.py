import sys
from fpdf import FPDF
import os
import UI_MainWindow
import IndividualMetrics
from PyQt5 import QtWidgets
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfFileMerger
import glob

class OutputWriter(object):
    def producePDF(self, now, ):
        pdf = FPDF()  
        #-----------------------Cover page-------------------------
        pdf.add_page(orientation='P')
        pdf.set_font('helvetica', size=12)
        pdf.cell(200, 12, txt="Assurance results", ln=1, align="C")
        #pdf.set_font('helvetica', size=10)
        #reportDate = "Date Assurance analysis started: " + str(now)
        #pdf.cell(200, 10, txt=reportDate, ln=1, align="C")
        #pdf.cell(200, 10, txt="Files analysed: ", ln=1, align="C")
        #if "Filename" in UI_MainWindow.Ui_MainWindow.NumericMetrics[0].columns:
        #    for filename in UI_MainWindow.Ui_MainWindow.NumericMetrics[0]['Filename']:
        #        pdf.cell(200, 10, txt=str(filename), ln=1, align="C")
        #pdf.cell(200, 10, txt='Assurance version: Development', ln=1, align="C")
              
        #---------------------------PCA-----------------------------
        if UI_MainWindow.Ui_MainWindow.outliersDetected:
            
            #Heading:
            pdf.set_font('helvetica', size=10)
            pdf.cell(200, 10, txt="Outlier detection with PCA", ln=1, align="C")
                        
            image_path = os.path.join(os.getcwd(),"outlierDetection.png")
            pdf.image(image_path, w=200)
            pdf.ln(0.15)
            if UI_MainWindow.Ui_MainWindow.RandomForestPerformed == False:
                pdfName = "AssuranceReport.pdf"
                pdf.output(pdfName) 
        UI_MainWindow.Ui_MainWindow.pdf.progress.setValue(33)
        
        #-----------Output---------------------------------
        #We have to output before we get to individual metrics, so we can join the pdfs
        
        
        
            
        #---------------------------Individual metrics----------------
            
        if(UI_MainWindow.Ui_MainWindow.indMetricsGraphed):
            OutputWriter.saveGraphPDFs(self)
            UI_MainWindow.Ui_MainWindow.pdf.progress.setValue(55)
            #import all the pdfs:
            paths = glob.glob('*.pdf')
            paths.sort()
            OutputWriter.merger('AssuranceReport.pdf', paths)
            
            
            
            #for metric in UI_MainWindow.Ui_MainWindow.listOfMetrics:            
            #    if first == False:
            #      pdf.add_page(orientation="L")
            #    if metric == "StartTimeStamp":
            #        metric = "runDate"
            #    picturename = str(metric)+".png"
            #    image_path = os.path.join(os.getcwd(), picturename)
            #    try:
            #        pdf.image(image_path, w=300)
                    
            #    except:
            #        QtWidgets.QMessageBox.warning(self, "Warning:", image_path + " could not be added to the report.")
            #    first = False
            #    progressCounter= progressCounter+(10/len(UI_MainWindow.Ui_MainWindow.listOfMetrics))
            #    UI_MainWindow.Ui_MainWindow.pdf.progress.setValue(55+progressCounter)
        UI_MainWindow.Ui_MainWindow.pdf.progress.setValue(100)

        
    
    def merger(output_path, input_paths):
        pdf_merger = PdfFileMerger()
        file_handles = []
    
        for path in input_paths:
            pdf_merger.append(path)
        
        with open(output_path, 'wb') as fileobj:
            pdf_merger.write(fileobj)
    
        
    def saveGraphPDFs(self):
            #Here we run through all the metrics to produce grphs for the pdf
        progressCounter2 = 0
        
        for metric in UI_MainWindow.Ui_MainWindow.listOfMetrics:
            for dataset in range(len(UI_MainWindow.Ui_MainWindow.metrics)):
                if UI_MainWindow.Ui_MainWindow.element in UI_MainWindow.Ui_MainWindow.metrics[dataset].columns:
                    whichds = dataset
                    break
            graph = IndividualMetrics.MyIndMetricsCanvas(UI_MainWindow.Ui_MainWindow.metrics[whichds],
                            UI_MainWindow.Ui_MainWindow.metrics[whichds], metric)
            #image_path = os.path.join(os.getcwd(), metric +".pdf")
            #with PdfPages(image_path) as export_pdf:
            #    export_pdf.savefig()
            
            del graph
            progressCounter2= progressCounter2+(10/len(UI_MainWindow.Ui_MainWindow.listOfMetrics))
            UI_MainWindow.Ui_MainWindow.pdf.progress.setValue(33+progressCounter2)