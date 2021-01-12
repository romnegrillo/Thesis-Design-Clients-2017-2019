from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import sys
import imageprocessing
import math

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        loadUi("classify_window.ui", self)
        self.setFixedSize(self.size())
        self.initGui()

    def initGui(self):
        self.mode = ["Top View", "Side View"]
        self.comboBox.addItems(self.mode)
        self.browseButton.clicked.connect(self.browseButtonClicked)
        self.enterButton.clicked.connect(self.enterButtonClicked)
        self.imgObj = imageprocessing.TrainingImageProcessing()

    def browseButtonClicked(self):
        print("Browse button clicked.")

        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Single File', QtCore.QDir.currentPath(), '*.jpg')

        if fileName:
            self.fileName=fileName.replace(".jpg","_x.jpg")
            
             
            image = self.imgObj.getImage(fileName)

            if(len(image.shape) == 2):
                # One channel.
                imageFormat = QtGui.QImage.Format_Indexed8
            else:
                # Check if three or four channels.
                numChannel = image.shape[2]

                if numChannel == 3:
                    imageFormat = QtGui.QImage.Format_RGB888
                elif numChannel == 4:
                    imageFormat = QtGui.QImage.Format_RGBA8888

            outImage = QtGui.QImage(image, image.shape[1], image.shape[0], image.strides[0],
                                    imageFormat)

            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(outImage))
            self.imageLabel.setScaledContents(True)

            image = self.imgObj.getImage(self.fileName)
            self.classificationTB.setText("")
            self.ageTB.setText("")
        
    def enterButtonClicked(self):
        try:
            fileName=self.fileName

            try:
                age=int(self.ageTB.text())
            except Exception as exp:
                print(str(exp))
                messagebox=QtWidgets.QMessageBox()
                messagebox.setText("Please enter a valid age.")
                messagebox.setWindowTitle("Error")
                messagebox.exec_()
                return
                
            
            totalArea = self.imgObj.getAreaPercentage()
            maxima = self.imgObj.getMaximaEllipse()
            minima = self.imgObj.getMinimaEllipse()
            X=math.sqrt((totalArea**2)+(maxima**2)+(minima**2))
 
            mode = str(self.comboBox.currentText())

            print(maxima, minima,totalArea, X)


            print(mode)

            if mode == self.mode[0]:
                print("Top mode selected.")
                weightEstimated=round(0.0533*X-8.3933,4)
              
            elif mode == self.mode[1]:
                print("Side mode selected.")
                weightEstimated=round(0.0551*X-9.4065,4)
    
            print(weightEstimated)

                                                   
            self.weightTB.setText(str(weightEstimated) + " kg")

            #print(f"Age {age}")
            if age in range(4,6):
                if weightEstimated in range(6,8):
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 6.65:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")
                    
            elif age in range(6,8):
                if weightEstimated in range(11,14):
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 11.88:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age in range(8,10):
                if weightEstimated in range(20,23):
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 20.24:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age in range(10,12):
                if weightEstimated in range(28,33):
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 28.98:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age in range(12,14):
                if weightEstimated in range(38,43):
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 38.48:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age in range(14,16):
                if weightEstimated in range(48,55):
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 48.93:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age in range(16,18):
                if weightEstimated in range(61,69):
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 61.75:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age in range(18,20):
                if weightEstimated in range(76, 85):
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 76.68:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")                

            elif age in range(20,22):
                if weightEstimated in range(90, 99):
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 90.25:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")  

            elif age == 22:
                if weightEstimated in range(104, 115):
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 104.5:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            else:
                self.classificationTB.setText("Age out of range.")

                
        except Exception as exp:
            print(str(exp))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
