import cv2
import numpy as np
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import time

class ImageProcessing:

    def __init__(self,minRadius,maxRadius):

        self.minRadius=minRadius-1
        self.maxRadius=maxRadius-1
        
        self.bgr=None
        self.gray=None
        self.filtered=None
        self.binary=None
        self.output=None
        
        self.numRBC=None
        self.timeStart=None
        self.timeEnd=None
        self.execTime=None

        self.validImage=False
        self.imagePresent=False

    def processImage(self,imagePath):

        self.validImage=False
        
        # Start the time.
        self.timeStart=time.time()
        
        # Read the image.
        img=cv2.imread(imagePath)

        # Save image copy.
        imgCopy=img.copy()

        # Finding the needed square.
        cv2.rectangle(img,(180,150),(500,475),(0,255,0),2)
        #cv2.imshow("input",img)

        # Cropped
        img=imgCopy[150:475,180:500]
        #cv2.imshow("cropped",img)
        self.bgr=img

        # Convert to grayscale.
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #cv2.imshow("gray",gray)
        self.gray=gray

        # Filter the image.
        filtered=cv2.GaussianBlur(gray,(3,3),0)
        #cv2.imshow("filtered",filtered)
        self.filtered=filtered

        # Detect edges.
        # Sobel
        #edges=cv2.adaptiveThreshold(filtered,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,3,2)
        upperThresh=int(cv2.threshold(filtered, 125,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[0])
        lowerThresh=int(0.5*(upperThresh))
        edges=cv2.Canny(filtered,lowerThresh,upperThresh)
        #cv2.imshow("edges",edges)

        binary=edges.copy()
        self.binary=binary

        # Watershed to find overlapping circles.
        thresh=edges

        D = ndimage.distance_transform_edt(filtered)
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

            if r>(self.minRadius) and r<(self.maxRadius):
                cv2.circle(image, (int(x), int(y)), int(r)+1, (255, 0, 0), 1) 
                radiusList.append(int(r)) 

        radiusList.sort()

        #print("Number of RBC in the given range radius: ", end="")
        numRBC=len(radiusList)
        self.numRBC=numRBC
        #print(numRBC)

        # Show the output image
        #cv2.imshow("Output", image)
        self.output=image

        self.timeEnd=time.time()

        self.execTime=self.timeEnd-self.timeStart
        #print(self.execTime)

        self.validImage=True
        self.imagePresent=True

    def getBGR(self):
        return cv2.cvtColor(self.bgr,cv2.COLOR_BGR2RGB)

    def getGray(self):
        return self.gray

    def getFiltered(self):
        return self.filtered

    def getBinary(self):
        return self.binary

    def getOutput(self):
        return self.output

    def getNumRBC(self):
        return self.numRBC

    def getExecTime(self):
        return round(self.execTime,4)

    def setValidImage(self,isValid):
        self.validImage=isValid

    def getValidImage(self):
        return self.validImage

    def getImagePresent(self):
        return  self.imagePresent

if __name__=="__main__":
    pass
    #test=ImageProcessing(2,6)
    #test.processImage("./test3/sample_17.jpg")
