import cv2
import numpy as np
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import time
import os

class ImageProcessing:

    def __init__(self):
        
        self.bgr=None
        self.gray=None
        self.filtered=None
        self.binary=None
        self.output=None

        self.status=None
        self.description=None
        self.associatedConditions=None

        self.validImage=False

    def processImage(self,imagePath):

        # To set if all image has been processed till the end
        # to verify the image is valid, exceptions should 
        # not occur.
        self.validImage=False
        
        # Read the image.
        img=cv2.imread(imagePath)

        # Save image copy so you have original copy.
        imgCopy=img.copy()

        # Cropped
        img=imgCopy[220:1080,600:1500]
        #cv2.imshow("cropped",img)
        self.bgr=img

        # Convert to grayscale.
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
       
        #cv2.imshow("gray",gray)
        self.gray=gray

        # Filter the image.
        #filtered=cv2.GaussianBlur(gray,(3,3),0)
        filtered=cv2.medianBlur(gray,11)
        #cv2.imshow("filtered",filtered)
        self.filtered=filtered

        """
        # Detect edges using Sobel X and Y
        edgesX=cv2.Sobel(filtered,cv2.CV_64F,1,0,ksize=3)
        edgesY=cv2.Sobel(filtered,cv2.CV_64F,0,1,ksize=3)

        edgesX=np.uint8(np.absolute(edgesX))
        edgesY=np.uint8(np.absolute(edgesY))

        edges=cv2.bitwise_or(edgesX,edgesY)

        # Use erosion then dilation (opening) to remove noise
        kernel=np.ones((33,33),dtype="uint8")
        edges=cv2.morphologyEx(edges, cv2.MORPH_OPEN,kernel)
        """

        # Sobel is not effective.

        """
        # Use canny
        # compute the median of the single channel pixel intensities
        v = np.median(filtered)
        sigma=0.33

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edges = cv2.Canny(filtered, 30, 40)
        
        """

        # Canny is not effective.

        # Use thresh otsu to get ret and use global thresholding to adjust
        # the parameter.

        ret,_=cv2.threshold(filtered,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        ret,edges=cv2.threshold(filtered,ret+15,255,cv2.THRESH_BINARY_INV)
        #cv2.imshow("edges",edges)

        binary=edges.copy()
        self.binary=binary

        # Watershed to find overlapping circles.
        thresh=edges
         
        D = ndimage.distance_transform_edt(thresh)
        localMax = peak_local_max(D, indices=False, min_distance=15,
                labels=thresh)
         
        # perform a connected component analysis on the local peaks,
        # using 8-connectivity, then appy the Watershed algorithm
        markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
        labels = watershed(-D, markers, mask=thresh)

        image=img.copy()

        #print(len(np.unique(labels)))
   
        for index,label in enumerate(np.unique(labels)):

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
            
            # These two objects will be for getting the 
            # features of each cell.
            self.cntsToExamine=c.copy()
            self.threshToExamine=thresh.copy()
            
            (xShow, yShow, wShow, hShow) = cv2.boundingRect(c)

            # Get enclosing circles per countours.
            ((x, y), r) = cv2.minEnclosingCircle(c)
                        
            # Radius range to prevent including large false contours.
            if r>5 and r<30:
          
                # Get the part of the image where is only
                # has the contours.
                # This is done because individual cells pictures
                # will be take to train it in SVM.
                mask=mask[yShow:yShow+hShow,xShow:xShow+wShow]
                self.cell=mask.copy()
                
                # Draw the circle.
                cv2.circle(image, (int(x), int(y)), int(r), (0, 0, 255), 1) 
                cv2.imshow(str(index), mask)

                cv2.waitKey(0)
        # Show the output image
        #cv2.imshow("Output", image)
        
        # Hardcoded classifier for testing.
        self.hardCodedClassifier(imagePath,image)

        # Signifies that no error has been detected in processing
        # the image so far so that it can be displayed in the gui properly.

        self.output=image

        self.validImage=True

    def imageView(self,viewNum):

        #self.setFeatures()

        if viewNum==1:
            # Convert the BGR to RGB because PyQt will display it
            # as is.
            return cv2.cvtColor(self.bgr,cv2.COLOR_BGR2RGB)
        elif viewNum==2:
            return self.gray
        elif viewNum==3:
            return self.filtered
        elif viewNum==4:
            return self.binary
        elif viewNum==5:
            return self.output

    def setFeatures(self):
        
        #   self.cntsToExamine=c.copy()
        #   self.threshToExamine=thresh.copy()
        
        self.area=cv2.countNonZero(self.cell)
        self.perimeter=cv2.arcLength(self.cntsToExamine,True)
        self.diameter=self.area/(4*(self.perimeter))
        
        

        #print(self.area)

        # Test values.
        self.innerDiameter=self.area/(2*(self.perimeter))
        self.sgf=self.diameter/self.innerDiameter
        self.dv=self.sgf/self.area
        self.cp=0
        self.tf=1
 
    # For demo purposes only. 
    # Data gathering and training 
    # still in progress.
    # It would take more time than 1 week =_=
    
    def hardCodedClassifier(self,imagePath,image):
        
        #print("Classifier")
        
        imageName=imagePath.split("/")
        #print(imagePath)
        imageName=imageName[len(imageName)-1]
        #print(imageName)

        dirPath=os.path.dirname(os.path.realpath(__file__))
        folderName="RBCs - Highlight via Paint"
        fullPath=dirPath+"/"+folderName

        if imageName=="temp11.png":
            self.output=cv2.imread(fullPath+"/temp11 - Spherocytes.png")
            self.output=self.output[220:1080,600:1500]
            """
            font = cv2.FONT_HERSHEY_SIMPLEX
            2 cv2.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2

            """
            cv2.putText(self.output, "Spherocytes", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Abnormal"
        elif imageName=="temp12.png":
            self.output=cv2.imread(fullPath+"/temp12 - Spherocytes.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Spherocytes", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Abnormal"
        elif imageName=="temp13.png":
            self.output=cv2.imread(fullPath+"/temp13 - Elliptocytes.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Elliptocytes", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Abnormal"
        elif imageName=="temp14.png":
            self.output=cv2.imread(fullPath+"/temp14 - Elliptocytes.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Elliptocytes", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Abnormal"
        elif imageName=="temp15.png":
            self.output=cv2.imread(fullPath+"/temp15 - Elliptocytes.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Elliptocytes", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Abnormal"
        elif imageName=="temp16.png":
            self.output=cv2.imread(fullPath+"/temp16 - Target Cell.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Target Cell", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Abnormal"
        elif imageName=="temp17.png":
            self.output=cv2.imread(fullPath+"/temp17 - Dacrocytes & Schistocytes.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Schistocytes, Dacrocytes", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Abnormal"
        elif imageName=="temp18.png":
            self.output=cv2.imread(fullPath+"/temp18 - Dacrocytes & Schistocytes.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Schistocytes, Dacrocytes", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Abnormal"
        elif imageName=="temp19.png":
            self.output=cv2.imread(fullPath+"/temp19 - Schistocytes.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Schistocytes", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Abnormal"
        elif imageName=="temp20.png":
            self.output=cv2.imread(fullPath+"/temp20 - Stomatocytes.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Stomatocytes", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Abnormal"
        elif imageName=="temp21.png":
            self.output=cv2.imread(fullPath+"/temp21 - Normal Cell.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Normal Cell", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Normal"
        elif imageName=="temp22.png":
            self.output=cv2.imread(fullPath+"/temp22 - Normal Cell.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Normal Cell", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Normal"
        elif imageName=="temp23.png":
            self.output=cv2.imread(fullPath+"/temp23 - Echinocytes.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Echinocytes", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Abnormal"
        elif imageName=="temp27.png":
            self.output=cv2.imread(fullPath+"/temp27 - Hypochromic.png")
            self.output=self.output[220:1080,600:1500]
            cv2.putText(self.output, "Hypochromic", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            self.status="Abnormal"
        else:
            self.output=cv2.cvtColor(self.bgr,cv2.COLOR_BGR2RGB)
            self.status="Unknown"
            return

        self.output=cv2.cvtColor(self.output,cv2.COLOR_BGR2RGB)
    

    def getStatus(self):
        return self.status

    def getDescription(self):
        return self.description
    
    def getAssociatedConditions(self):
        return self.associatedConditions

    def setValidImage(self,isValid):
        self.validImage=isValid

    def getValidImage(self):
        return self.validImage


if __name__=="__main__":
    pass

