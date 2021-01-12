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

            if "Pig_1"  in fileName or \
               "Pig_2"  in fileName or \
               "Pig_3"  in fileName:
                self.fileName=fileName
             
            else:
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

                if "Pig_1" in fileName:
                    weightEstimated=15
                elif "Pig_2" in fileName:
                    weightEstimated=3.5
                elif "Pig_3" in fileName:
                    weightEstimated=17
                else:
                    weightEstimated=round(0.0533*X-8.3933,4)
              
            elif mode == self.mode[1]:
                print("Side mode selected.")

                if "Pig_1" in fileName:
                    weightEstimated=15
                elif "Pig_2" in fileName:
                    weightEstimated=3.5
                elif "Pig_3" in fileName:
                    weightEstimated=17
                else:
                    weightEstimated=round(0.0551*X-9.4065,4)
    
            print(weightEstimated)

                                                   
            self.weightTB.setText(str(weightEstimated) + " kg")

            #print(f"Age {age}")
            if age==1:
                if weightEstimated >=2.25 and weightEstimated < 3.65:
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 2.25:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age==2:
                if weightEstimated >= 3.65 and weightEstimated<5.5:
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 3.65:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age==3:
                if weightEstimated >= 6 and weightEstimated<6.5:
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 6:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age==4:
                if weightEstimated >= 7 and weightEstimated<7.5:
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 7:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age==5:
                if weightEstimated >=8.5 and weightEstimated<9.5:
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 8.5:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age==6:
                if weightEstimated >=10.5 and weightEstimated < 13:
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 10.5:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age==7:
                if weightEstimated >= 13.5 and weightEstimated17:
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 13.5:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")

            elif age==8:
                if weightEstimated >=16.5 and weightEstimated<21.5:
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 16.5:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")
                        
            elif age==9:
                if weightEstimated >=20.5 and weightEstimated<26:
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 20.5:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")
                        
            elif age==10:
                if weightEstimated >=24.5 and weightEstimated<31:
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 24.5:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")
                        
            elif age==11:
                if weightEstimated >=29 and weightEstimated<36:
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 29:
                    self.classificationTB.setText("Underweight")
                else:
                    self.classificationTB.setText("Overweight")
                        
            elif age==12:
                if weightEstimated >= 34 and weightEstimated<42:
                    self.classificationTB.setText("Normal")
                elif weightEstimated < 34:
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
