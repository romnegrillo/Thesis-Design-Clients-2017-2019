from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.uic import loadUi
import sys
import training_imageprocessing
import os
import datetime

# Record current path of the program where it is.
dirPath = os.path.dirname(os.path.realpath(__file__))
dirPath=dirPath.replace("\\","/")

# UI file names.
trainingMain="/training_main.ui"
fullPathTrainingMain=dirPath+trainingMain

# Text file records.
textFile="/training_records.txt"
fullPathTextFile=dirPath+textFile

# Image records.
imageFolderBalut="/captured_images_balut"
fullPathImageFolderBalut=dirPath+imageFolderBalut

imageFolderPenoy="/captured_images_penoy"
fullPathImageFolderPenoy=dirPath+imageFolderPenoy

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
            #print(balutOrPenoy)
            

            if balutOrPenoy=="Balut":
                rgbName=fullPathImageFolderBalut+"/rgb_balut_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                grayName=fullPathImageFolderBalut+"/gray_balut_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                binaryName=fullPathImageFolderBalut+"/binary_balut_"+str(now).replace(" ","_").replace(":","_")+".jpg"

                with open(fullPathTextFile,"a") as f:
                    f.write("balut,"+str(self.imageObject.getNumPixels())+"\n")

                self.imageObject.saveImage(rgbName,grayName,binaryName)
                
            elif balutOrPenoy=="Penoy":
                rgbName=fullPathImageFolderPenoy+"/rgb_penoy_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                grayName=fullPathImageFolderPenoy+"/gray_penoy_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                binaryName=fullPathImageFolderPenoy+"/binary_penoy_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                           
                with open(fullPathTextFile,"a") as f:
                    f.write("penoy,"+str(self.imageObject.getNumPixels())+"\n")

                self.imageObject.saveImage(rgbName,grayName,binaryName)
                
    def clearDataButtonClicked(self):
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Clear Data")
        msg.setText("WARNING. All images and data will be deleted.\nContinue?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        retValue=msg.exec_()

        if retValue==QtWidgets.QMessageBox.Yes:
            
            # Delete images for side view.
            folder=fullPathImageFolderBalut
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)

            # Delete images for side view.
            folder=fullPathImageFolderPenoy
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
                    
            with open(fullPathTextFile,"w") as f:
                pass

    # Close event when pressing X or Alt+F4
    def closeEvent(self, event):
        # Close the timer if active.
        if self.timer.isActive():
            self.timer.stop()
        # Close the camera if active.
        if self.imageObject.isCameraOpen():
            self.imageObject.closeCam()

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    w=Training()
    w.show()
    sys.exit(app.exec_())
