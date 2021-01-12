from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.uic import loadUi
import sys
import training_imageprocessing
import os
import datetime
import RPi.GPIO as GPIO

# Record current path of the program where it is.
dirPath = os.path.dirname(os.path.realpath(__file__))
dirPath=dirPath.replace("\\","/")

# UI file names.
trainingMain="/training_main.ui"
fullPathTrainingMain=dirPath+trainingMain

# Old, not used. For refernce only.
###################################################
# Text file records.
textFile="/training_records.txt"
fullPathTextFile=dirPath+textFile

# Image records.
imageFolderBalut="/captured_images_balut"
fullPathImageFolderBalut=dirPath+imageFolderBalut

imageFolderPenoy="/captured_images_penoy"
fullPathImageFolderPenoy=dirPath+imageFolderPenoy
###################################################

# Updated, replaced the old.
##############################################
# Text file records.
textFile1="/training_records_10days.txt"
fullPathTextFile10days=dirPath+textFile1

textFile2="/training_records_14days.txt"
fullPathTextFile14days=dirPath+textFile2

# Image records.
balut10days="/captured_images_balut_10days"
penoy10days="/captured_images_penoy_10days"
balut14days="/captured_images_balut_14days"
penoy14days="/captured_images_penoy_14days"
abnoy14days="/captured_images_abnoy_14days"

fullPathImagebalut10days=dirPath+balut10days
fullPathImagepenoy10days=dirPath+penoy10days
fullPathImagebalut14days=dirPath+balut14days
fullPathImagepenoy14days=dirPath+penoy14days
fullPathImageabnoy14days=dirPath+abnoy14days

relayPin=2
##############################################

class Training(QtWidgets.QMainWindow):

    def __init__(self):
        super(Training,self).__init__()
        loadUi(fullPathTrainingMain, self)

        # Buttons.
        self.rgbButton.clicked.connect(self.rgbButtonClicked)
        self.binaryButton.clicked.connect(self.binaryButtonClicked)
        self.grayButton.clicked.connect(self.grayButtonClicked)
        self.captureButton.clicked.connect(self.captureButtonClicked)
        self.clearDataButton.clicked.connect(self.clearDataButtonClicked)
        
        # Image processing object.
        self.imageObject=training_imageprocessing.ImageProcessing(usbcamera=False,rpicamera=True)
        self.imageObject.openCamera()
        self.imageObject.setImageMode(1)

        # Disable number of pixels view.
        #self.threshPixelsTB.setEnabled(False)

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(relayPin, GPIO.OUT)
        GPIO.output(relayPin, GPIO.LOW)

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

        self.threshPixelsTB.setText(str(self.imageObject.getNumPixels()))

    def rgbButtonClicked(self):
        self.imageObject.setImageMode(1)

    def grayButtonClicked(self):
        self.imageObject.setImageMode(2)

    def binaryButtonClicked(self):
        self.imageObject.setImageMode(3)

    def captureButtonClicked(self):
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Save Data")
        msg.setText("All images will be saved along with its data.\nContinue?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        retValue=msg.exec_()

        if retValue==QtWidgets.QMessageBox.Yes:

            now=datetime.datetime.now()

            balutOrPenoy=str(self.eggCB.currentText())
            mode=str(self.modeCB.currentText())
            #print(balutOrPenoy)
            #print(mode)

            if mode=="10 days mode" and balutOrPenoy=="Abnoy":
                msg=QtWidgets.QMessageBox()
                msg.setWindowTitle("Not Available")
                msg.setText("Abnoy is available only in 14 days mode.")
                msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
                retValue=msg.exec_()

                return

            
            if mode=="10 days mode":
                if balutOrPenoy=="Balut":
                    rgbName=fullPathImagebalut10days+"/rgb_balut_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                    grayName=fullPathImagebalut10days+"/gray_balut_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                    binaryName=fullPathImagebalut10days+"/binary_balut_"+str(now).replace(" ","_").replace(":","_")+".jpg"

                    with open(fullPathTextFile10days,"a") as f:
                        f.write("balut,"+str(self.imageObject.getNumPixels())+"\n")

                    self.imageObject.saveImage(rgbName,grayName,binaryName)
                    
                elif balutOrPenoy=="Penoy":
                    rgbName=fullPathImagepenoy10days+"/rgb_penoy_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                    grayName=fullPathImagepenoy10days+"/gray_penoy_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                    binaryName=fullPathImagepenoy10days+"/binary_penoy_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                               
                    with open(fullPathTextFile10days,"a") as f:
                        f.write("penoy,"+str(self.imageObject.getNumPixels())+"\n")

                    self.imageObject.saveImage(rgbName,grayName,binaryName)
            else:
                if balutOrPenoy=="Balut":
                    rgbName=fullPathImagebalut14days+"/rgb_balut_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                    grayName=fullPathImagebalut14days+"/gray_balut_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                    binaryName=fullPathImagebalut14days+"/binary_balut_"+str(now).replace(" ","_").replace(":","_")+".jpg"

                    with open(fullPathTextFile14days,"a") as f:
                        f.write("balut,"+str(self.imageObject.getNumPixels())+"\n")

                    self.imageObject.saveImage(rgbName,grayName,binaryName)
                    
                elif balutOrPenoy=="Penoy":
                    rgbName=fullPathImagepenoy14days+"/rgb_penoy_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                    grayName=fullPathImagepenoy14days+"/gray_penoy_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                    binaryName=fullPathImagepenoy14days+"/binary_penoy_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                               
                    with open(fullPathTextFile14days,"a") as f:
                        f.write("penoy,"+str(self.imageObject.getNumPixels())+"\n")

                    self.imageObject.saveImage(rgbName,grayName,binaryName)

                elif balutOrPenoy=="Abnoy":
                    rgbName=fullPathImageabnoy14days+"/rgb_penoy_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                    grayName=fullPathImageabnoy14days+"/gray_penoy_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                    binaryName=fullPathImageabnoy14days+"/binary_penoy_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                               
                    with open(fullPathTextFile14days,"a") as f:
                        f.write("abnoy,"+str(self.imageObject.getNumPixels())+"\n")

                    self.imageObject.saveImage(rgbName,grayName,binaryName)
                
    def clearDataButtonClicked(self):
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Clear Data")
        msg.setText("WARNING. All images and data will be deleted.\nContinue?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        retValue=msg.exec_()

        if retValue==QtWidgets.QMessageBox.Yes:

            folder=fullPathImagebalut10days
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)

            folder=fullPathImagepenoy10days
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)

            folder=fullPathImagebalut14days
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)

            folder=fullPathImagepenoy14days
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
                    
            with open(fullPathTextFile10days,"w") as f:
                pass
            
            with open(fullPathTextFile14days,"w") as f:
                pass

    # Close event when pressing X or Alt+F4
    def closeEvent(self, event):
        # Close the timer if active.
        if self.timer.isActive():
            self.timer.stop()
        # Close the camera if active.
        if self.imageObject.isCameraOpen():
            self.imageObject.closeCam()

        GPIO.output(relayPin, GPIO.HIGH)
        GPIO.cleanup()

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    w=Training()
    w.show()
    sys.exit(app.exec_())
