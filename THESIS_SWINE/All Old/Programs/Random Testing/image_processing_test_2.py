import cv2
import numpy as np

# Get input image.
img=cv2.imread("./images/pig2.jpg")
cv2.imshow("Input",img)

# Convert to grayscale and blur noise.
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur=cv2.GaussianBlur(gray,(3,3),0)
cv2.imshow("Gray and Blurred",blur)

# Use adaptive thresholding to find contours.
thresh=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,0)
cv2.imshow("Adaptive Threshold",thresh)

# Detect contours from adaptive thresholding.
threshCopy=thresh.copy()
_,cnts,_=cv2.findContours(threshCopy,cv2.RETR_EXTERNAL,
                          cv2.CHAIN_APPROX_SIMPLE)

if len(cnts):

    # Find the largest contour.
    cntsLenList=[]

    for c in cnts:
        cntsLenList.append(len(c))
        
    indexLargestC=cntsLenList.index(max(cntsLenList))
    
    cv2.drawContours(threshCopy,cnts,-1,(255),-1)
    cv2.imshow("Adaptive Threshold Contours",threshCopy)

# Apply morpgolohical transformation, erode and dilate.
k=np.array((11,11),dtype="uint8")
threshCopy=cv2.dilate(threshCopy,k,iterations=5)
cv2.imshow("Opened",threshCopy)

cv2.waitKey(0)
cv2.destroyAllWindows()
