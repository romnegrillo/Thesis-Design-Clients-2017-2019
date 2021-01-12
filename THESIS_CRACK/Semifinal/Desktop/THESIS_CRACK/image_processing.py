from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import time
import numpy as np

class ImageProcessing:

    def __init__(self,numCrack):
        self.oneLinePixels=5000

        self.thold=200
        self.numCrack=numCrack
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera)

    def getImage(self):
        Kernel_size = 15
        low_threshold = 40
        high_threshold = 120

        rho = 10
        threshold = 15
        theta = np.pi/180
        minLineLength = 10
        maxLineGap = 1
        thold=self.thold


        self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)

        # Get the array of pixels from the captured image.
        self.image=self.rawCapture.array
         
        # Flip the display because PiCamera was placed up side down.
        # Display the image on screen and wait for a keypress.
        image=cv2.flip(self.image,0)

        img = image.copy()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        t, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        k = np.array((3, 3), dtype="uint8")
        #thresh = cv2.erode(thresh, k, iterations=10)
        #thresh = cv2.dilate(thresh, k, iterations=10)

        cv2.rectangle(thresh,(400,210),(900,600),(255),2)
         
        self.rawCapture.truncate(0)

        cropped=thresh[210:600,400:900]
        self.lineNumPixels=cv2.countNonZero(cropped)

        leftCrop=thresh[210:600,400:650]
        rightCrop=thresh[210:600,650:900]

        #cv2.imshow("left",leftCrop)
        #cv2.imshow("right",rightCrop)

        self.leftLineNumPixels=cv2.countNonZero(leftCrop)
        self.rightLineNumPixels=cv2.countNonZero(rightCrop)

        #print(self.leftLineNumPixels, self.rightLineNumPixels)

        
        #cv2.line(thresh,(400,405),(900,405),(255),2)
        print("Current num pixels: ", end="")
        print(self.lineNumPixels)
        
        return thresh

    def getLineNumPixels(self):
        return self.lineNumPixels

    def getOneLineNumPixels(self):
        return self.oneLinePixels

    def getMovement(self):
        if(self.leftLineNumPixels > self.rightLineNumPixels):
            print("To right")
            return "right"
        else:
            print("To left")
            return "left"

    def whileIsCrack(self):
        pass

    def getNumCrack(self):
        return self.numCrack

    def minusNumCrack(self):
        self.numCrack=self.numCrack-1

if __name__=="__main__":
    imgObj=ImageProcessing(1)
    try:
        while 1:
            img=imgObj.getImage()
            imgObj.getMovement()
            cv2.imshow("test",img)

            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break
    except Exception as exp:
        print(str(exp))
