import cv2
import numpy as np
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage

minRadius=2
maxRadius=6

# Read the image.
img=cv2.imread("./test3/sample_17.jpg")

# Save image copy.
imgCopy=img.copy()

# Finding the needed square.
cv2.rectangle(img,(180,150),(500,475),(0,255,0),2)
cv2.imshow("input",img)

# Cropped
img=imgCopy[150:475,180:500]
cv2.imshow("cropped",img)

# Convert to grayscale.
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("gray",gray)

# Filter the image.
filtered=cv2.GaussianBlur(gray,(3,3),0)
cv2.imshow("filtered",filtered)

# Detect edges.
edges=cv2.adaptiveThreshold(filtered,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,6)
#edges=cv2.Canny(filtered,127,200)
cv2.imshow("edges",edges)

# Watershed to find overlapping circles.
thresh=edges

D = ndimage.distance_transform_edt(thresh)
localMax = peak_local_max(D, indices=False, min_distance=1,
	labels=thresh)
 
# perform a connected component analysis on the local peaks,
# using 8-connectivity, then appy the Watershed algorithm
markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=thresh)

image=img.copy()

radiusList=[]

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

    # Filter that radius it should fall between the minimum and max.

    if r>minRadius and r<maxRadius:
        cv2.circle(image, (int(x), int(y)), int(r), (0, 0, 255), 1) 
        radiusList.append(int(r)) 

radiusList.sort()

print("Number of WBC in the given range radius: ", end="")
print(len(radiusList))

# Show the output image
cv2.imshow("Output", image)

cv2.waitKey(0)
cv2.destroyAllWindows()
