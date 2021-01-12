import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

class TrainingImageProcessing:

    def __init__(self,usbcam=True,rpicam=False):
        self.usbcam=usbcam
        self.rpicam=rpicam
        self.returnNumber=0

        if self.usbcam:
            self.cap=cv2.VideoCapture(0)
        else:
            self.cap=PiCamera()
            self.rawCapture=PiRGBArray(self.cap)

    def getImage(self):

        if self.usbcam:
            pass
            ret,img=self.cap.read()
        else:
            self.cap.capture(self.rawCapture, format="bgr", use_video_port=True)
            img=self.rawCapture.array
            self.rawCapture.truncate(0)

        """
        image=cv2.flip(image,1)
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

            self.imageBGR=image
            self.maskBinary=maskBinary
            self.maskCnts=maskCnts
        """
        
        img=cv2.flip(img,1)
        #cv2.imshow("img",img)
        cv2.imwrite("test.jpg",img) 
                    
        hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        #cv2.imshow("hsv",hsv)

        upper=(0,40,90)
        lower=(40,255,255)

        binary=cv2.inRange(hsv,upper,lower)
        k=np.ones((3,3),dtype="uint8")
        binary=cv2.erode(binary,k,iterations=10)
        binary=cv2.dilate(binary,k,iterations=10)
        #cv2.imshow("binary",binary)

        _,cnts,_=cv2.findContours(binary,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cntsLen=[]
        
        for i,c in enumerate(cnts):
            cntsLen.append(len(c))

        
        if cntsLen!=0:

            if cntsLen==1:
                indexLargest=0
            else:
                indexLargest=cntsLen.index(max(cntsLen))
            
            cntsLen.sort(reverse=True)
            
            cntsMask=np.zeros(img.shape[:2],dtype="uint8")
            cv2.drawContours(cntsMask,cnts,indexLargest,(255),3)

            binaryMask=np.zeros(img.shape[:2],dtype="uint8")
            cv2.drawContours(binaryMask,cnts,indexLargest,(255),-1)
            
            #cv2.imshow(file.replace("rgb","cnts"),cntsMask)
            #cv2.imshow(file.replace("rgb","binary"),binaryMask)
             
            #cv2.imwrite(file.replace("rgb","cnts"),cntsMask)
            #cv2.imwrite(file.replace("rgb","binary"),binaryMask)
        

        self.imageBGR=img
        self.maskBinary=binaryMask
        self.maskCnts=cntsMask

        self.numWhitePixels=cv2.countNonZero(binaryMask)
        self.totalPixels=img.shape[0]*img.shape[1]
        self.areaPercentage=(self.numWhitePixels/self.totalPixels)*100
        
        if self.returnNumber==0:
            image=cv2.cvtColor(self.imageBGR,cv2.COLOR_BGR2RGB)
            return image
        elif self.returnNumber==1:
            return self.maskBinary
        elif self.returnNumber==2:
            return self.maskCnts

    def isCameraOpen(self):

        if self.usbcam:
            return self.cap.isOpened()
        else:
            # As long as no camera is functioning,
            # it will remain open.
            return True

    def closeCam(self):
        
        if self.usbcam:
            pass
            self.cap.release()
        else:
            self.cap.close()

    def getNumWhitePixels(self):
        return self.numWhitePixels

    def getTotalArea(self):
        return self.totalPixels

    def getAreaPercentage(self):
        return self.areaPercentage

    def setReturnNumber(self,num):
        self.returnNumber=num

    def saveImage(self,rgbName,binaryName,cntsName):
        cv2.imwrite(rgbName,self.imageBGR)
        cv2.imwrite(binaryName,self.maskBinary)
        cv2.imwrite(cntsName,self.maskCnts)
        
