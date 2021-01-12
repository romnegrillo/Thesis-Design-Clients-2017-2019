import imageprocessing
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import os

class StartWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(StartWindow,self).__init__()
        dirPath = os.path.dirname(os.path.realpath(__file__))
        fileName="startwindow.ui"
        fullPath=dirPath+"/"+fileName
        loadUi(fullPath,self)
        
        self.imageProcessingButton.clicked.connect(self.imageProcessingButtonClicked)
        self.impedanceButton.clicked.connect(self.impedanceButtonClicked)
        self.minimizeButton.clicked.connect(self.minimizeButtonClicked)
        self.shutdownButton.clicked.connect(self.shutdownButtonClicked)

    def imageProcessingButtonClicked(self):
        self.close()
        self.w=ImageProcessingWindow()
        self.w.show()

    def openPortButtonClicked(self):
        pass

    def colonyCountGraphClicked(self):
        pass

    def impedanceButtonClicked(self):
        pass

    def minimizeButtonClicked(self):
        self.close()

    def shutdownButtonClicked(self):
        pass

class ImageProcessingWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(ImageProcessingWindow,self).__init__()
        dirPath = os.path.dirname(os.path.realpath(__file__))
        fileName="imageprocwindow.ui"
        fullPath=dirPath+"/"+fileName
        loadUi(fullPath,self)

        #self.imageObject=imageprocessing.ImageProcessing(None,rpicamera=True)
        self.imageObject=imageprocessing.ImageProcessing(usbcamera=0)
        self.backButton.clicked.connect(self.backButtonClicked)
        
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.updateFrames)
        self.timer.start(1)

    def updateFrames(self):
        try:
            image=self.imageObject.getImage()
        except Exception as exp:
            print(str(exp))
        
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
        self.colonyCountText.setText(str(self.imageObject.getColonyCount()))

    def backButtonClicked(self):
        self.closeCameraAndTimer()
        self.close()
        self.w=StartWindow()
        self.w.show()
        
    def closeEvent(self,event):
        self.closeCameraAndTimer()
        event.accept()

    def closeCameraAndTimer(self):

        if self.timer.isActive():
            self.timer.stop()
        if self.imageObject.isCameraOpen():
            self.imageObject.closeCamera()
        

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    w=StartWindow()
    w.show()
    sys.exit(app.exec_())
