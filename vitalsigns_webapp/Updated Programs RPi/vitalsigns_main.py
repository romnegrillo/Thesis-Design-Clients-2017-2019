from __future__ import annotations
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import sys
import serial
from typing import *
import sys
import os
from matplotlib.backends.qt_compat import QtCore, QtWidgets
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
import numpy as np
import time
from datetime import datetime
from matplotlib.backends.qt_compat import QtCore, QtWidgets
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
import numpy as np
import sys
import pyrebase
from firebase_admin import credentials
import firebase_admin
inRPi = True

try:
    import RPi.GPIO
except ImportError:
    inRPi = False

# Record current path of the program where it is.
dirPath = os.path.dirname(os.path.realpath(__file__))
dirPath = dirPath.replace("\\", "/")

# Serial ports parameters, same ports, just separated variables for different testing.
# sensorPort = "/dev/ttyUSB0"
sensorPort = "COM14"
current_user_UID=""
latitudeCoordinate=""
longitudeCoordinate=""

adminDoctorKey = "j7FEbdLjTsWUtGomO5WkyCYED5t1"

config = {
    "apiKey": "AIzaSyDGD8ewVOBVxl6O1r35Npy2RRw2dlWGdP8",
    "authDomain": "mapuavitalsignsdatabase.firebaseapp.com",
    "databaseURL": "https://mapuavitalsignsdatabase.firebaseio.com",
    "projectId": "mapuavitalsignsdatabase",
    "storageBucket": "mapuavitalsignsdatabase.appspot.com",
    "messagingSenderId": "582213066054",
    "appId": "1:582213066054:web:ab72ca16bf4849166bd947",
    "measurementId": "G-G5FC6W67QF",
    "serviceAccount": dirPath+"/mapuavitalsignsdatabase-firebase-adminsdk-uphv7-0cff4fb849.json"

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def loadSensors():
    global latitudeCoordinate
    global longitudeCoordinate

    try:
        data = sensorSerial.readline().decode()
        if "XFLAG" not in data:
            return False
        else:
            latitudeCoordinate=data.split(",")[3]
            longitudeCoordinate=data.split(",")[4]

            if(float(latitudeCoordinate)==0):
                latitudeCoordinate="14.5905"
            if(float(longitudeCoordinate)==0):
                longitudeCoordinate="120.9781"

            print("Latitude: " + latitudeCoordinate)
            print("Longitude: " + longitudeCoordinate)
            return True
    except Exception as exp:
        print(str(exp))
        return False
    
try:
    
    sensorSerial = serial.Serial(sensorPort, 9600)
    print("Sensor port opened.")

    while True:
        print("Loading sensors (body temp, GPS, GSM)...")
        if loadSensors():
            break
   
except Exception as exp:
    print(str(exp))

    

class Login(QtWidgets.QMainWindow):
    
    def __init__(self):

        super(Login, self).__init__()
        loadUi(dirPath+"/vitalsigns_login.ui", self)

        if inRPi:
            self.showFullScreen()

        self.loginButton.clicked.connect(self.loginButtonClicked)
        self.guestButton.clicked.connect(self.guestButtonClicked)
        self.exitButton.clicked.connect(self.exitButtonClicked)

    def loginButtonClicked(self):
        global current_user_UID
        global adminDoctorKey
        
        username = self.usernameTB.text()
        password = self.passTB.text()

        if username and password:
            try:

                print("Logging in.")
                print(username, password)

                user = auth.sign_in_with_email_and_password(username, password)
                auth.refresh(user['refreshToken'])
                
                current_user_UID=user["localId"]

                print("UID")
                print(current_user_UID)
                print("Logged in.")

                if current_user_UID!=adminDoctorKey:
                    self.userWindow=User()
                    self.close()
                    self.userWindow.show()
                else:
                    message = QtWidgets.QMessageBox()
                    message.setWindowTitle("Warning")
                    message.setText("Admin cannot login in this device.")
                    message.setIcon(QtWidgets.QMessageBox.Question)
                    message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            except ConnectionError as exp:
                print(str(exp))
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Warning")
                message.setText("Invalid username and/or password")
                message.setIcon(QtWidgets.QMessageBox.Question)
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()
            except Exception as exp:
                print(str(exp))
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Warning")
                message.setText("Cannot connect to the cloud. Make sure you have proper internet connection and it is not blocking it.")
                message.setIcon(QtWidgets.QMessageBox.Question)
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()

    def guestButtonClicked(self):

        message = QtWidgets.QMessageBox()
        message.setWindowTitle("Warning")
        message.setText("You won't save any data in guest mode, is that okay?")
        message.setIcon(QtWidgets.QMessageBox.Question)
        message.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        choice = message.exec_()

        if choice == QtWidgets.QMessageBox.Ok:
            current_user_UID=""
            self.userWindow = User()
            self.userWindow.show()
            self.hide()

    def exitButtonClicked(self):
        self.hide()


class User(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(User, self).__init__()
        loadUi(dirPath+"/vitalsigns_user.ui", self)
        self.counterNext = 0

        if inRPi:
            self.showFullScreen()

        self.continueButton.clicked.connect(self.continueButtonClicked)
        self.logoutButton.clicked.connect(self.logoutButtonClicked)

    def continueButtonClicked(self):

        try:
            if self.counterNext == 0:
                self.label_2.setText("")
                self.label_2.setStyleSheet("background-image: url('" + dirPath + "/connection.PNG');\n"
                                           "background-position: center; \n"
                                           "background-repeat: no-repeat;\n")
                self.counterNext = self.counterNext+1
            elif self.counterNext == 1:
                self.counterNext = self.counterNext-1
                
                self.symptomsWindow = Symptoms()
                self.symptomsWindow.show()
                self.close()
        except Exception as exp:
            print(str(exp))

    def logoutButtonClicked(self):

        if self.counterNext == 0:
            self.loginWindow = Login()
            self.loginWindow.show()
            self.close()
            self.counterNext = self.counterNext + 1

        elif self.counterNext == 1:
            self.label_2.setText("In the next window, you will be asked to answer a form indicating\nsymptoms you are experiencing.\n\nNext is use the arm blood pressure monitor to know your blood pressure\nand heart rate.\n\nThen in the last part you have to put your finger through\nthe body temperature sensor.\n\nTo view your respiratory rate, click ECG button in the last window and\nwait for it to stabilize then go back to the previous window to view respiratory rate. ")
            self.label_2.setStyleSheet(
                "background-color: qconicalgradient(cx:1, cy:1, angle:0, stop:0 rgba(1, 255, 72, 255), stop:1 rgba(255, 255, 255, 255));")
            self.counterNext = self.counterNext-1


class Symptoms(QtWidgets.QMainWindow):

    def __init__(self):
        super(Symptoms, self).__init__()
        loadUi(dirPath+"/vitalsigns_symptoms.ui", self)

        if inRPi:
            self.showFullScreen()

        self.symptomsNameToFirebase = [
            "abdominal_pain",	
            "arm_pain",	
            "back_pain",	
            "body_aches",	
            "breast_pain",	
            "breathing_difficulty",	
            "chest_pain",	
            "congestion",	
            "cough",	
            "diarrhea",	
            "ear_pain",	
            "excessive_sweating",	
            "faintness",	
            "fatigue",	
            "flu",	
            "gas",	
            "genitcal_itching",	
            "headache",	
            "irregular_periods",	
            "joint_pain",	
            "leg_pain",	
            "mouth_lesions",	
            "nausea",	
            "neck_pain",	
            "rectal_bleeding",	
            "rush",	
            "skin_lump",	
            "sore_throat",	
            "vomiting",
        ]

        self.symptomsValueToFirebase = []

        self.symptomsNameList = [
            "Abdominal_Pain",	
            "Arm_Pain",	
            "Back_Pain",	
            "Body_Aches",	
            "Breast_Pain",	
            "Breathing_Difficulty",	
            "Chest_Pain",	
            "Congestion",	
            "Cough",	
            "Diarrhea",	
            "Ear_Pain",	
            "Excessive_Sweating",	
            "Faintness",	
            "Fatigue",	
            "Flu",	
            "Gas",	
            "Genitcal_Itching",	
            "Headache",	
            "Irregular_Periods",	
            "Joint_Pain",	
            "Leg_Pain",	
            "Mouth_Lesions",	
            "Nausea",	
            "Neck_Pain",	
            "Rectal_Bleeding",	
            "Rush",	
            "Skin_Lump",	
            "Sore_Throat",	
            "Vomiting",
        ]
        
        self.labelList = []
        self.comboBoxList = []

        for i in range(1,30):
            self.labelList.append("label_"+str(i))
            self.comboBoxList.append("comboBox_"+str(i))

 
        for i in self.comboBoxList:
            eval("self."+i).addItems([str(i) for i in range(0,11)])

 
        for i,symptomsName in zip(self.labelList,self.symptomsNameList):
            eval("self."+i).setText(str(symptomsName))

        self.continueButton.clicked.connect(self.continueButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

    def continueButtonClicked(self):
        global current_user_UID
        
        try:
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Are you sure?")
            message.setText("Are you sure you filled all symptoms you are experiencing?")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            choice = message.exec_()
            
 

            if choice == QtWidgets.QMessageBox.Ok:
                for i in self.comboBoxList:
                    self.symptomsValueToFirebase.append(eval("self."+i).currentText())

                    self.symptomsWithValuesToFirebase = dict(zip(self.symptomsNameToFirebase,self.symptomsValueToFirebase))

                print(self.symptomsWithValuesToFirebase)

                if current_user_UID!="":
                    db.child("users").child(current_user_UID).child("usersymptoms").set(self.symptomsWithValuesToFirebase)
                    
                self.bpWindow = BloodPressure()
                self.bpWindow.show()
                self.close()

        except Exception as exp:
            print(str(exp))
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Warning")
            message.setText("Make sure you have proper internet connection.")
            message.setIcon(QtWidgets.QMessageBox.Question)
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()

    def backButtonClicked(self):
        self.userWindow = User()
        self.userWindow.show()
        self.hide()


class BloodPressure(QtWidgets.QMainWindow):

    def __init__(self):
        super(BloodPressure, self).__init__()
        loadUi(dirPath+"/vitalsigns_bloodpressure.ui", self)

        if inRPi:
            self.showFullScreen()

        self.continueButton.clicked.connect(self.continueButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

    def continueButtonClicked(self):
        global sensorSerial
        try:

            # Update bp and heart rate in next window.

            systolic = round(float(self.sysTB.text()), 2)
            diastolic = round(float(self.diaTB.text()), 2)
            heartRate = round(float(self.heartTB.text()), 2)

            data = {
                "systolic": systolic,
                "diastolic": diastolic,
                "heartRate": heartRate,
            }
            
            bp_and_heartrate = data

            # Clear buff.

             
        
            self.mainWindow = Main(bp_and_heartrate)
            self.mainWindow.show()
            self.close()
            
        except Exception as exp:
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Error")
            message.setText("Invalid input detected.\nPlease input a valid data.")
            message.exec_()
        

    def backButtonClicked(self):
        self.symptomsWindow = Symptoms()
        self.symptomsWindow.show()
        self.hide()


class Main(QtWidgets.QMainWindow):

    def __init__(self, bp_and_heartrate):
        global current_user_UID
        global sensorSerial
        
        super(Main, self).__init__()
        loadUi(dirPath+"/vitalsigns_main.ui", self)

        if inRPi:
            self.showFullScreen()

        self.bp_and_heartrate=bp_and_heartrate

        sensorSerial.flushInput()
        sensorSerial.flushOutput()

        self.backButton.clicked.connect(self.backButtonClicked)
        self.viewECGButton.clicked.connect(self.viewECGButtonClicked)
        self.callButton.clicked.connect(self.callButtonClicked)

        try:
            # Get user info first.
            if current_user_UID=="":
                self.userAge = 25
                self.nameTB.setText("Guest")
            else:
                self.userAge = int(db.child("users").child(current_user_UID).child("userinfo").child("age").get().val())
                self.name = db.child("users").child(current_user_UID).child("userinfo").child("full_name").get().val()
                self.location = db.child("users").child(current_user_UID).child("userinfo").child("address").get().val()
                self.gender = db.child("users").child(current_user_UID).child("userinfo").child("gender").get().val()
                self.doctorNumber =  db.child("users").child(current_user_UID).child("userinfo").child("assigned_doctor_number").get().val()

                self.nameTB.setText(str(self.name))
                self.locationTB.setText(str(self.location))
                self.sexTB.setText(str(self.gender))
                self.ageTB.setText(str(self.userAge))
                
                db.child("users").child(current_user_UID).update({"assessment": ""})

                my_stream = db.child("users").child(current_user_UID).child("assessment").stream(self.stream_handler)
        except Exception as exp:
            print(str(exp))
            
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(1000)


    def callButtonClicked(self):
        global sensorSerial
        global current_user_UID

        if current_user_UID!="":
        
            try:
                # Send call command.
                 
                toSend = "3,+63" + self.doctorNumber[1:]
                print(toSend)
                
                sensorSerial.write(toSend.encode())    
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Calling")
                message.setText("Calling assigned doctor. Please wait.")
                choice = message.exec_()

                 

                if choice == QtWidgets.QMessageBox.Ok:
                    # Send hang up command.
                    sensorSerial.write("4\r\n".encode())
            except Exception as exp:
                print(str(exp))
        else:
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Warning")
            message.setText("Call not available for guest mode.")
            choice = message.exec_()

    def backButtonClicked(self):
        
        if self.timer.isActive():
            self.timer.stop()


        self.bpWindow = BloodPressure()
        self.bpWindow.show()
        self.hide()
        
    def stream_handler(self,message):
        
        print(message["data"])
        try:
             
            self.doctorAssessmentTextbox.insertPlainText(message["data"]+"\n")
        except Exception as exp:
            print(str(exp))

     

    def updateTimer(self):
        global current_user_UID
        global sensorSerial
        global latitudeCoordinate
        global longitudeCoordinate
        
        try:
 
            data = sensorSerial.readline().decode()
            

            if "XFLAG" in data:
                self.bodyTemp = float(data.split(",")[1])
            else:
                self.bodyTemp = 0
                
            self.heartRate = self.bp_and_heartrate["heartRate"]
            self.diastolic = self.bp_and_heartrate["diastolic"]
            self.systolic = self.bp_and_heartrate["systolic"]

            print(self.bodyTemp, self.heartRate, self.diastolic, self.systolic)
 
            # Body Temp
            # For babies, children, adults:
            # Based on table
            self.bodyTempStatus = "Normal"
            
            # Children and adults
            if self.userAge <= 65 and self.userAge > 3:
                if self.bodyTemp >= 37.2:
                    self.bodyTempStatus = "Fever"
                elif self.bodyTemp < 35:
                    self.bodyTempStatus = "Hypothermia"
                else:
                    self.bodyTempStatus = "Unknown"
            # Babies, 3 months to 3 years
            elif self.userAge <= 3:
                if self.bodyTemp >= 38.9:
                    self.bodyTempStatus = "Fever"
                elif self.bodyTemp < 35:
                    self.bodyTempStatus = "Hypothermia"
                else:
                    self.bodyTempStatus = "Unknown"
            # Over 65
            else:
                if self.bodyTemp >= 37.2:
                    self.bodyTempStatus = "Fever"
                elif self.bodyTemp < 35:
                    self.bodyTempStatus = "Hypothermia"
                else:
                    self.bodyTempStatus = "Unknown"

            # Blood pressure
            # Based from table.
            if self.systolic < 120 and self.diastolic < 80:
                self.bpStatus = "Normal"
            elif self.systolic >= 120 and self.systolic <= 129 and self.diastolic < 80:
                self.bpStatus = "Elevated"
            elif (self.systolic >= 130 and self.systolic <= 139) or (self.diastolic >= 80 and self.diastolic <= 89):
                self.bpStatus = "High BP Stage 1"
            elif (self.systolic >= 140 and self.systolic < 180) or (self.diastolic >= 90 and self.systolic < 120):
                self.bpStatus = "High BP Stage 2"
            elif self.systolic >= 180 or self.diastolic >= 120:
                self.bpStatus = "Hypertensive"
            else:
                self.bpStatus = "Unknown"

            # Heart heart
            # Based on table.
            if self.heartRate >= 60 and self.heartRate <= 90:
                self.heartStatus = "Average"
            elif self.heartRate < 60:
                self.heartStatus = "Low"
            elif self.heartRate > 90:
                self.heartStatus = "High"
            else:
                self.heartStatus = "Unknown"

            if self.bodyTemp!=0:
                self.bodyTempTB.setText(str(self.bodyTemp) + " C - " + self.bodyTempStatus)
            else:
                self.bodyTempTB.setText("Conecting to sensor...")

            self.heartRateTB.setText(str(self.heartRate) + " BPM - " + self.heartStatus)
            self.diastolicTB.setText(str(self.diastolic) + " mmHg")
            self.systolicTB.setText(str(self.systolic) + " mmHg")

            self.bpStatusTB.setText(self.bpStatus)

           

            self.deviceCoordinates.setText(str(latitudeCoordinate)+", "+str(longitudeCoordinate))

            if current_user_UID!="":
                vital_data = {
                    "time":"01-01-01 01-01-91",
                    "body_temp":"1",
                    "heart_rate":"2",
                    "systolic":"3",
                    "diastolic":"4",
                    "blood_pressure":"5",
                    "respiration_rate":"6",

                }
                timeNow = time.strftime("%Y-%m-%d %H-%M-%S")

                #print(vital_data)
                
                # Update data in firebase
                db.child("users").child(current_user_UID).child("uservitalshistory").child(timeNow).set(vital_data)

        except Exception as exp:
            print(str(exp))


    def viewECGButtonClicked(self):
        self.w = ApplicationWindow(self.bp_and_heartrate)
        self.w.show()
        self.close()
        

    def closeEvent(self, event):

        if self.timer.isActive():
            self.timer.stop()

        event.accept()


class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self, bp_and_heartrate):
        global sensorSerial
        
        super(ApplicationWindow, self).__init__()

        self.bp_and_heartrate=bp_and_heartrate

        sensorSerial.flushInput()
        sensorSerial.flushOutput()
         
        # 1. Window settings
        self.setGeometry(300, 300, 800, 480)
        self.setWindowTitle("ECG")
        # self.setWindowTitle("Matplotlib live plot in PyQt - example 2")
        self.frm = QtWidgets.QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: #eeeeec; }")
        self.lyt = QtWidgets.QVBoxLayout()
        self.frm.setLayout(self.lyt)
        self.setCentralWidget(self.frm)

        self.backButton = QtWidgets.QPushButton('BACK', self)
        self.backButton.resize(100, 32)
        self.backButton.move(610, 25)

        self.backButton.clicked.connect(self.backButtonClicked)

        # 2. Place the matplotlib figure
        self.myFig = MyFigureCanvas(x_len=50, y_range=[0, 800], interval=20)
        self.lyt.addWidget(self.myFig)

        
        # 3. Show
        # self.show()
        if inRPi:
            self.showFullScreen()
        else:
            self.show()

        return

    def backButtonClicked(self):

        try:
            self.myFig.event_source.stop()
            
            global sensorSerial
            sensorSerial.write("1\r\n".encode())

            print("1000 ms delay command sent.")
            
            self.mainWindow = Main(self.bp_and_heartrate)
            self.mainWindow.show()
            self.close()
            
        except Exception as exp:
            print(str(exp))

    def closeEvent(self, event):

   
        self.myFig.event_source.stop()
        event.accept()


class MyFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''

    def __init__(self, x_len: int, y_range: List, interval: int) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        global sensorSerial
        sensorSerial.write("2\r\n".encode())

        print("100 ms delay command sent.")
        
        FigureCanvas.__init__(self, mpl_fig.Figure())

        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        x = list(range(0, x_len))
        y = [0] * x_len

        # Store a figure and ax
        self._ax_ = self.figure.subplots()
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(x, y)

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_,
                                    fargs=(y,), interval=interval, blit=True)

        return


    def _update_canvas_(self, i, y) -> None:
        
        '''
        This function gets called regularly by the timer.

        '''

        global sensorSerial
        
        try:
 
            data = sensorSerial.readline().decode()
            print(data.split(",")[2])

            if "XFLAG" in data:
                self.ecgData = int(data.split(",")[2])
            else:
                self.ecgData = 0
        except Exception as exp:
            print(str(exp))
            self.ecgData=0
                
        y.append(int(self.ecgData))                 # Add new datapoint
        y = y[-self._x_len_:]                        # Truncate list _y_
        self._line_.set_ydata(y)
        
        return self._line_,

class timedMessageBox(QtWidgets.QMessageBox):
    def __init__(self, timeout, message):
        super(timedMessageBox, self).__init__()
        self.timeout = timeout
         
        self.setText('\n'.join((message, "")))

    def showEvent(self, event):
        QtCore.QTimer().singleShot(self.timeout*1000, self.close)
        super(timedMessageBox, self).showEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Login()
    w.show()
    app.exec_()
