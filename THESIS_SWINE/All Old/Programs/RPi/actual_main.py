from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import sys
import os
import actual_imageprocessing

# Record current path of the program where it is.
dirPath = os.path.dirname(os.path.realpath(__file__))

# UI file names
actualMainFileName=dirPath+"/actual_main.ui"
actualSideFileName=dirPath+"/actual_side.ui"
actualTopFileName=dirPath+"/actual_top.ui"

class ActualMain(QtWidgets.QMainWindow):

    def __init__(self):
        super(ActualMain,self).__init__()
        loadUi(actualMainFileName,self)

        # Button listeners.

        self.svButton.clicked.connect(self.svButtonClicked)
        self.tvButton.clicked.connect(self.tvButtonClicked)
        self.closeButton.clicked.connect(self.closeButtonClicked)
        self.shutdownButton.clicked.connect(self.shutdownButtonClicked)

    def svButtonClicked(self):
        self.w=ActualSide()
        self.w.show()
        self.close()

        
    def tvButtonClicked(self):
        self.w=ActualTop()
        self.w.show()
        self.close()


    def closeButtonClicked(self):
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Close Program")
        msg.setText("Are you sure you want to close the program?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        retValue=msg.exec_()

        if retValue==QtWidgets.QMessageBox.Yes:
            self.close()

    def shutdownButtonClicked(self):
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Shutdown Device")
        msg.setText("Are you sure you want to shutdown the program?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        retValue=msg.exec_()

        if retValue==QtWidgets.QMessageBox.Yes:
            pass
        
    
class ActualSide(QtWidgets.QMainWindow):

    def __init__(self):
        super(ActualSide,self).__init__()
        loadUi(actualSideFileName,self)

        # Button listeners.
        self.rgbButton.clicked.connect(self.rgbButtonClicked)
        self.binButton.clicked.connect(self.binButtonClicked)
        self.cntsButton.clicked.connect(self.cntsButtonClicked)
        self.captureButton.clicked.connect(self.captureButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

        # Disable line edit for diplaying weight.
        self.weightTB.setEnabled(False)
        
        # Image processing object.
        self.imageObject=actual_imageprocessing.TrainingImageProcessing(usbcam=True,rpicam=False)

        # QtTimer to get image continuosly.
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.updateFrames)

        # Start the timer.
        self.timer.start(1)

    def updateFrames(self):
        # Get the image.
        image=self.imageObject.getImage()

        # First check first how many channels the image is so
        # that it can be formatted properly to display.

        if(len(image.shape)==2):
            # One channel.
            imageFormat=QtGui.QImage.Format_Indexed8
        else:
            # Check if three or four channels.
            numChannel=image.shape[2]

            if numChannel==3:
                imageFormat=QtGui.QImage.Format_RGB888
            elif numChannel==4:
                imageFormat=QtGui.QImage.Format_RGBA8888

        outImage=QtGui.QImage(image, image.shape[1],image.shape[0], image.strides[0],
                              imageFormat)

        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(outImage))
        self.imageLabel.setScaledContents(True)
        
    def rgbButtonClicked(self):
        self.imageObject.setReturnNumber(0)

    def binButtonClicked(self):
        self.imageObject.setReturnNumber(1)

    def cntsButtonClicked(self):
        self.imageObject.setReturnNumber(2)

    def captureButtonClicked(self):
        pass

    def backButtonClicked(self):
        # Close the timer if active.
        if self.timer.isActive():
            self.timer.stop()
        # Close the camera if active.
        if self.imageObject.isCameraOpen():
            self.imageObject.closeCam()

        # Open another window.
        self.w=ActualMain()
        self.w.show()

        # Close current window..
        self.close()

    # Close event when pressing X or Alt+F4
    def closeEvent(self, event):
        # Close the timer if active.
        if self.timer.isActive():
            self.timer.stop()
        # Close the camera if active.
        if self.imageObject.isCameraOpen():
            self.imageObject.closeCam()

class ActualTop(QtWidgets.QMainWindow):

    def __init__(self):
        super(ActualTop,self).__init__()
        loadUi(actualTopFileName,self)

        # Button listeners.        
        self.rgbButton.clicked.connect(self.rgbButtonClicked)
        self.binButton.clicked.connect(self.binButtonClicked)
        self.cntsButton.clicked.connect(self.cntsButtonClicked)
        self.captureButton.clicked.connect(self.captureButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

        # Disable line edit for diplaying weight.
        self.weightTB.setEnabled(False)

        # Image processing object.
        self.imageObject=actual_imageprocessing.TrainingImageProcessing(usbcam=False,rpicam=True)

        # QtTimer to get image continuosly.
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.updateFrames)

        # Start the timer.
        self.timer.start(1)

    def updateFrames(self):
        # Get the image.
        image=self.imageObject.getImage()

        # First check first how many channels the image is so
        # that it can be formatted properly to display.

        if(len(image.shape)==2):
            # One channel.
            imageFormat=QtGui.QImage.Format_Indexed8
        else:
            # Check if three or four channels.
            numChannel=image.shape[2]

            if numChannel==3:
                imageFormat=QtGui.QImage.Format_RGB888
            elif numChannel==4:
                imageFormat=QtGui.QImage.Format_RGBA8888

        outImage=QtGui.QImage(image, image.shape[1],image.shape[0], image.strides[0],
                              imageFormat)

        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(outImage))
        self.imageLabel.setScaledContents(True)
        
    def rgbButtonClicked(self):
        self.imageObject.setReturnNumber(0)

    def binButtonClicked(self):
        self.imageObject.setReturnNumber(1)

    def cntsButtonClicked(self):
        self.imageObject.setReturnNumber(2)

    def captureButtonClicked(self):
        pass

    def backButtonClicked(self):
        # Close the timer if active.
        if self.timer.isActive():
            self.timer.stop()
        # Close the camera if active.
        if self.imageObject.isCameraOpen():
            self.imageObject.closeCam()

        # Open another window.
        self.w=ActualMain()
        self.w.show()

        # Close current window..
        self.close()

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
    w=ActualMain()
    w.show()
    sys.exit(app.exec_())
