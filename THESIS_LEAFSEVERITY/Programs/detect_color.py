"""
OpenCV read colored image as BGR.
OpenCV displays colored image as RGB.

In summary, a three channel image composed of A,B,C,
CBA is displayed as ABC.

That means BGR is displayed as RGB.
L*a*b* is displayed as b*a*L*
HSV is displayed as VSH

Values converted are correct using the function cvtColor().
The only thing to look out is it displays it in reverse channel order.

Taken note because its different when using MATLAB when I use image processing.
"""

import cv2
import numpy as np

# Extract ROI using image segmentation.
img=cv2.imread("leaf_sample1.jpg")
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blurred=cv2.GaussianBlur(gray,(5,5),0)
ret,otsuThres=cv2.threshold(blurred,0,
                            255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
otsuThres=cv2.bitwise_not(otsuThres)
maskedLeaf=cv2.bitwise_and(img,img,mask=otsuThres)

totalArea=cv2.countNonZero(otsuThres)

cv2.imshow("ROI",maskedLeaf)

# Define color to detect, the yellowish part of the leaf
# using HSV colorspace


hsv=cv2.cvtColor(maskedLeaf,cv2.COLOR_BGR2HSV)
cv2.imshow("HSV",hsv)
greenPart=cv2.inRange(hsv,(30, 100, 100), (70, 255, 255) )
cv2.imshow("Green Part",greenPart)
greenPart=cv2.inRange(hsv,(0, 100, 100), (30, 255, 255) )
cv2.imshow("Yellow Part",greenPart)

cv2.waitKey(0)
cv2.destroyAllWindows()
