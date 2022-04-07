import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('C:/zebraFish/frames_grey/0001.png',0)

# img = cv.bilateralFilter(img,9,75,75)
# img = cv.medianBlur(img,3)

img = cv.GaussianBlur(img,(5,5),0)

i1 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,13,20)
i2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 13, 20)

cv.imshow('og', img)
cv.imshow('adap', i1)
cv.imshow('gaus', i2)
cv.waitKey(0)

# img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# ret, thresh1 = cv.threshold(img, 120, 255, cv.THRESH_BINARY + 
#                                             cv.THRESH_OTSU)
# cv.imshow('Otsu Threshold', thresh1) 
# cv.waitKey(0)                                            