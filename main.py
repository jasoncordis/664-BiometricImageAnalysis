from skimage import io
from matplotlib import pyplot as plt
from skimage.filters import threshold_mean

import numpy as np
from scipy import ndimage as ndi
from skimage.util import random_noise
from skimage import feature

image = io.imread('/664/664-BiometricImageAnalysis/images/frames_grey/0001.png')

#Threshold
thresh = threshold_mean(image)
binary = image > thresh

fig, axes = plt.subplots(ncols=2, figsize=(8, 3))
output = axes.ravel()

output[0].imshow(image, cmap=plt.cm.gray)
output[0].set_title('Original image')

output[1].imshow(binary, cmap=plt.cm.gray)
output[1].set_title('Result')

plt.show()

#Edge detection
edges = feature.canny(image)
io.imshow(edges)
io.show()
