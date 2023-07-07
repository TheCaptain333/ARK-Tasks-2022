import cv2 as cv
import numpy as np
from projection_matrices import p_left,p_right
method = cv.TM_SQDIFF_NORMED


bike_image = cv.imread('bike.png')
left_image = cv.imread('left.png')
right_image = cv.imread('right.png')

resultL = cv.matchTemplate(bike_image, left_image, method)
resultR = cv.matchTemplate(bike_image, right_image, method)


mnL,_,mnLocL,_ = cv.minMaxLoc(resultL)
mnR,_,mnLocR,_ = cv.minMaxLoc(resultR)


MPxL,MPyL = mnLocL
MPxR,MPyR = mnLocR


trows,tcols = bike_image.shape[:2]

xL,yL = MPxL+tcols/2,MPyL+trows/2
xR,yR = MPxR+tcols/2,MPyR+trows/2


height,width = left_image.shape[:2]

uL,vL = yL,width-xL
uR,vR = yR,width-xR

imgL = np.array([[uL],[vL],[1]])
imgR = np.array([[uR],[vR],[1]])

p_left_3x3 = p_left[0:3,0:3]
p_right_3x3 = p_right[0:3,0:3]

p_left_column = p_left[0:3,3]
p_right_column = p_right[0:3,3]

final_mat = np.subtract(np.matmul(np.linalg.inv(p_left_3x3),p_left_column),np.matmul(np.linalg.inv(p_left_3x3),p_right_column))


coeff_left= np.matmul(np.linalg.inv(p_left_3x3),imgL)
coeff_right= np.matmul(np.linalg.inv(p_right_3x3),imgR)

ml = coeff_left[0][0]
nl = coeff_left[1][0]
mr = coeff_right[0][0]
nr = coeff_right[1][0]




coeff_mat = np.array([[ml,-mr,0],[nl,-nr,0],[0,0,1]])



solution = np.linalg.solve(coeff_mat,final_mat)

Z_left = solution[0]
Z_right = solution[1]

print('Distance from left camera is %0.3f metres' % Z_left)
print('Distance from right camera is %0.3f metres'% Z_right)
