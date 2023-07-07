import cv2 as cv
from matplotlib import pyplot as plt

imgL = cv.imread('left.png',0)
imgR = cv.imread('right.png',0)

stereo = cv.StereoBM_create(numDisparities=0,blockSize=21)


depth_map=stereo.compute(imgL,imgR)

plt.imshow(depth_map)
plt.axis('on')
plt.show()

