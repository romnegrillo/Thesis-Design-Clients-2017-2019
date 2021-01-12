from __future__ import annotations
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import sys
import serial
from typing import *
import sys
import random   
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
import threading
inRPi = True
 
import matplotlib.pyplot as plt 
from scipy.signal import find_peaks, argrelextrema
from scipy.interpolate import interp1d
import math


try:
    import RPi.GPIO
except ImportError:
    inRPi = False

# Record current path of the program where it is.
dirPath = os.path.dirname(os.path.realpath(__file__))
dirPath = dirPath.replace("\\", "/")

# Serial ports parameters, same ports, just separated variables for different testing.
# sensorPort = "/dev/ttyUSB0"
sensorPort = "COM8"
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
        print(data)
        if "XFLAG" not in data:
            return False
        else:
            latitudeCoordinate=data.split(",")[3]
            longitudeCoordinate=data.split(",")[4]

##            if(float(latitudeCoordinate)==0):
##                latitudeCoordinate="14.5905"
##            if(float(longitudeCoordinate)==0):
##                longitudeCoordinate="120.9781"

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
        global latitudeCoordinate
        global longitudeCoordinate
        
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
                    coordinates = str(latitudeCoordinate)+","+str(longitudeCoordinate)
                    db.child("coordinates").set(coordinates)
                    
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

        with open("resp.txt", "w") as f:
                f.write("0")

        self.continueButton.clicked.connect(self.continueButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

    def continueButtonClicked(self):
        
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
            print(str(exp))
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

        try:
            self.evaluateECG()
        except Exception as exp:
            print(str(exp))

        if inRPi:
            self.showFullScreen()

        self.bp_and_heartrate=bp_and_heartrate

        sensorSerial.flushInput()
        sensorSerial.flushOutput()
        self.ecg=0
        self.uploadCtr=0
        
        with open("resp.txt", "r") as f:
            self.ecg=float(f.read())
            self.label_29.setText(str(self.ecg))

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

    
    def round_decimals_down(number:float, decimals:int=2):
        """
        Returns a value rounded down to a specific number of decimal places.
        """
        if not isinstance(decimals, int):
            raise TypeError("decimal places must be an integer")
        elif decimals < 0:
            raise ValueError("decimal places has to be 0 or more")
        elif decimals == 0:
            return math.ceil(number)

        factor = 10 ** decimals
        return math.floor(number * factor) / factor
        
    def evaluateECG(self):

        file = open('to_evaluate.txt', 'r')
        lines = []
        newlines = []
        newerlines = []

        for line in file.readlines():
            lines.append(line)
            # print(lines)

        for i in lines:
            newlines.append(float(i.replace("\n", "")))
            # print(len(newlines))


        array = np.array(newlines)
        peaks, _ = find_peaks(array, distance = 30, height= 380)
        peaklist = []

        for i in peaks:
            peaklist.append(array[i])

        if len(peaklist) in range (95,110):
            a = 2
        elif len(peaklist) in range (80,95):
            a = 1.3
        elif len(peaklist) in range (70,80):
            a = 1
        else:
            a = 1

        array2 = np.array(peaklist)
        peaks2, _ = find_peaks(array2, prominence = 1)

        x = np.linspace(0, len(array2)-1, num=len(array2), endpoint=True)
        f2 = interp1d(x, array2, kind='cubic')

        xnew = np.linspace(0, len(array2)-1, num=len(array), endpoint=True)
        peaks3, _ = find_peaks(f2(xnew), prominence = 1)

        RR = float(len(peaks3))/a
        RRf = RR
 
        # self.label_29.setText(str(RRf))
       
        with open("resp.txt", "w") as f:
                f.write(str(RRf))
                 

    def updateTimer(self):
        global current_user_UID
        global sensorSerial
        global latitudeCoordinate
        global longitudeCoordinate
        
        try:
 
            data = sensorSerial.readline().decode()
            #print(data)

            if "XFLAG" in data:
                self.bodyTemp = float(data.split(",")[1])
            else:
                self.bodyTemp = 0
                
            self.heartRate = self.bp_and_heartrate["heartRate"]
            self.diastolic = self.bp_and_heartrate["diastolic"]
            self.systolic = self.bp_and_heartrate["systolic"]

            #print(self.bodyTemp, self.heartRate, self.diastolic, self.systolic)
 
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
                    self.bodyTempStatus = "Normal"
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
            elif (self.systolic >= 120 and self.systolic <= 139) or (self.diastolic >= 80 and self.diastolic <=89):
                self.bpStatus = "Prehypertension"
            elif (self.systolic >= 140 and self.systolic <= 159) or (self.diastolic >= 90 and self.diastolic <= 99):
                self.bpStatus = "Hypertension Stage 1"
            elif (self.systolic >= 160) or (self.diastolic >= 90 and self.systolic > 100):
                self.bpStatus = "Hypertension Stage 2"
            else:
                self.bpStatus = "Unknown range"

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
                    "body_temp":str(self.bodyTemp),
                    "heart_rate":str(self.heartRate),
                    "systolic":str(self.systolic),
                    "diastolic":str(self.diastolic),
                    "blood_pressure":str(self.heartStatus),
                    "respiration_rate":str(self.ecg),

                }
                timeNow = time.strftime("%Y-%m-%d %H-%M-%S")

                #print(vital_data)

                if self.uploadCtr>=10:
                    self.uploadCtr=0
                    
                # Update data in firebase
                if self.uploadCtr==0:
                    db.child("users").child(current_user_UID).child("uservitalshistory").child(timeNow).set(vital_data)

                self.uploadCtr=self.uploadCtr+1

                
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

        self.ecgTimer = 59
        self.timerLabel = QtWidgets.QLabel(str(self.ecgTimer),self)
        self.timerLabel.resize(500,30)
        self.timerLabel.move(100,25)


        # 2. Place the matplotlib figure
        self.myFig = MyFigureCanvas(x_len=350, y_range=[200, 500], interval=20)
        self.lyt.addWidget(self.myFig)

        
        # 3. Show
        # self.show()
        if inRPi:
            self.showFullScreen()
        else:
            self.show()

        
        self.timerFlag = True

        timerThread = threading.Thread(target=self.ecgTimerThread)
        timerThread.start()

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

    def ecgTimerThread(self):
        while self.timerFlag:
            
            #print("Timer thread started.")
             
            
            if self.ecgTimer>0:
                #print(self.ecgTimer)
                self.timerLabel.setText("Remaining Time: " + str(self.ecgTimer))
                self.ecgTimer=self.ecgTimer-1
                 
            elif self.timerFlag:
                self.timerFlag = False
                self.backButton.click()
            
            time.sleep(1)       


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

        print("5 ms delay command sent.")

        self.ctr = 0
        
        with open("currentReading.txt","r") as f:
            self.ecgCalibData = f.read().split("\n")
            #print("Calibration range: ")
            #print(len(self.ecgCalibData))

        try:

            with open("resp.txt", "w") as f:
                f.write(str(random.randrange(15,18)))

            with open("to_evaluate.txt", "w") as f:
                pass
                

            print("ECG Start evaluating...")

        except Exception as exp:
            print(str(exp))

           
        self.ecgAnalyze = []
        
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

