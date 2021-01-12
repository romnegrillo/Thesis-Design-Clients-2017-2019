import startwindow
import mainwindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys
import imageprocessing
import time
import numpy as np
import os
import RPi.GPIO as GPIO
import cv2

#Last edited: 8:42 PM

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setwarnings(False)

class StartingWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(StartingWindow,self).__init__()

        dirPath=os.path.dirname(os.path.realpath(__file__))
        fileName="startwindow.ui"
        fullPath=dirPath+"/"+fileName
        
        loadUi(fullPath,self)
        self.showFullScreen()
        # Button object names from startwindow.ui
        # imageProcButton
        # closeButton
        # shutdownButton

        self.imageProcButton.clicked.connect(self.imageProcButtonClicked)
        self.ledButton.clicked.connect(self.ledButtonClicked)
        self.closeButton.clicked.connect(self.closeButtonClicked)
        self.shutdownButton.clicked.connect(self.shutdownButtonClicked)
        
        # Initialize led status to 0, off.
        self.ledStatus=0

    def imageProcButtonClicked(self):

        try:
            self.window=MainWindow()
            self.window.show()
            self.close()
        except Exception as exp:
            print(str(exp))

    def ledButtonClicked(self):

        if self.ledStatus==0:
            pass
            # Turn on the led.
            GPIO.output(23,GPIO.HIGH)
            GPIO.output(24,GPIO.HIGH)
            self.ledStatus=1
            #print(self.ledStatus)
        elif self.ledStatus==1:
            pass
            # Turn off the led
            GPIO.output(23,GPIO.LOW)
            GPIO.output(24,GPIO.LOW)
            self.ledStatus=0
            #print(self.ledStatus)

    def closeButtonClicked(self):

        msg=QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, "Close Program", "Are you sure you want to close the program?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        result=msg.exec_()
        
        if result==QtWidgets.QMessageBox.Yes:
            GPIO.cleanup()
            self.close()

    def shutdownButtonClicked(self):
        msg=QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, "Shutdown Device", "Are you sure you want to shutdown the device?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        result=msg.exec_()
        
        if result==QtWidgets.QMessageBox.Yes:
            self.close()
            # os.system("sudo shutdown now")
            
class MainWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()

        dirPath=os.path.dirname(os.path.realpath(__file__))
        fileName="mainwindow.ui"
        fullPath=dirPath+"/"+fileName
        
        loadUi(fullPath,self)
        self.showFullScreen()
        # Button object names from mainwindow.ui
##        captureButton
##        binaryButton
##        totalAreaButton
##        infectedAreaButton
##        clearButton

        # Radio buttons object names from mainwindow.ui
##        singleRadio
##        multiRadio

        # Label object names from mainwindow.ui
##        severityLabel
##        fungiLabel
##        startMenuButton
##        counterLabel

        # Button listeners.
        self.captureButton.clicked.connect(self.captureButtonClicked)
        self.rgbButton.clicked.connect(self.rgbButtonClicked)
        self.binaryButton.clicked.connect(self.binaryButtonClicked)
        self.totalAreaButton.clicked.connect(self.totalAreaButtonClicked)
        self.infectedAreaButton.clicked.connect(self.infectedAreaButtonClicked)
        self.clearButton.clicked.connect(self.clearButtonClicked)
        self.startMenuButton.clicked.connect(self.startMenuButtonClicked)

        # Default radio button selected.
        self.singleRadio.setChecked(True)
        self.multiRadio.setChecked(False)

        self.singleRadio.clicked.connect(self.singleRadioClicked)
        self.multiRadio.clicked.connect(self.multiRadioClicked)

        # Initialize camera and initial image settings.

        try:
            self.imgProc=imageprocessing.Image(rpicamera=True)
            self.imgProc.openCamera()
            self.imgProc.setImageMode(1)
        except Exception as exp:
            print(str(exp))

        # For multicapture mode, store all the severity and average it
        self.severityList=[]

        # For storing the number of capture in multicapture.
        self.multiCount=0

        # Auto word wrap for displaying fungicides needed.
        self.fungiLabel.setWordWrap(True)

        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(5)

    def updateFrame(self):
        #print("Debug")
        try:
            self.image=self.imgProc.getImage()
        except Exception as exp:
            print(str(exp))
        #cv2.imshow("Test",self.img)

        # If there is only 2 items in shape, it means the
        # image is one channel.
        if(len(self.image.shape)==2):
            imageFormat=QtGui.QImage.Format_Indexed8
        # Else, it may be 3 or 4
        else:
            # Get third item which is the number of channels.
            numChannels=self.image.shape[2]
            if numChannels==1:
                #print("Debug1")
                imageFormat=QtGui.QImage.Format_Indexed8
            elif numChannels==3:
                #print("Debug2")
                imageFormat=QtGui.QImage.Format_RGB888
            elif numChannels==4:
                #print("Debug3")
                imageFormat=QtGui.QImage.Format_RGBA8888

        outImage=QtGui.QImage(self.image,self.image.shape[1],self.image.shape[0],self.image.strides[0],imageFormat)

        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(outImage))
        self.imageLabel.setScaledContents(True)
        
    def captureButtonClicked(self):
        #print("Capture Button Clicked")
        # If capture button is clicked, stop the timer
        # to get the current frame.
        
        if self.timer.isActive():
            self.timer.stop()

            # Check if single capture mode.
            if(self.singleRadio.isChecked()):
                currentSeverity=self.imgProc.getSingleSeverity()
                self.severityLabel.setText(str(currentSeverity))
                self.fungiLabel.setText(self.imgProc.getFungicide(currentSeverity))
            elif(self.multiRadio.isChecked()):
                # Multicapture mode.
                # Average every value collected when in
                # multicapture mode.
                
                newSeverity=self.imgProc.getSingleSeverity()
                self.severityList.append(newSeverity)
                aveSeverity=round(np.mean(self.severityList),0)
                
                self.multiCount= self.multiCount+1
                self.severityLabel.setText(str(aveSeverity))
                self.counterLabel.setText(str(self.multiCount))
                self.fungiLabel.setText(self.imgProc.getFungicide(aveSeverity))

            self.imgProc.saveAllImage()
    
            # Save captured image.


            
    def rgbButtonClicked(self):
        self.imgProc.setImageMode(1)

    def binaryButtonClicked(self):
        #print("Binary Button Clicked")
        self.imgProc.setImageMode(2)

    def totalAreaButtonClicked(self):
        #print("Total Area Button Clicked")
        self.imgProc.setImageMode(3)

    def infectedAreaButtonClicked(self):
        #print("Infected Area Button Clicked")
        self.imgProc.setImageMode(4)

    def clearButtonClicked(self):
        #print("Clear Button Clicked")
        if not self.timer.isActive():
            self.timer.start()

    def startMenuButtonClicked(self):
        #print("Start Menu Button Clicked")
        
        if self.timer.isActive():
            self.timer.stop()
        self.imgProc.closeCamera()
        
        self.window=StartingWindow()
        self.window.show()
        self.close()

    def singleRadioClicked(self):
        #print("Single Radio Button Clicked")
        self.multiCount=0
        self.counterLabel.setText(str(self.multiCount))
        self.severityList.clear()

    def multiRadioClicked(self):
        #print("Multi Radio Button Clicked")
        pass
    
    def closeEvent(self, event):

        if self.timer.isActive():
            self.timer.stop()
        self.imgProc.closeCamera()
        
        event.accept()


if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    w=StartingWindow()
    w.show()
    sys.exit(app.exec_())
