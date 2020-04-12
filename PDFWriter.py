import sys
from fpdf import FPDF
import os
import UI_MainWindow

class OutputWriter(object):
    def producePDF(self, now, ):
        pdf = FPDF()
        pdf.add_page()
        
        #Heading:
        pdf.set_font('helvetica', size=12)
        pdf.cell(200, 10, txt="Assurance results", ln=1, align="C")
        
        #---------------------------PCA---------------------------
        if(UI_MainWindow.Ui_MainWindow.PCA.PCAplot):
            pdf.set_font('helvetica', size=10)
            pdf.cell(200, 10, txt="Outlier detection with PCA", ln=1, align="C")
                        
            image_path = os.path.join(os.getcwd(),"outlierDetection.png")
            pdf.image(image_path, w=200, dpi = 1000)
            pdf.ln(0.15)
        
        #-----------Output---------------------------------
        
        pdfName = "AssuranceOutput.pdf"
        pdf.output(pdfName) 