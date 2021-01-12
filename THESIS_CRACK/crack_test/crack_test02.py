import cv2
import numpy as np

Kernel_size = 15
low_threshold = 40
high_threshold = 120

rho = 1
threshold = 100
theta = np.pi/180
minLineLength = 1
maxLineGap = 10000000


img = cv2.imread("crack_test.jpeg")

xNew = int(img.shape[1]/2)
yNew = int(xNew*(img.shape[0]/img.shape[1]))
img = cv2.resize(img, (xNew, yNew))

frame = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
t, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)

k = np.array((3, 3), dtype="uint8")
thresh = cv2.erode(thresh, k, iterations=10)
thresh = cv2.dilate(thresh, k, iterations=10)

edged = thresh[:]

lines = cv2.HoughLinesP(edged, 1, np.pi/180, 1, minLineLength=1, maxLineGap=500)

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
# Draw lines on input image
if(lines is not None):
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, 'lines_detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
cv2.imshow("threshold", edged)
cv2.imshow("line detect test", frame)


cv2.waitKey(0)
cv2.destroyAllWindows()