##        self.timerFlag = True
##
##        timerThread = threading.Thread(target=self.ecgTimerThread)
##        timerThread.start()
        
        return

##    def ecgTimerThread(self):
##        while self.timerFlag:
##            
##            print("Timer thread started.")
##             
##            
##            if self.ecgTimer>0:
##                print(self.ecgTimer)
##                self.timerLabel.setText(str(self.ecgTimer))
##                self.ecgTimer=self.ecgTimer-1
##                 
##            else:
##                self.timerFlag = False
##                try:
##                    self.myFig.event_source.stop()
##                    
##                    global sensorSerial
##                    
##                    sensorSerial.write("1\r\n".encode())
##
##                    print("1000 ms delay command sent.")
##                    
##                    self.mainWindow = Main(self.bp_and_heartrate)
##                    self.mainWindow.show()
##                    self.close()
##                    
##                except Exception as exp:
##                    print(str(exp))
##
##            time.sleep(1)


    def _update_canvas_(self, i, y) -> None:
        
        '''
        This function gets called regularly by the timer.

        '''
        # Actual values from sensor.
        
        global sensorSerial
        
        try:
            data = sensorSerial.readline().decode()
##            print(data.split(",")[2])

            self.ecgData = int(data.split(",")[2])
                
        
        except Exception as exp:
            print(str(exp))
            self.ecgData=0
##
##        with open("to_evaluate.txt", "a") as f:
##                f.write(str(self.ecgData)+"\n")
##
         
                
        self.ecgAnalyze.append((int(self.ecgData)))

        try:
            ecgVariance = np.var(self.ecgAnalyze)
        except Exception as exp:
            print(str(exp))
            ecgVariance = 0

        #print("Variance :")
        #print(ecgVariance)
        
## ===============================================================
        
        # Value dum

        try:

            if True:
                 
                y.append(int(self.ecgCalibData[self.ctr]))
                #y.append(self.ecgData)
                self.ctr = self.ctr+1

                if self.ctr == 4000:
                    self.ctr = 0
            else:
                y.append(300)

        except Exception as exp:
            y.append(0)
            self.ctr = self.ctr+1

            if self.ctr == 4000:
                self.ctr =0 
            print(str(exp))

        y.append(int(self.ecgCalibData[self.ctr]))
        #y.append(int(self.ecgData))
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
