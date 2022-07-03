# 664-BiometricImageAnalysis

#How it works:
This is a Python application that is designed to analyze greyscale and binary images of zebrafish and locate the heads of each fish in the image. For greyscale images, minimum thresholding is used in order to locate specific parts of fish bodies. For binary images, edge detection is used in order to find fish shapes, then the geometry of each fish is determined by finding how each part of the fish expands while moving left to right on an X-axis. 

# Required libraries: 
CV2
skimage
matplotlib
pandas
numpy
