# Assurance
Statistical analysis tool for "Shotgun" and SWATH quality metrics

This windows-only standalone desktop application can be used to run QuaMeter/ SwaMe on mzML files or .tsv/.json files from previous runs can be uploaded. 

The files can then be analyzed in any of three ways:
Outlier detection with PCA
Graph of each metric separately
Analysis of longitudinal data via random forest with h2o package

Requirements: 
The h2o package requires Java, preferrably jdk 8, no later version than 12. 
If you do not plan to run random forest, Java is not required. You may also be asked by your computer to give permission when Java starts running.
https://www.oracle.com/java/technologies/javase-jdk8-downloads.html 

##For developers:

A requirements.txt file exists to ease the installation of packages. 
Run the following from your virtual environment/root project directory:

pip install requirements.txt

##To publish the exe from source code:
Install pyinstaller.

Run the following from within the directory containing the source code:

pyinstaller Assurance.py -D --hidden-import="sklearn.utils._cython_blas" --hidden-import="sklearn.neighbors.typedefs" --hidden-import="sklearn.neighbors.quad_tree" --hidden-import="sklearn.tree._utils"  --add-data="C:\Users\newMarina\AppData\Local\Programs\Python\Python37\Lib\site-packages\sklearn\.libs\vcomp140.dll;." --windowed -i assurance.ico -F