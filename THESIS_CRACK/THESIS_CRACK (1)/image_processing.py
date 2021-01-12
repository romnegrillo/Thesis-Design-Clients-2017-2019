from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import time

class ImageProcessing:

    def __init__(self,numCrack):
        self.numCrack=numCrack

    def whileIsCrack(self):
        pass

    def getNumCrack(self):
        return self.numCrack

    def minusNumCrack(self):
        self.numCrack=self.numCrack-1
