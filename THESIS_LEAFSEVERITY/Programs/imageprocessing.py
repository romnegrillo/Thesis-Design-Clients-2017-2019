import cv2
import numpy as np
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import os

class Image:

    # Constructor, select either USB or RPi Camera
    def __init__(self,usbcamera=0,rpicamera=False):

        self.imageMode=1
        self.multicaptureCtr=0
        
        if not rpicamera:
            # USB camera selected.
            self.usbcamera=usbcamera
            self.rpicamera=False
            #print("USB camera selected.")
        else:
            # RPi camera selected.
            self.usbcamera=False
            self.rpicamera=True
            #print("RPi camera selected.")
            pass

    def openCamera(self):

        if not self.rpicamera:
            # USB camera selected.
            self.cap=cv2.VideoCapture(self.usbcamera)
        else:
            # RPi camera selected.
            self.rpicam=PiCamera()
            self.rawCapture = PiRGBArray(self.rpicam)
            pass

    def closeCamera(self):

        if not self.rpicamera:
             # USB camera selected.
            self.cap.release()
        else:
             # RPi camera selected.
             # Autoclose
             self.rpicam.close()
             pass

    def getImage(self):

        if not self.rpicamera:
            self.ret,self.frame=self.cap.read()

            # Read an image for testing purposes.
            # Uncomment it to test.
            #self.frame=cv2.imread("leaf_sample1.jpg")
        else:
            pass
            # Get image from RPi camera.
            self.rpicam.capture(self.rawCapture, format="bgr", use_video_port=True)
            self.frame=self.rawCapture.array
            
        y,x=self.frame.shape[:2]
        self.frame=self.frame[0:y-45,215:x-80]
        rgb=cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
        blurred=cv2.GaussianBlur(gray,(5,5),0)
        
        # Get the threshold using otsu thresholding algorithm.
        t,otsuThres=cv2.threshold(blurred,
                                0,
                                255,
                                cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # Invert it threshold.
        otsuThres=cv2.bitwise_not(otsuThres)
        #adaptive=cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #cv2.THRESH_BINARY,5,1)
        #adaptive=cv2.bitwise_not(adaptive)
                                       
        # Find contours in the binary image.
        _,cnts,_=cv2.findContours(otsuThres,cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

        # Draw and fill the binary image before using it as a mask.
        cv2.drawContours(otsuThres,cnts,-1,(255),-1)

        totalAreaMasked=cv2.bitwise_and(rgb,rgb,mask=otsuThres)

        # Yellow range HSV
        #yellowLowerRange=(0, 90, 90)
        #yellowUpperRange=(24, 255, 255)
        
        yellowLowerRange=(0, 10, 10)
        yellowUpperRange=(25, 255, 255)
        
        # Convert the total masked area to HSV
        # HSV is displayed as VSH to we invert it again using BGR2RGB
        totalMaskedHSV=cv2.cvtColor(totalAreaMasked,cv2.COLOR_RGB2HSV)
        #totalMaskedHSVDisp=cv2.cvtColor(totalMaskedHSV,cv2.COLOR_BGR2RGB)

        # As of now, it gets the yellowish part.
        infectedAreaMask=cv2.inRange(totalMaskedHSV,yellowLowerRange,
                                 yellowUpperRange)
        
        infectedArea=cv2.bitwise_and(totalAreaMasked,totalAreaMasked,
                                     mask=infectedAreaMask)

        totalAreaPixels=cv2.countNonZero(otsuThres)
        totalInfectedPixels=cv2.countNonZero(infectedAreaMask)
        self.severity=round((totalInfectedPixels/totalAreaPixels)*100.0,0)
        #print("Severity %.2f"%severity)

        if self.rpicamera:
            self.rawCapture.truncate(0)

        self.rgbGet=rgb
        self.binaryGet= infectedAreaMask#otsuThres  ######
        self.totalAreaMaskedGet=totalAreaMasked
        self.infectedAreaGet=infectedArea
        
        if self.imageMode==1:
            return self.rgbGet
        elif self.imageMode==2:
            return self.binaryGet
        elif self.imageMode==3:
            return self.totalAreaMaskedGet
        elif self.imageMode==4:
            return self.infectedAreaGet
        
        return self.frame

    def getRGB(self):
        return self.rgbGet

    def getBinary(self):
        return self.binaryGet

    def getTotalArea(self):
        return self.totalAreaMaskedGet

    def getInfectedArea(self):
        return self.infectedAreaGet

    def getSingleSeverity(self):
        return self.severity

    def getFungicide(self,pS):
        if(pS>50):
            return "cypronazole + azoxystrobin onn leaves"
        elif(pS<=15):
            return "cyproconazole on soil and cyproconazole + azoxystrobin on leaves"
        elif(pS>15 and pS<=39):
            return "triadimenol on soil and cyproconazole + trifloxystrobin on leaves"
        elif(pS>39 and pS<=50):
            return "flutriafol on soil and frutriafol on leaves"

    def setImageMode(self, imageMode):
        self.imageMode=imageMode

    def saveAllImage(self):
        dirPath=os.path.dirname(os.path.realpath(__file__))
        fileName="captured_images/"
        fullPath=dirPath+"/"+fileName

        file1=fullPath+"image_rgb_"
        file2=fullPath+"image_binary_"
        file3=fullPath+"image_roi_"
        file4=fullPath+"image_infected_"

        # File number 1 by default.
        # Count number of files in directory
        # and divide it by 4.
        # Increment numFile is it is not equal to 0.
        
        numFile=1
##        print(file1)
##        print(file2)
##        print(file3)
##        print(file4)

        numOfFilesInDir=sum([len(files) for r,d,files in os.walk(fullPath)])
        #print(numOfFilesInDir)

        if numOfFilesInDir!=0:
            numFile=int((numOfFilesInDir/4)+1)

        file1=file1+str(numFile)+".jpg"
        file2=file2+str(numFile)+".jpg"
        file3=file3+str(numFile)+".jpg"
        file4=file4+str(numFile)+".jpg"

        cv2.imwrite(file1,self.rgbGet)
        cv2.imwrite(file2,self.binaryGet)
        cv2.imwrite(file3,self.totalAreaMaskedGet)
        cv2.imwrite(file4,self.infectedAreaGet)
        
