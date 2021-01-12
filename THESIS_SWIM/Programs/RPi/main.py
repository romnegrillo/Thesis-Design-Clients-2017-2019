from PyQt5 import QtCore, QtGui, QtWidgets
from guidesign import Ui_MainWindow
from pH_ORP_I2C_Class import atlas_i2c 
import sys
import serial
import time
import os

class MainLogic(QtWidgets.QMainWindow, Ui_MainWindow):

    # I2C Address of Sensors
    ORPAddress=98
    pHAddress=99

    # Create the sensor object.
    device=atlas_i2c()

    # Port where Arduino Nano is connected.

    try:
        arduinoPort=serial.Serial("/dev/ttyUSB0",9600)
    except:
        print("Arduino not connected to /dev/ttyUSB0")
        arduinoPort.close()

    try:
        numberOfFiles=len(os.listdir("Records"))
        
        if numberOfFiles==0:
            numberOfFiles=1
        else:
            numberOfFiles=numberOfFiles+1

        fileName="Records"+"/"+"Record No. "+str(numberOfFiles)+".txt"
        file=open(fileName,"a")

    except:
        print("Directory of text file does not exists or previous file is open!","Or Create a folder named 'Records' in the current directory.")
 
    # Restart Arduino Nano program
    # everytime the GUI is opened.
    arduinoPort.setDTR(False)
    time.sleep(1)
    arduinoPort.flushInput()
    arduinoPort.setDTR(True)
    arduinoPort.flush()

    # Variable to record if the windows GUI will be closed or not.
    isClosed=False

    # Timer to loop.
    timer=QtCore.QTimer()
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.showFullScreen()
        self.timer.timeout.connect(self.updatePrint)

        self.minimizeButton.clicked.connect(self.minimizeButtonClicked)
        self.shutdownButton.clicked.connect(self.shutdownButtonClicked)
        
        self.timer.start(1)
        
    def minimizeButtonClicked(self):
        self.showMinimized()

    def shutdownButtonClicked(self):
        msg=QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, "Shutdown", "Shutdown the device?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        result=msg.exec_()
        
        if result==QtWidgets.QMessageBox.Yes:
            print("Shutdown")

    def closeEvent(self, event):

        if self.isClosed==False:
            self.isClosed=True
            time.sleep(1)
            print("Closed")
            toSend="XXX"
            toSend+="\n"
            print("Writing to port...")
            print(toSend,end='')
            self.arduinoPort.write(toSend.encode())
            self.arduinoPort.flush()
            self.arduinoPort.close()
            self.file.close()
            
    def updatePrint(self):

        if self.isClosed==False:

            try:
                myTime12=time.strftime("%I:%M %p",time.localtime())
                myTime24=time.strftime("%H:%M",time.localtime())
                myDate=time.strftime("%m/%d:%Y",time.localtime())

                self.datetimeLabel.setText(str(myDate)+" "+str(myTime12))

                self.device.set_i2c_address(self.ORPAddress)    
                queryValue=self.device.query("R")
                newList=[x for x in list(queryValue) if x.isdigit() or x=="."]
                ORPValue=float(''.join(newList))
             
                self.device.set_i2c_address(self.pHAddress)
                queryValue=self.device.query("R")
                newList=[x for x in list(queryValue) if x.isdigit() or x=="."]
                phValue=float(''.join(newList))

                self.phLabel.setText(str(phValue))
                self.ORPLabel.setText(str(ORPValue))

                toWrite=str(phValue)+"-"+str(ORPValue)+"-"+str(myTime24)+"\n"
                self.file.write(toWrite)
                
                effect=""

                if phValue>8:
                    effect="Chlorine Disinfection Poor, " + \
                           "Eye/Skin Irritation, Straining Plaster, " + \
                           "Algae Growth, Reduced Effectiveness of Bacteride"
                elif phValue<7:
                    effect="Eye/Skin Irritation, " + \
                           "Corrodes Pipes, " + \
                           "Etching of Plasters, " + \
                           "Scale Forming"
                elif phValue>=7 and phValue<8:
                    effect="Most Ideal for Eye or Skin Comfort and Disinfection"

                self.waterStatusLabel.setText(effect)

                toSend='{}'.format(''.join([str(ORPValue),",",str(phValue)]))
                toSend+="\n"
                
                print("Writing to port...")
                print(toSend,end='')
                self.arduinoPort.write(toSend.encode())
            except:
                self.arduinoPort.flush()
                self.arduinoPort.close()
                self.file.close()
                print("An error has occured. Program ended!")

def main():
    app = QtWidgets.QApplication(sys.argv)
    w=MainLogic()
    w.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()

