# Import packages.
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import numpy as np
import argparse
import cv2

# Load the image.
image = cv2.imread("sample3.jpg")

# Create a circle mask.
mask=np.zeros((image.shape[:2]),np.uint8)
(x,y)=mask.shape[1]//2,mask.shape[0]//2
# Sample 1 radius = 275
# Sample 2 radius = 286
# Sample 3 radius = 90
rad=276
cv2.circle(mask,(x,y),rad,(255),-1)

# Get ROI and set its background to white.
# Note that this method works only if the colonies
# are lighter than the background.
# If the colonies are darker than the background, we
# will repeat this code in the section below but
# we set the background to black.
imageROI=cv2.bitwise_and(image,image,mask=mask)
imageROI[imageROI==0]=255
#cv2.imshow("Input", imageROI)

# Convert to grayscale, blur it
# then apply Otsu's thresholding
gray = cv2.cvtColor(imageROI, cv2.COLOR_BGR2GRAY)
blurred=cv2.GaussianBlur(gray,(3,3),0)
thresh = cv2.threshold(blurred, 0, 255,
	cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Bit AND the threshold with the circle mask
# and count the number of non-zero pixels.
threshMasked=cv2.bitwise_and(thresh,mask)
countNonZeroInsideDish=cv2.countNonZero(threshMasked)
print(countNonZeroInsideDish)
#cv2.imshow("Debug",threshMasked)
targetPixels=100

# If there are at least 100 pixels, it means that
# the background is darker than the colonies, else
# vice-versa
if countNonZeroInsideDish>targetPixels:
        pass
else:
        # We repeat the same code above but we set the background
        # to black.
        imageROI=cv2.bitwise_and(image,image,mask=mask)
        cv2.imshow("Input", imageROI)

        # Convert to grayscale, blur it
        # then apply Otsu's thresholding
        gray = cv2.cvtColor(imageROI, cv2.COLOR_BGR2GRAY)
        blurred=cv2.GaussianBlur(gray,(3,3),0)
        thresh = cv2.threshold(blurred, 0, 255,
                cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]                       

#cv2.imshow("Thresh", thresh)

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
	# it on the mask
	mask = np.zeros(gray.shape, dtype="uint8")
	mask[labels == label] = 255

	# Detect contours in the mask and grab the largest one
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	c = max(cnts, key=cv2.contourArea)

	# Draw a circle enclosing the object
	((x, y), r) = cv2.minEnclosingCircle(c)
	cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
	cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)),
		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# Show the output image
#cv2.imshow("Output", image)

