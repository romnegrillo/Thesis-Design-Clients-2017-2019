import cv2
import numpy as np
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import time

class ImageProcessing:

    def __init__(self,minRadius,maxRadius):

        self.minRadius=minRadius
        self.maxRadius=maxRadius
        
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
        #img=imgCopy[150:475,180:500]

        # Uncropped
        img=imgCopy
        
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
        #edges=cv2.adaptiveThreshold(filtered,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,3,2)

        # Canny edge detector.
        # Parameters cannot be automated since
        # the image involves too much black parts
        # in the microscope.
        edges=cv2.Canny(filtered,127,200)
        #cv2.imshow("edges",edges)
        
        binary=edges.copy()
        self.binary=binary
        
        # Detect contours
        cnts,_=cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        radiusList=[]
        image=img.copy()
        CHTMask=np.zeros(image.shape[:2],dtype="uint8")
        CHTImage=img.copy()
        
        for i,c in enumerate(cnts):

            # Get the radius of every contour.
            ((xC,yC),r)=cv2.minEnclosingCircle(c)
            
            if r>=self.minRadius and r<=self.maxRadius:

                cv2.circle(image,(int(xC),int(yC)),int(r),(0,0,255),1)
                cv2.circle(CHTMask,(int(xC),int(yC)),int(r),(255),1)
                radiusList.append(r)
                #print(r)

        if len(radiusList):
            # Detect contours first and detect circles in the contours
            circles = cv2.HoughCircles(CHTMask,cv2.HOUGH_GRADIENT,1,20)
            
            radiusList.sort()

            #print("Number of RBC in the given range radius: ", end="")
            numRBC=len(radiusList)
            self.numRBC=numRBC
            #print(numRBC)
        else:
            self.numRBC=0

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
        return int(self.numRBC - self.numRBC*0.2)

    def getExecTime(self):
        return round(self.execTime,4)

    def setValidImage(self,isValid):
        self.validImage=isValid

    def getValidImage(self):
        return self.validImage

    def getImagePresent(self):
        return  self.imagePresent

if __name__=="__main__":
    test=ImageProcessing(2,6)
    #test.processImage("./test3/sample_17.jpg")
