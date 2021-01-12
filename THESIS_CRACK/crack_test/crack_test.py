import cv2
import numpy as np

img = cv2.imread("crack_test.jpeg")
xNew = int(img.shape[1]/2)
yNew = int(xNew*(img.shape[0]/img.shape[1]))
img = cv2.resize(img, (xNew, yNew))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
t, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)

k = np.array((3, 3), dtype="uint8")
thresh = cv2.erode(thresh, k, iterations=10)
thresh = cv2.dilate(thresh, k, iterations=10)

lines = cv2.HoughLines(thresh, 1, np.pi/180, 20)
for rho, theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imshow("test", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
