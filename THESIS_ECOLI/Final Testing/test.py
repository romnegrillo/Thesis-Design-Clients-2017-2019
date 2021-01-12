# Import packages.
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import numpy as np
import argparse
import cv2

sampleNum=5

# Load the image.
image = cv2.imread("Sample 5 ~100 coliform.jpg")
rad=240

# Resize, image sample is too big.
(y,x)=image.shape[:2]
xNew=700
yNew=int(xNew*(y/x))
image = cv2.resize(image,(xNew,yNew))
inputImg=image.copy()
cv2.imshow("Input", image)

# Create mask
(y,x)=image.shape[:2]
(yC,xC)=y//2,x//2
mask=np.zeros((y,x),dtype="uint8")

cv2.circle(mask,(xC,yC),rad,(255),-1)
cv2.imshow("Mask",mask)

masked=cv2.bitwise_and(image,image,mask=mask)
#masked[masked==0]=255

cv2.imshow("Masked",masked)

# Convert to grayscale, blur it
# then apply Otsu's thresholding
gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
blurred=cv2.GaussianBlur(gray,(3,3),0)  
cv2.imshow("Blurred", blurred)


thresh = cv2.threshold(blurred, 110, 255,
	cv2.THRESH_BINARY)[1]
threshCopy=thresh.copy()
cv2.imshow("Thresh",thresh)

#thresh=cv2.erode(thresh,None,iterations=1)
# Compute the exact Euclidean distance from every binary
# Pixel to the nearest zero pixel, then find peaks in this
# distance map
D = ndimage.distance_transform_edt(thresh)
localMax = peak_local_max(D, indices=False, min_distance=5,
	labels=thresh)

# Perform a connected component analysis on the local peaks,
# Using 8-connectivity, then appy the Watershed algorithm
markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=thresh)
print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

# Loop over the unique labels returned by the Watershed
# algorithm
for label in np.unique(labels):
	# If the label is zero, we are examining the 'background'
	# so simply ignore it
	if label == 0:
		continue

	# Otherwise, allocate memory for the label region and draw
	# it on the maskq
	mask = np.zeros(gray.shape, dtype="uint8")
	mask[labels == label] = 255

	# Detect contours in the mask and grab the largest one
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	c = max(cnts, key=cv2.contourArea)

	# Draw a circle enclosing the object
	((x, y), r) = cv2.minEnclosingCircle(c)
	cv2.circle(image, (int(x), int(y)), int(r), (0, 0, 255), 2)
	#cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)),
	#	cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


cv2.putText(image,"Colony Count: %s"%(len(np.unique(labels)) - 1),(10,image.shape[0]-45),cv2.FONT_HERSHEY_PLAIN,
            3,(0,0,255),3)

# Show the output image
cv2.imshow("Output", image)
        

cv2.imwrite("input"+str(sampleNum)+".jpg",inputImg)
cv2.imwrite("threshold"+str(sampleNum)+".jpg",threshCopy)
cv2.imwrite("output"+str(sampleNum)+".jpg",image)


cv2.waitKey(0)
cv2.destroyAllWindows()
