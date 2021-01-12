import cv2
import numpy as np

img = cv2.imread("./Pig 1/IMG_5499.jpg")

y, x = img.shape[:2]
yNew = 500
xNew = int((x/y) * yNew)

img = cv2.resize(img, (xNew,yNew))
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

_,_,gray = cv2.split(img)
t,thresh = cv2.threshold(gray,170, 255, cv2.THRESH_BINARY_INV)


cv2.imshow("test", thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()
