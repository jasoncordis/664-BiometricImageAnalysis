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
ax = axes.ravel()

ax[0].imshow(image, cmap=plt.cm.gray)
ax[0].set_title('Original image')

ax[1].imshow(binary, cmap=plt.cm.gray)
ax[1].set_title('Result')

for a in ax:
    a.axis('off')

plt.show()

#Edge detection
edges = feature.canny(image)
io.imshow(edges)
io.show()
