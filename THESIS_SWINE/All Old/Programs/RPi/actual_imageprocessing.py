import cv2
import numpy as np

class TrainingImageProcessing:

    def __init__(self,usbcam=True,rpicam=False):
        self.usbcam=usbcam
        self.rpicam=rpicam
        self.returnNumber=0

        if self.usbcam:
            self.cap=cv2.VideoCapture(0)
            print("debug")
        else:
            pass

    def getImage(self):

        if self.usbcam:
            pass
            ret,image=self.cap.read()
            gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

            # Use otsu thresholding to get the high and low
            # threshold value to be used in Canny edge detector.
            t,thresh=cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV +
                                   cv2.THRESH_OTSU)

            # Perform dilation and erosion
            dilated=cv2.dilate(thresh,None,iterations=1)
            eroded=cv2.erode(dilated,None,iterations=1)
 
            # Find contours.
            _,cnts,_=cv2.findContours(eroded,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

            # If there is atleast one contours.
            if len(cnts):

                # List for lengths of contours.
                cntsLen=[]

                # Append all the length of cnts.
                for i in range(len(cnts)):
                    cntsLen.append(len(cnts[i]))

                # Get the max length.   
                maxIdxCnts=cntsLen.index(max(cntsLen))

                # Draw the max length contours on another mask.
                # Largest contours.
                maskBinary=np.zeros(image.shape[:2],dtype="uint8")
                maskCnts=np.zeros(image.shape[:2],dtype="uint8")
                
                cv2.drawContours(maskBinary,cnts,maxIdxCnts,(255),-1)
                cv2.drawContours(maskCnts,cnts,maxIdxCnts,(255),2)

                self.numWhitePixels=cv2.countNonZero(maskBinary)
                self.totalPixels=image.shape[0]*image.shape[1]
                self.areaPercentage=(self.numWhitePixels/self.totalPixels)*100
                
            if self.returnNumber==0:
                image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                return image
            elif self.returnNumber==1:
                return maskBinary
            elif self.returnNumber==2:
                return maskCnts
            
        else:
            pass

    def isCameraOpen(self):

        if self.usbcam:
            return self.cap.isOpened()
        else:
            pass

    def closeCam(self):
        
        if self.usbcam:
            pass
            self.cap.release()
        else:
            pass

    def getNumWhitePixels(self):
        return self.numWhitePixels

    def getTotalArea(self):
        return self.totalPixels

    def getAreaPercentage(self):
        return self.areaPercentage

    def getEstimatedWeight(self):
        pass

        # Wait for the training data set.
        # It will be added here.

    def setReturnNumber(self,num):
        self.returnNumber=num
