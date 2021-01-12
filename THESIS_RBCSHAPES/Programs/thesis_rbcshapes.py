from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import sys
import image_processing as improc
import cv2
import os

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main,self).__init__()

        dirPath=os.path.dirname(os.path.realpath(__file__))
        fileName="thesis_rbcshapes.ui"
        fullPath=dirPath+"/"+fileName
        #print(fullPath)

        loadUi(fullPath,self)
        self.setFixedSize(self.size())
        self.setWindowTitle("Main")
        #self.showFullScreen()
        
        self.descriptionButton.clicked.connect(self.descriptionButtonClicked)
        self.assConditionsButton.clicked.connect(self.assConditionsButtonClicked)
        self.browseButton.clicked.connect(self.browseButtonClicked)
        self.changeViewButton.clicked.connect(self.changeViewButtonClicked)
        self.exitButton.clicked.connect(self.exitButtonClicked)
        
        self.imageObject=improc.ImageProcessing()
        self.mode=1
        
    def browseButtonClicked(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        if fileName:
            print(fileName)

            try:
                self.imageObject.processImage(fileName)
                self.dispImage(self.mode)
            except:
                self.imageObject.setValidImage(False)


    def changeViewButtonClicked(self):
        
        if self.imageObject.getValidImage():
            self.mode=self.mode+1
            #print(self.mode)

            if self.mode>5:
                self.mode=1
            
            self.dispImage(self.mode)
        
    def dispImage(self,imageMode):

        if not self.imageObject.getValidImage():
            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Image selected cannot be processed!")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()

            return
        
        if imageMode==1:
            image=self.imageObject.imageView(1)
        elif imageMode==2:
            image=self.imageObject.imageView(2)
        elif imageMode==3:
            image=self.imageObject.imageView(3)
        elif imageMode==4:
            image=self.imageObject.imageView(4)
        elif imageMode==5:
            image=self.imageObject.imageView(5)            
        
        # First check first how many channels the image is so
        # that it can be formatted properly to display

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

        outImage=QtGui.QImage(image, image.shape[1],image.shape[0], image.strides[0],imageFormat)


        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(outImage))
        self.imageLabel.setScaledContents(True)

        self.statusTB.setText(self.imageObject.getStatus())

    def descriptionButtonClicked(self):
        self.w=DescriptionWindow()
        self.w.show()
        self.close()


    def assConditionsButtonClicked(self):
        self.w=AssociatedConditionsWindow()
        self.w.show()
        self.close()

    def exitButtonClicked(self):
        self.close()

    def closeEvent(self,event):
        event.accept()

class DescriptionWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(DescriptionWindow,self).__init__()

        dirPath=os.path.dirname(os.path.realpath(__file__))
        fileName="description_window.ui"
        fullPath=dirPath+"/"+fileName
        #print(fullPath)

        loadUi(fullPath,self)
        self.setFixedSize(self.size())
        self.setWindowTitle("Description")
        #self.showFullScreen()

        self.backButton.clicked.connect(self.backButtonClicked)
    
    def backButtonClicked(self):
        self.w=Main()
        self.w.show()
        self.close()

class AssociatedConditionsWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(AssociatedConditionsWindow,self).__init__()

        dirPath=os.path.dirname(os.path.realpath(__file__))
        fileName="conditions_window.ui"
        fullPath=dirPath+"/"+fileName
        #print(fullPath)

        loadUi(fullPath,self)
        self.setFixedSize(self.size())
        self.setWindowTitle("Associated Conditions")
        #self.showFullScreen()

        self.backButton.clicked.connect(self.backButtonClicked)
    
    def backButtonClicked(self):
        self.w=Main()
        self.w.show()
        self.close()

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    w=Main()
    w.show()
    app.exec_()
