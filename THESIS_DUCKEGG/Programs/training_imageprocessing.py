import cv2
import datetime
import os
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

class ImageProcessing:

    def __init__(self,usbcamera=True,rpicamera=False):

        self.usbcamera=usbcamera
        self.rpicamera=rpicamera
        self.imageMode=1

    def openCamera(self):

        if not self.rpicamera:
            self.capture=cv2.VideoCapture(0)
        else:
            self.rpicapture=PiCamera()
            self.rawCapture=PiRGBArray(self.rpicapture)

    def closeCamera(self):

        if not self.rpicamera:
            self.capture.release()
        else:
            self.rpicapture.close()

    def getFrames(self):

        if not self.rpicamera:
            ret,self.frame=self.capture.read()
        else:
            self.rpicapture.capture(self.rawCapture, format="bgr", use_video_port=True)
            self.frame=self.rawCapture.array
            self.rawCapture.truncate(0)

        self.frame=cv2.flip(self.frame,0)
        y,x=self.frame.shape[:2]
        

        # Localize.
        self.frame=self.frame[140:y-190,110:x-390]
        self.bgr=self.frame

        # Grayscale
        self.gray=cv2.cvtColor(self.bgr,cv2.COLOR_BGR2GRAY)

        # CLAHE
        clahe = cv2.createCLAHE(clipLimit=40.0, tileGridSize=(8,8))
        self.claheImg = clahe.apply(self.gray)

        y,x=self.frame.shape[:2]
        
        # Create mask 01/20/2019
        self.mask=np.zeros((y,x),np.uint8)
        cv2.ellipse(self.mask,(x//2,(y//2)+70),(135,200),0,0,360,255,-1)
        self.maskedClahe=cv2.bitwise_and(self.claheImg,self.claheImg,mask=self.mask)
        ########################
        
        t,self.thresh=cv2.threshold(self.maskedClahe,170,255,cv2.THRESH_BINARY_INV)

        self.thresh=cv2.bitwise_and(self.thresh,self.mask)

        if self.imageMode==1:
            return cv2.cvtColor(self.bgr,cv2.COLOR_BGR2RGB)
        elif self.imageMode==2:
            return self.maskedClahe
        elif self.imageMode==3:
            return self.thresh

    def setImageMode(self, num):
        self.imageMode=num
        
    def getNumPixels(self):
        return cv2.countNonZero(self.thresh)

    def saveImage(self,rgbName,grayName,binaryName):
        cv2.imwrite(rgbName,self.bgr)
        cv2.imwrite(grayName,self.gray)
        cv2.imwrite(binaryName,self.thresh)

    def isCameraOpen(self):
        # Always true for RPiCam once the program starts.
        return True

    def closeCam(self):

        if not self.rpicamera:
            self.capture.release()
        else:
            self.rpicapture.close()
         
