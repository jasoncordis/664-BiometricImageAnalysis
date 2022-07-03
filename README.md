# 664-BiometricImageAnalysis

# How it works:
This is a Python application that is designed to analyze greyscale and binary images of zebrafish and locate the heads of each fish in the image. 

For greyscale images, minimum thresholding is used in order to locate specific parts of fish bodies. For binary images, edge detection is used in order to find fish shapes, then the geometry of each fish is determined by finding how each part of the fish expands while moving left to right on the X-axis. 

In order to make the most accurate program possible, an overlap function was also designed to locate abnormal fish bodies that could represent more than one fish overlapping, and fish orientation patterns were also added to determine the direction of a specific fish. 

# Required libraries: 
CV2
skimage
matplotlib
pandas
numpy
