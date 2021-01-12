from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import sys
import os
import training_imageprocessing
import math
import time
import datetime
import shutil

# Record current path of the program where it is.
dirPath = os.path.dirname(os.path.realpath(__file__))
dirPath=dirPath.replace("\\","/")

# UI file names.
trainingMainFileName="/training_main.ui"
trainingSideFileName="/training_side.ui"
trainingTopFileName="/training_top.ui"

# Directory of the image to save.
trainingSideViewImages="/training_sideview_images"
trainingTopViewImages="/training_topview_images"

# Textfile names.
trainingSideViewTextFile="/side_record.txt"
trainingTopViewTextFile="/top_record.txt"

# Full path of the files above.
fullPathTrainingMain=dirPath+trainingMainFileName
fullPathTrainingSide=dirPath+trainingSideFileName
fullPathTrainingTop=dirPath+trainingTopFileName

fullPathTrainingSideViewImages=dirPath+trainingSideViewImages
fullPathTrainingTopViewImages=dirPath+trainingTopViewImages

fullPathTrainingSideTextFile=dirPath+trainingSideViewTextFile
fullPathTrainingTopTextFile=dirPath+trainingTopViewTextFile

class TrainingMain(QtWidgets.QMainWindow):

    def __init__(self):
        super(TrainingMain,self).__init__()
        loadUi(fullPathTrainingMain,self)
        self.showFullScreen()
        self.setFixedSize(self.frameGeometry().width(),self.frameGeometry().height())

        # Button listeners.
        self.svButton.clicked.connect(self.svButtonClicked)
        self.tvButton.clicked.connect(self.tvButtonClicked)
        self.svpgButton.clicked.connect(self.svpgButtonClicked)
        self.tvpgButton.clicked.connect(self.tvpgButtonClicked)
        self.clearSVButton.clicked.connect(self.clearSVButtonClicked)
        self.clearTVButton.clicked.connect(self.clearTVButtonClicked)
        self.closeButton.clicked.connect(self.closeButtonClicked)
        self.shutdownButton.clicked.connect(self.shutdownButtonClicked)

    # Button events.
    def svButtonClicked(self):
        pass
        try:
            self.w=TrainingSide()
            self.w.show()
            self.close()
        except Exception as exp:
            print(str(exp))

    def tvButtonClicked(self):
        pass
        try:
            self.w=TrainingTop()
            self.w.show()
            self.close()
        except Exception as exp:
            print(str(exp))

    def svpgButtonClicked(self):
        pass

    def tvpgButtonClicked(self):
        pass

    def clearSVButtonClicked(self):
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Clear Side View Data")
        msg.setText("Are you sure you want delete all side view data?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        retValue=msg.exec_()

        if retValue==QtWidgets.QMessageBox.Yes:
            with open(fullPathTrainingSideTextFile,"w") as f:

                # Delete images for side view.
                folder=fullPathTrainingSideViewImages
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(e)

                msg=QtWidgets.QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Side view data deleted.")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                retValue=msg.exec_()

    def clearTVButtonClicked(self):
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle("Clear Top View Data")
        msg.setText("Are you sure you want delete all top view data?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        retValue=msg.exec_()

        if retValue==QtWidgets.QMessageBox.Yes:
            with open(fullPathTrainingTopTextFile,"w") as f:

                # Delete images for side view.
                folder=fullPathTrainingTopViewImages
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(e)
                        
                msg=QtWidgets.QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Top view data deleted.")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                retValue=msg.exec_()

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
            os.system("sudo shutdown now")
    
class TrainingSide(QtWidgets.QMainWindow):

    def __init__(self):
        super(TrainingSide,self).__init__()
        loadUi(fullPathTrainingSide,self)
        self.showFullScreen()
        self.setFixedSize(self.frameGeometry().width(),self.frameGeometry().height())

        # Button listeners.
        self.rgbButton.clicked.connect(self.rgbButtonClicked)
        self.binButton.clicked.connect(self.binButtonClicked)
        self.cntsButton.clicked.connect(self.cntsButtonClicked)
        self.captureButton.clicked.connect(self.captureButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

        # Image processing object.
        self.imageObject=training_imageprocessing.TrainingImageProcessing(usbcam=False,rpicam=True)

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
        
    # Button events.
    def rgbButtonClicked(self):
        self.imageObject.setReturnNumber(0)

    def binButtonClicked(self):
        self.imageObject.setReturnNumber(1)

    def cntsButtonClicked(self):
        self.imageObject.setReturnNumber(2)

    def captureButtonClicked(self):

        weight=self.weightTB.text()
        age=self.ageTB.text()
        
        if weight and \
            not weight.isspace() and \
            age and \
            not age.isspace():

            try:
                weight=int(weight)
                age=int(age)
                numWhitePixels=self.imageObject.getNumWhitePixels()
                totalPixels=self.imageObject.getTotalArea()
                areaPercentage=self.imageObject.getAreaPercentage()
                
                # Record weight, age and number of pixels.
                try:
                    print(weight)
                    print(age)
                    print(numWhitePixels)
                    print(totalPixels)
                    print(areaPercentage)

                    # Write to textfile.
                    with open(fullPathTrainingSideTextFile,"a") as f:
                        toWrite=str(weight) + "," + \
                                 str(age) + "," + \
                                 str(numWhitePixels) + "," + \
                                 str(totalPixels) + "," + \
                                 str(areaPercentage) + "," + \
                                 str(math.log(numWhitePixels)) + \
                                 "\n"

                        
                        f.write(toWrite)

                        now=datetime.datetime.now()

                        rgbName=fullPathTrainingSideViewImages+"/rgb_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                        binaryName=fullPathTrainingSideViewImages+"/binary_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                        cntsName=fullPathTrainingSideViewImages+"/cnts_"+str(now).replace(" ","_").replace(":","_")+".jpg"

                        print(rgbName)
                        print(binaryName)
                        print(cntsName)

                        self.imageObject.saveImage(rgbName,binaryName,cntsName)

                        msg=QtWidgets.QMessageBox()
                        msg.setWindowTitle("Success")
                        msg.setText("Data recorded!")
                        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        retValue=msg.exec_()

                except ZeroDivisionError:
                    msg=QtWidgets.QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setText("No area found.")
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    retValue=msg.exec_()
                    return
                except Exception as exp:
                    print(str(exp))
                    return
                
            except ValueError:
                msg=QtWidgets.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Enter a valid number.")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                retValue=msg.exec_()
                return
        else:
            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Weight and age are required fields.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            retValue=msg.exec_()

    def backButtonClicked(self):
        pass
        # Close the timer if active.
        if self.timer.isActive():
            self.timer.stop()
        # Close the camera if active.
        if self.imageObject.isCameraOpen():
            self.imageObject.closeCam()

        # Open another window.
        self.w=TrainingMain()
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

class TrainingTop(QtWidgets.QMainWindow):

    def __init__(self):
        super(TrainingTop,self).__init__()
        loadUi(fullPathTrainingTop,self)
        self.showFullScreen()
        self.setFixedSize(self.frameGeometry().width(),self.frameGeometry().height())

        # Button listeners.
        self.rgbButton.clicked.connect(self.rgbButtonClicked)
        self.binButton.clicked.connect(self.binButtonClicked)
        self.cntsButton.clicked.connect(self.cntsButtonClicked)
        self.captureButton.clicked.connect(self.captureButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

       # Image processing object.
        self.imageObject=training_imageprocessing.TrainingImageProcessing(usbcam=False,rpicam=True)

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
        
    # Button events.
    def rgbButtonClicked(self):
        self.imageObject.setReturnNumber(0)

    def binButtonClicked(self):
        self.imageObject.setReturnNumber(1)

    def cntsButtonClicked(self):
        self.imageObject.setReturnNumber(2)

    def captureButtonClicked(self):
        
        weight=self.weightTB.text()
        age=self.ageTB.text()
        
        if weight and \
            not weight.isspace() and \
            age and \
            not age.isspace():

            try:
                weight=int(weight)
                age=int(age)
                numWhitePixels=self.imageObject.getNumWhitePixels()
                totalPixels=self.imageObject.getTotalArea()
                areaPercentage=self.imageObject.getAreaPercentage()
                
                # Record weight, age and number of pixels.
                try:
                    print(weight)
                    print(age)
                    print(numWhitePixels)
                    print(totalPixels)
                    print(areaPercentage)

                    # Write to textfile.
                    with open(fullPathTrainingTopTextFile,"a") as f:
                        toWrite=str(weight) + "," + \
                                 str(age) + "," + \
                                 str(numWhitePixels) + "," + \
                                 str(totalPixels) + "," + \
                                 str(areaPercentage) + "," + \
                                 str(math.log(numWhitePixels)) + \
                                 "\n"
                        
                        f.write(toWrite)
                        
                        now=datetime.datetime.now()

                        rgbName=fullPathTrainingTopViewImages+"/rgb_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                        binaryName=fullPathTrainingTopViewImages+"/binary_"+str(now).replace(" ","_").replace(":","_")+".jpg"
                        cntsName=fullPathTrainingTopViewImages+"/cnts_"+str(now).replace(" ","_").replace(":","_")+".jpg"

                        print(rgbName)
                        print(binaryName)
                        print(cntsName)

                        self.imageObject.saveImage(rgbName,binaryName,cntsName)

                        
                        msg=QtWidgets.QMessageBox()
                        msg.setWindowTitle("Success")
                        msg.setText("Data recorded!")
                        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        retValue=msg.exec_()
                        
                except ZeroDivisionError:
                    msg=QtWidgets.QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setText("No area found.")
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    retValue=msg.exec_()
                    return
                except Exception as exp:
                    print(str(exp))
                    return
                
            except ValueError:
                msg=QtWidgets.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Enter a valid number.")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                retValue=msg.exec_()
                return
        else:
            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Weight and age are required fields.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            retValue=msg.exec_()

    def backButtonClicked(self):
        # Close the timer if active.
        if self.timer.isActive():
            self.timer.stop()
        # Close the camera if active.
        if self.imageObject.isCameraOpen():
            self.imageObject.closeCam()

        # Open another window.
        self.w=TrainingMain()
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
    w=TrainingMain()
    w.show()
    sys.exit(app.exec_())
