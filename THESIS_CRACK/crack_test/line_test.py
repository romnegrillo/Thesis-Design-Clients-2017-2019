# -*- coding: utf-8 -*-
import sys
import time
import cv2
import numpy as np
import os

Kernel_size = 15
low_threshold = 40
high_threshold = 120

rho = 10
threshold = 15
theta = np.pi/180
minLineLength = 10
maxLineGap = 1


frame = cv2.imread("crack_test.jpeg")

# Convert to Grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# Blur image to reduce noise. if Kernel_size is bigger the image will be more blurry
blurred = cv2.GaussianBlur(gray, (Kernel_size, Kernel_size), 0)

# Perform canny edge-detection.
# If a pixel gradient is higher than high_threshold is considered as an edge.
# if a pixel gradient is lower than low_threshold is is rejected , it is not an edge.
# Bigger high_threshold values will provoque to find less edges.
# Canny recommended ratio upper:lower  between 2:1 or 3:1
edged = cv2.Canny(blurred, low_threshold, high_threshold)
# Perform hough lines probalistic transform

lines = cv2.HoughLinesP(edged, rho=rho, theta=theta, threshold=threshold,
                        minLineLength=minLineLength, maxLineGap=maxLineGap)
# Draw cicrcles in the center of the picture
cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 20, (0, 0, 255), 1)
cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 10, (0, 255, 0), 1)
cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 2, (255, 0, 0), 2)

# With this for loops a grid is painted on the picture
for y in range(0, frame.shape[0], 40):
    cv2.line(frame, (0, y), (frame.shape[0], y), (255, 0, 0), 1)
    for x in range(0, frame.shape[1], 40):
        cv2.line(frame, (x, 0), (x, frame.shape[1]), (255, 0, 0), 1)

# Draw lines on input image

cv2.imshow("threshold", edged)
cv2.imshow("line detect test", frame)


cv2.waitKey(0)

cv2.destroyAllWindows()
