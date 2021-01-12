from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import sys
import image_processing as improc

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main,self).__init__()
        loadUi("thesis_rbc.ui",self)
        self.setFixedSize(self.size())
        self.setWindowTitle("THESIS")
        #self.showFullScreen()

        self.browseButton.clicked.connect(self.browseButtonClicked)
        self.rgbButton.clicked.connect(self.rgbButtonClicked)
        self.grayscaleButton.clicked.connect(self.grayscaleButtonClicked)
        self.filteredButton.clicked.connect(self.filteredButtonClicked)
        self.binaryButton.clicked.connect(self.binaryButtonClicked)
        self.outputImageButton.clicked.connect(self.outputImageButtonClicked)
        self.exitButton.clicked.connect(self.exitButtonClicked)
    
        self.imageObject=improc.ImageProcessing(2,6)
        
    def browseButtonClicked(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        if fileName:
            print(fileName)

            try:
                self.imageObject.processImage(fileName)
            except:
                self.imageObject.setValidImage(False)
                
            self.dispImage(1)
    
    def rgbButtonClicked(self):
        self.dispImage(1)
    
    def grayscaleButtonClicked(self):
        self.dispImage(2)
    
    def filteredButtonClicked(self):
        self.dispImage(3)
    
    def binaryButtonClicked(self):
        self.dispImage(4)
    
    def outputImageButtonClicked(self):
        self.dispImage(5)
    
    def dispImage(self,imageMode):

        # First check first how many channels the image is so
        # that it can be formatted properly to display
        if not self.imageObject.getValidImage():
            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Image selected cannot be processed!")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            retValue=msg.exec_()

            return
        
        if imageMode==1:
             image=self.imageObject.getBGR()
        elif imageMode==2:
            image=self.imageObject.getGray()
        elif imageMode==3:
            image=self.imageObject.getFiltered()
        elif imageMode==4:
            image=self.imageObject.getBinary()
        elif imageMode==5:
            image=self.imageObject.getOutput()

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

        self.rbcLabel.setText(str(self.imageObject.getNumRBC()))
        self.procTimeLabel.setText(str(self.imageObject.getExecTime()))

    def exitButtonClicked(self):
        self.close()

    def closeEvent(self,event):
        event.accept()

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    w=Main()
    w.show()
    app.exec_()
