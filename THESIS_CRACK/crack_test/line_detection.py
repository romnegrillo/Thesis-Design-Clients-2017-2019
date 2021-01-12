# Line detection using Probalistic Hough Line Transform.
import cv2
import numpy as np

img = cv2.imread("./crack_test.jpeg")

(y, x) = img.shape[0:2]
xNew = 500
yNew = int((y/x)*xNew)

img = cv2.resize(img, (xNew, yNew), interpolation=cv2.INTER_AREA)
cv2.imshow("Input", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
cv2.imshow("Blurred", blurred)

canny = cv2.Canny(blurred, 100, 250)
cv2.imshow("Canny", canny)

lines = cv2.HoughLinesP(canny, 1, np.pi/180, 10, minLineLength=2, maxLineGap=100)

if(lines is not None):
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("Output", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
