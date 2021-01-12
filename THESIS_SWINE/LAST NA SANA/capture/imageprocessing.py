import cv2
import numpy as np
import os

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    print("Not in RPi")


class TrainingImageProcessing:

    def __init__(self, usbcam=False, rpicam=False):
        self.usbcam = usbcam
        self.rpicam = rpicam
        self.returnNumber = 0

        if self.usbcam:
            self.cap = cv2.VideoCapture(0)
        elif self.rpicam:
            self.cap = PiCamera()
            self.rawCapture = PiRGBArray(self.cap)

    def getImage(self, imageInput=None):

        if self.usbcam:
            pass
            ret, image = self.cap.read()
            print("debug")
        elif self.rpicam:
            self.cap.capture(self.rawCapture, format="bgr", use_video_port=True)
            image = self.rawCapture.array
            self.rawCapture.truncate(0)
            image = cv2.flip(image, 1)
        else:
            image = cv2.imread(imageInput)

        img = image.copy()

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower1 = (0, 70, 50)
        upper1 = (10, 255, 255)

        thresh1 = cv2.inRange(hsv, lower1, upper1)

        lower2 = (170, 70, 50)
        upper2 = (255, 255, 255)

        thresh2 = cv2.inRange(hsv, lower2, upper2)

        thresh = cv2.bitwise_or(thresh1, thresh2)

        k = np.ones((3,3), dtype = "uint8")
        thresh = cv2.dilate(thresh,k,iterations=3)


        y, x = thresh.shape[:2]
        yNew = 500
        xNew = int((x/y) * yNew)

        img = cv2.resize(img, (xNew, yNew))
        thresh = cv2.resize(thresh, (xNew, yNew))


        # Find contours.
        _, cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        maskBinary = np.zeros(thresh.shape[:2], dtype="uint8")
        maskCnts = np.zeros(thresh.shape[:2], dtype="uint8")
        maskBinaryEllipse = np.zeros(img.shape, dtype="uint8")
            
        # If there is atleast one contours.
        if len(cnts):

            # List for lengths of contours.
            cntsLen = []

            # Append all the length of cnts.
            for i in range(len(cnts)):
                cntsLen.append(len(cnts[i]))

            # Get the max length.
            maxIdxCnts = cntsLen.index(max(cntsLen))

            # Draw the max length contours on another mask.
            # Largest contours.
            #maskBinary = np.zeros(thresh.shape[:2], dtype="uint8")
            #maskCnts = np.zeros(thresh.shape[:2], dtype="uint8")
            #maskBinaryEllipse = np.zeros(img.shape, dtype="uint8")

            cv2.drawContours(maskBinary, cnts, maxIdxCnts, (255), -1)
            cv2.drawContours(maskCnts, cnts, maxIdxCnts, (255), 2)
            cv2.drawContours(maskBinaryEllipse, cnts, maxIdxCnts, (255, 255, 255), -1)

            try:
                ellipse = cv2.fitEllipse(cnts[maxIdxCnts])
                (x, y), (ma, MA), angle = cv2.fitEllipse(cnts[maxIdxCnts])
                cv2.ellipse(maskBinaryEllipse, ellipse, (0, 0, 255), 3)
            except:
                ma=0
                MA=0
            
            self.numWhitePixels = cv2.countNonZero(maskBinary)
            self.totalPixels = img.shape[0]*img.shape[1]
            self.areaPercentage = (self.numWhitePixels/self.totalPixels)*100

            self.ma=ma
            self.MA=MA
            #print(self.areaPercentage)
            #print(ma)
            #print(MA)
            
            self.imageBGR = img
            self.maskBinary = maskBinary
            self.maskCnts = maskCnts
            self.ellipse = maskBinaryEllipse

            print("DEBUG")

        if self.returnNumber == 0:

            image = cv2.cvtColor(self.imageBGR, cv2.COLOR_BGR2RGB)
            return image
        elif self.returnNumber == 1:
            return self.maskBinary
        elif self.returnNumber == 2:
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

    def setReturnNumber(self, num):
        self.returnNumber = num

    def getMaximaEllipse(self):
        return self.MA

    def getMinimaEllipse(self):
        return self.ma

    def saveImage(self, rgbName, binaryName, cntsName, ellipseName):
        cv2.imwrite(rgbName, self.imageBGR)
        cv2.imwrite(binaryName, self.maskBinary)
        cv2.imwrite(cntsName, self.maskCnts)
        cv2.imwrite(ellipseName,self.ellipse)

    def computeWeight(self):
        if view=="side":
            basePath = "./actual_sideview_images/"
            X=sqrt(self.ma**2 + self.MA**2 + self.areaPercentage**2)
            return 0.0551*X-9.4065
        else:
            X=sqrt(self.ma**2 + self.MA**2 + self.areaPercentage**2)
            basePath="./actual_topview_images/"
            return 0.0533*self.X-8.3933
             
        
    # For checking
    def compWeight(self,fileName,view):
        if view=="side":
            basePath = "./actual_sideview_images/"
            basis=[6,6,4,4,12]
        else:
            basePath="./actual_topview_images/"
            basis=[7,6,4,4,11,11,12]
            
        imageList = [i for i in os.listdir(basePath) if ".jpg" in i]
        imageList.sort()
        
        for i,j in enumerate(imageList):
            if j==fileName:
                return basis[i]
            
        return "Error"
