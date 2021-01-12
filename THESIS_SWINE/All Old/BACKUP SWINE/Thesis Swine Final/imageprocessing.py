import cv2
import numpy as np

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

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Use otsu thresholding to get the high and low
        # threshold value to be used in Canny edge detector.
        t, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV +
                                  cv2.THRESH_OTSU)

        # Perform dilation and erosion
        dilated = cv2.dilate(thresh, None, iterations=1)
        eroded = cv2.erode(dilated, None, iterations=1)

        # Find contours.
        _, cnts, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
            maskBinary = np.zeros(image.shape[:2], dtype="uint8")
            maskCnts = np.zeros(image.shape[:2], dtype="uint8")
            maskBinaryEllipse = np.zeros(image.shape, dtype="uint8")

            cv2.drawContours(maskBinary, cnts, maxIdxCnts, (255), -1)
            cv2.drawContours(maskCnts, cnts, maxIdxCnts, (255), 2)
            cv2.drawContours(maskBinaryEllipse, cnts, maxIdxCnts, (255, 255, 255), -1)

            try:
                ellipse = cv2.fitEllipse(cnts[maxIdxCnts])
                (x, y), (self.ma, self.MA), angle = cv2.fitEllipse(cnts[maxIdxCnts])
                cv2.ellipse(maskBinaryEllipse, ellipse, (0, 0, 255), 3)
            except:
                pass
        
            self.numWhitePixels = cv2.countNonZero(maskBinary)
            self.totalPixels = image.shape[0]*image.shape[1]
            self.areaPercentage = (self.numWhitePixels/self.totalPixels)*100

            self.imageBGR = image
            self.maskBinary = maskBinary
            self.maskCnts = maskCnts
            self.ellipse = maskBinaryEllipse

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
