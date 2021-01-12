from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.uic import loadUi
import sys
import training_imageprocessing
import os
import datetime
import RPi.GPIO as GPIO
import time

# Record current path of the program where it is.
dirPath = os.path.dirname(os.path.realpath(__file__))
dirPath=dirPath.replace("\\","/")

# UI file name
classificationMain="/classification_main.ui"
fullPathClassificationMain=dirPath+classificationMain

# Training record file name.
recordName="/training_records.txt"
fullPathRecordName=dirPath+recordName

class ClassificationMain(QtWidgets.QMainWindow):

    def __init__(self):
        super(ClassificationMain,self).__init__()
        loadUi(fullPathClassificationMain, self)

        # Image processing object.
        self.imageObject=training_imageprocessing.ImageProcessing(usbcamera=False,rpicamera=True)
        self.imageObject.openCamera()
        self.imageObject.setImageMode(1)

        # Disable number of pixels view.
        #self.threshPixelsTB.setEnabled(False)

##        data=[]
##        balut=[]
##        penoy=[]
##
##        with open(fullPathRecordName,"r") as f:
##            data=f.readlines()
##
##            for i in data:
##
##                if i.split(",")[0]=="balut":
##                    balut.append(int(i.split(",")[1]))
##                else:
##                    penoy.append(int(i.split(",")[1]))

##        balut.sort()
##        penoy.sort()
##
##        print(balut)
##        print(penoy)
##
##            print("Balut min and max")
##            print(min(balut))
##            print(max(balut))
##
##            print("Penoy min and max")
##            print(min(penoy))
##            print(max(penoy))
##            
##            self.penoyMin=min(penoy)
##            self.penoyMax=max(penoy)
##
##            self.balutMin=min(balut)
##            self.balutMax=max(balut)


        # Initialize GPIO.
        
        GPIO.setmode(GPIO.BCM)
        self.relayPin=2
        self.redPin=23
        self.greenPin=24
        self.bluePin=25
        
        GPIO.setup(self.relayPin, GPIO.OUT)
        GPIO.output(self.relayPin, GPIO.LOW)

        GPIO.setup(self.redPin, GPIO.OUT)
        GPIO.setup(self.greenPin, GPIO.OUT)
        GPIO.setup(self.bluePin, GPIO.OUT)

        GPIO.output(self.redPin, GPIO.LOW)
        GPIO.output(self.greenPin, GPIO.LOW)
        GPIO.output(self.bluePin, GPIO.LOW)
        
        # Start timer to update frames,
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.updateFrames)
        self.timer.start(1)

    def updateFrames(self):

        image=self.imageObject.getFrames()  
        
        if(len(image.shape)==2):
            imageFormat=QtGui.QImage.Format_Indexed8
        else:
            numChannel=image.shape[2]

            if numChannel==3:
                imageFormat=QtGui.QImage.Format_RGB888
            elif numChannel==4:
                imageFormat=QtGui.QImage.Format_RGBA8888
        outImage=QtGui.QImage(image, image.shape[1],image.shape[0], image.strides[0],
                              imageFormat)

        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(outImage))
        self.imageLabel.setScaledContents(True)

        numPixels=self.imageObject.getNumPixels()
        #print(numPixels)

        # Color notes
        # PENOY = RED
        # BALUT = GREEN
        # UNKNOWN = BLUE

        #############
        
        # FERTILIZED
        #if numPixels>=self.balutMin and numPixels<=self.balutMax:
        if numPixels>=20000 and numPixels<60000:
            self.classificationLabel.setText("The egg is fertilized.")
            self.greenON()
        # NOT FERTILIZED
        #elif numPixels>=self.penoyMin and numPixels<=self.penoyMax:
        elif numPixels>=3000 and numPixels<20000:
            self.classificationLabel.setText("The egg is NOT fertilized.")
            self.redON()
        # UNKNOWN
        else:
            self.classificationLabel.setText("The egg is unknown.")
            self.blueON()

    def redON(self):
        GPIO.output(self.redPin, GPIO.HIGH)
        GPIO.output(self.greenPin, GPIO.LOW)
        GPIO.output(self.bluePin, GPIO.LOW)

    def greenON(self):
        GPIO.output(self.redPin, GPIO.LOW)
        GPIO.output(self.greenPin, GPIO.HIGH)
        GPIO.output(self.bluePin, GPIO.LOW)

    def blueON(self):
        GPIO.output(self.redPin, GPIO.LOW)
        GPIO.output(self.greenPin, GPIO.LOW)
        GPIO.output(self.bluePin, GPIO.HIGH)

    # Close event when pressing X or Alt+F4
    def closeEvent(self, event):
        # Close the timer if active.
        if self.timer.isActive():
            self.timer.stop()
        # Close the camera if active.
        if self.imageObject.isCameraOpen():
            self.imageObject.closeCam()

        GPIO.output(self.relayPin, GPIO.HIGH)
        GPIO.cleanup()
        


if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    w=ClassificationMain()
    w.show()
    sys.exit(app.exec_())
