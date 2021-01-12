from __future__ import annotations
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import sys
import sheet_database
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


from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.qt_compat import QtCore, QtWidgets
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
import numpy as np
import sys

inRPi = True

try:
    import RPi.GPIO
except ImportError:
    inRPi = False

# Record current path of the program where it is.
dirPath = os.path.dirname(os.path.realpath(__file__))
dirPath = dirPath.replace("\\", "/")

# Serial ports parameters, same ports, just separated variables for different testing.
tempPort = "/dev/ttyUSB0"
ecgPortName = "/dev/ttyUSB0"

# Google sheets parameters.

sheetName = "test"
jsonFileName = dirPath+"/database-f587d7d76e58.json"
isConnected = False

try:
    db = sheet_database.GoogleSheetDatabase(sheetName, jsonFileName)
    isConnected = True
except Exception as exp:
    print(str(exp))
    print("You are not connected to a network.")


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

        if not isConnected:

            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Error")
            message.setText(
                "You are not connected to the database, please check your internet connection.")
            message.setIcon(QtWidgets.QMessageBox.Information)

            message.exec_()
            return

        username = self.usernameTB.text()
        password = self.passTB.text()

        if username and password:
            try:

                print("Logging in.")
                if(db.login(username, password)):
                    self.userWindow = User(username)
                    self.userWindow.show()
                    self.hide()
                else:
                    message = QtWidgets.QMessageBox()
                    message.setWindowTitle("Error")
                    message.setText("Invalid username and/or password.")
                    message.setIcon(QtWidgets.QMessageBox.Critical)

                    message.exec_()
            except Exception as exp:
                print(str(exp))

    def guestButtonClicked(self):

        message = QtWidgets.QMessageBox()
        message.setWindowTitle("Warning")
        message.setText("You won't save any data in guest mode, is that okay?")
        message.setIcon(QtWidgets.QMessageBox.Question)
        message.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        choice = message.exec_()

        if choice == QtWidgets.QMessageBox.Ok:
            self.userWindow = User()
            self.userWindow.show()
            self.hide()

    def exitButtonClicked(self):
        self.hide()


class User(QtWidgets.QMainWindow):

    def __init__(self, username=None):
        super(User, self).__init__()
        loadUi(dirPath+"/vitalsigns_user.ui", self)
        self.counterNext = 0

        if inRPi:
            self.showFullScreen()

        self.username = username

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
                self.symptomsWindow = Symptoms(self.username)
                self.symptomsWindow.show()
                self.hide()
        except Exception as exp:
            print(str(exp))

    def logoutButtonClicked(self):

        if self.counterNext == 0:
            self.loginWindow = Login()
            self.loginWindow.show()
            self.hide()
            self.counterNext = self.counterNext + 1

        elif self.counterNext == 1:
            self.label_2.setText("In the next window, you will be asked to answer a form indicating\nsymptoms you are experiencing.\n\nNext is use the arm blood pressure monitor to know your blood pressure\nand heart rate.\n\nThen in the last part you have to put your finger through\nthe body temperature sensor.\n\nTo view your respiratory rate, click ECG button in the last window and\nwait for it to stabilize then go back to the previous window to view respiratory rate. ")
            self.label_2.setStyleSheet(
                "background-color: qconicalgradient(cx:1, cy:1, angle:0, stop:0 rgba(1, 255, 72, 255), stop:1 rgba(255, 255, 255, 255));")
            self.counterNext = self.counterNext-1


class Symptoms(QtWidgets.QMainWindow):

    def __init__(self, username=None):
        super(Symptoms, self).__init__()
        loadUi(dirPath+"/vitalsigns_symptoms.ui", self)

        if inRPi:
            self.showFullScreen()

        self.username = username

        self.addSeverity()
        self.continueButton.clicked.connect(self.continueButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

    def addSeverity(self):
        severity = list(range(1, 11))
        severity = [str(i) for i in severity]

        self.combo1.addItems(severity)
        self.combo2.addItems(severity)
        self.combo3.addItems(severity)
        self.combo4.addItems(severity)
        self.combo5.addItems(severity)
        self.combo6.addItems(severity)
        self.combo7.addItems(severity)
        self.combo8.addItems(severity)
        self.combo9.addItems(severity)
        self.combo10.addItems(severity)
        self.combo11.addItems(severity)

    def continueButtonClicked(self):

        try:
            # Update symptoms in user profile

            tab1 = [
                self.cb01,
                self.cb02,
                self.cb03,
                self.cb04,
                self.cb05,
                self.cb06,
                self.cb07,
                self.cb08,
                self.cb09,
                self.cb11,
                self.cb12,
                self.cb13,
                self.cb14,
                self.cb15,
                self.cb16,
                self.cb17,
            ]

            tab2 = [
                self.cb18,
                self.cb19,
                self.cb20,
                self.cb21,
                self.cb22,
                self.cb23,
                self.cb24,
                self.cb25,
                self.cb26,
                self.cb27,
                self.cb28,
                self.cb29,
                self.cb30,
                self.cb31,
                self.cb32,
                self.cb33,
                self.cb34,
                self.cb35,
            ]

            tab3 = [
                self.cb36,
                self.cb37,
                self.cb38,
                self.cb39,
                self.cb40,
                self.cb41,
                self.cb42,
                self.cb43,
                self.cb44,
                self.cb45,
                self.cb46,
                self.cb47,
                self.cb48,
                self.cb49,
                self.cb50,
                self.cb51,
            ]

            tab4 = [
                self.cb52,
                self.cb53,
                self.cb54,
                self.cb55,
                self.cb56,
                self.cb57,
                self.cb58,
                self.cb59,
                self.cb60,
                self.cb61,
                self.cb62,
                self.cb63,
                self.cb64,
                self.cb65,
                self.cb66,
                self.cb67,
                self.cb68,
            ]

            tab5 = [
                self.cb69,
                self.cb70,
                self.cb71,
                self.cb72,
                self.cb73,
                self.cb74,
                self.cb75,
                self.cb76,
                self.cb77,
                self.cb78,
                self.cb79,
                self.cb80,
                self.cb81,
                self.cb82,
                self.cb83,
                self.cb84,
                self.cb85,
                self.cb86,
                self.cb87,
            ]

            tab6 = [
                self.cb88,
                self.cb89,
                self.cb90,
                self.cb91,
                self.cb92,
                self.cb93,
                self.cb94,
                self.cb95,
                self.cb96,
                self.cb97,
                self.cb98,
                self.cb99,
                self.cb100,
                self.cb101,
                self.cb102,
                self.cb103,
                self.cb104,
                self.cb105,
                self.cb106,
                self.cb107,
                self.cb108,
                self.cb109,
                self.cb110,
            ]

            tab7 = [
                self.cb111,
                self.cb112,
                self.cb113,
                self.cb114,
                self.cb115,
                self.cb116,
                self.cb117,
                self.cb118,
                self.cb119,
                self.cb120,
                self.cb121,
                self.cb122,
                self.cb123,
                self.cb124,
                self.cb125,
            ]

            tab8 = [
                self.cb126,
                self.cb127,
                self.cb128,
                self.cb129,
                self.cb130,
                self.cb131,
                self.cb132,
                self.cb133,
                self.cb134,
                self.cb135,
                self.cb136,
                self.cb137,
                self.cb138,
                self.cb139,
                self.cb140,
                self.cb141,
                self.cb142,
                self.cb143,
                self.cb144,
                self.cb145,
            ]

            tab9 = [
                self.cb146,
                self.cb147,
                self.cb148,
                self.cb149,
                self.cb150,
                self.cb151,
                self.cb152,
                self.cb153,
                self.cb154,
                self.cb155,
                self.cb156,
                self.cb157,
                self.cb158,
                self.cb159,
                self.cb160,
                self.cb161,
                self.cb162,
                self.cb163,
                self.cb164,
                self.cb165,
            ]

            tab10 = [
                self.cb166,
                self.cb167,
                self.cb168,
                self.cb169,
                self.cb170,
                self.cb171,
                self.cb172,
                self.cb173,
                self.cb174,
                self.cb175,
                self.cb176,
                self.cb177,
                self.cb178,
                self.cb179,
                self.cb180,
                self.cb181,
            ]

            tab11 = [
                self.cb182,
                self.cb183,
                self.cb184,
                self.cb185,
                self.cb186,
                self.cb187,
                self.cb188,
                self.cb189,
                self.cb190,
                self.cb191,
                self.cb192,
                self.cb193,
                self.cb194,
            ]

            symptoms = {
                "Chest Pain": [],
                "Cough": [],
                "Diarrhea": [],
                "Swallowing": [],
                "Dizziness": [],
                "Headaches": [],
                "Palpitations": [],
                "Nasal Congestion": [],
                "Nausea": [],
                "Shorteness of Breath": [],
                "Wheezing": [],

            }

            cbList = [
                self.combo1,
                self.combo2,
                self.combo3,
                self.combo4,
                self.combo5,
                self.combo6,
                self.combo7,
                self.combo8,
                self.combo9,
                self.combo10,
                self.combo11
            ]

            for symp, cbList in zip(symptoms, cbList):
                symptoms[symp].append("Severity: " + cbList.currentText())

            for t1 in tab1:
                # print(t1.isChecked())
                if t1.isChecked():
                    symptoms["Chest Pain"].append(t1.text())

            for t2 in tab2:
                # print(t1.isChecked())
                if t2.isChecked():
                    symptoms["Cough"].append(t2.text())

            for t3 in tab3:
                # print(t1.isChecked())
                if t3.isChecked():
                    symptoms["Diarrhea"].append(t3.text())

            for t4 in tab4:
                # print(t1.isChecked())
                if t4.isChecked():
                    symptoms["Swallowing"].append(t4.text())

            for t5 in tab5:
                # print(t1.isChecked())
                if t5.isChecked():
                    symptoms["Dizziness"].append(t5.text())

            for t6 in tab6:
                # print(t1.isChecked())
                if t6.isChecked():
                    symptoms["Headaches"].append(t6.text())

            for t7 in tab7:
                # print(t1.isChecked())
                if t7.isChecked():
                    symptoms["Palpitations"].append(t7.text())

            for t8 in tab8:
                # print(t1.isChecked())
                if t8.isChecked():
                    symptoms["Nasal Congestion"].append(t8.text())

            for t9 in tab9:
                # print(t1.isChecked())
                if t9.isChecked():
                    symptoms["Nausea"].append(t9.text())

            for t10 in tab10:
                # print(t1.isChecked())
                if t10.isChecked():
                    symptoms["Shorteness of Breath"].append(t10.text())

            for t11 in tab11:
                # print(t1.isChecked())
                if t11.isChecked():
                    symptoms["Wheezing"].append(t11.text())

            self.symptoms = symptoms

            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Are you sure?")
            message.setText("Are you sure you filled all symptoms you are experiencing?")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

            choice = message.exec_()

            if choice == QtWidgets.QMessageBox.Ok:

                if True:
                    print(symptoms["Chest Pain"])
                    print(symptoms["Cough"])
                    print(symptoms["Diarrhea"])
                    print(symptoms["Swallowing"])
                    print(symptoms["Dizziness"])
                    print(symptoms["Headaches"])
                    print(symptoms["Palpitations"])
                    print(symptoms["Nasal Congestion"])
                    print(symptoms["Nausea"])
                    print(symptoms["Shorteness of Breath"])
                    print(symptoms["Wheezing"])

                if isConnected and self.username is not None:
                    symptomsData = []
                    symptomsData.append(self.username)

                    for key, value in symptoms.items():
                        if(len(value) != 0):
                            symptomsData.append(",\n".join(value))
                        else:
                            symptomsData.append("None")
                    # print("debug")
                    print(symptomsData)

                    try:
                        db.recordSymptoms(symptomsData)
                    except:
                        message = QtWidgets.QMessageBox()
                        message.setWindowTitle("Error")
                        message.setText(
                            "You are not connected to the database, please check your internet connection.")
                        message.setIcon(QtWidgets.QMessageBox.Information)

                        message.exec_()
                        return

                self.bpWindow = BloodPressure(self.username, self.symptoms)
                self.bpWindow.show()
                self.hide()

        except Exception as exp:
            print(str(exp))

    def backButtonClicked(self):
        self.userWindow = User(self.username)
        self.userWindow.show()
        self.hide()

    def getSymptomsData(self):
        pass


class BloodPressure(QtWidgets.QMainWindow):

    def __init__(self, username=None, symptoms=None):
        super(BloodPressure, self).__init__()
        loadUi(dirPath+"/vitalsigns_bloodpressure.ui", self)

        if inRPi:
            self.showFullScreen()

        self.username = username
        self.symptoms = symptoms

        self.continueButton.clicked.connect(self.continueButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

    def continueButtonClicked(self):

        # Update bp and heart rate in next window.
        data = self.getData()

        try:
            self.mainWindow = Main(username=self.username,
                                   systolic=data["systolic"], diastolic=data["diastolic"], heartRate=data["heartRate"],
                                   symptoms=self.symptoms)
            self.mainWindow.show()
            self.hide()
        except Exception as exp:
            print(str(exp))

    def backButtonClicked(self):
        self.symptomsWindow = Symptoms(self.username)
        self.symptomsWindow.show()
        self.hide()

    def getData(self):

        try:
            systolic = round(float(self.sysTB.text()), 2)
            diastolic = round(float(self.diaTB.text()), 2)
            heartRate = round(float(self.heartTB.text()), 2)

            data = {
                "systolic": systolic,
                "diastolic": diastolic,
                "heartRate": heartRate,
            }

            return data
        except ValueError:
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Error")
            message.setText("Invalid input detected.\nPlease input a valid data.")
            message.exec_()


class Main(QtWidgets.QMainWindow):

    def __init__(self, systolic, diastolic, heartRate, username=None, symptoms=None):
        super(Main, self).__init__()
        loadUi(dirPath+"/vitalsigns_main.ui", self)

        if inRPi:
            self.showFullScreen()

        self.username = username
        self.systolic = systolic
        self.diastolic = diastolic
        self.heartRate = heartRate
        self.symptoms = symptoms

        self.flag = 0

        print(self.systolic, self.diastolic, self.heartRate)

        print("Init data.")
        self.initData(username, symptoms)
        self.initPort()
        print("Done intit data.")

        self.backButton.clicked.connect(self.backButtonClicked)
        self.viewECGButton.clicked.connect(self.viewECGButtonClicked)
        self.callButton.clicked.connect(self.callButtonClicked)
        self.isECGOpen = False

    def initData(self, username, symptoms):

        if inRPi:
            self.showFullScreen()

        if username:
            self.username = username

            userDetails = db.getUserDetails(self.username)
            self.userAge = int(userDetails["age"])

            if userDetails is not None:
                print(userDetails["first_name"])
                print(userDetails["middle_name"])
                print(userDetails["last_name"])
                print(userDetails["age"])
                print(userDetails["gender"])
                print(userDetails["address"])

                fullName = str(userDetails["first_name"]) + " " + \
                    str(userDetails["middle_name"]) + " " + \
                    str(userDetails["last_name"])

                self.nameTB.setText(fullName)
                self.ageTB.setText(str(userDetails["age"]))
                self.sexTB.setText(str(userDetails["gender"]))
                self.locationTB.setText(str(userDetails["address"]))

                self.doctorNumber = "+63" + str(userDetails["doctor_number"])
        else:
            self.username = None
            self.nameTB.setText("Guest")

        # print(len(symptoms))
        self.symptomsTE.clear()

        print(symptoms)

        if symptoms:

            for category, symptom in symptoms.items():

                self.symptomsTE.append(str(category))

                for s in symptom:
                    self.symptomsTE.append("- " + str(s))
                if len(symptom) == 0:
                    self.symptomsTE.append("- None selected.")

                self.symptomsTE.append("\n")

            # self.symptomsTE.append("\n - Nothing follows.")

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(1)
        self.ctr = 0

    def initPort(self):
        self.tempPort = serial.Serial(port=tempPort, baudrate=9600)
        self.tempPort.write("0".encode())
        # self.ecgPort = serial.Serial(port=ecgPortName, baudrate=9600)

    def closePort(self):
        if self.tempPort.isOpen():
            self.tempPort.close()

        # if self.ecgPort.isOpen():
        #    self.ecgPort.close()

    def callButtonClicked(self):

        try:
            pass
            if self.username is not None:
                if self.tempPort.isOpen():
                    # Get registered doctor number.
                    # Send call signal to Arduino
                    print(self.doctor_number)
                    toSend = "2," + self.doctor_number
                    self.tempPort.write(toSend.encode())

        except Exception as exp:
            print(str(exp))

    def backButtonClicked(self):
        pass

        if self.timer.isActive():
            self.timer.stop()

        self.closePort()

        self.bpWindow = BloodPressure(self.username, symptoms=self.symptoms)
        self.bpWindow.show()
        self.hide()

    def updateTimer(self):
        # print("Timer")

        tempData = self.readPorts()

        if tempData == 0:
            self.bodyTempTB.setText("Warming up sensor...")
            return

        self.bodyTemp = tempData
        self.respirationRate = 0

        print(self.bodyTemp, self.systolic, self.diastolic, self.heartRate)

        # Body Temp
        # For babies, children, adults:
        # Based on table
        self.bodyTempStatus = "Normal"

        if self.username is None:
            self.userAge = 25

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

        self.bodyTempTB.setText(str(self.bodyTemp) + " C - " + self.bodyTempStatus)
        self.heartRateTB.setText(str(self.heartRate) + " BPM - " + self.heartStatus)
        self.diastolicTB.setText(str(self.diastolic) + " mmHg")
        self.systolicTB.setText(str(self.systolic) + " mmHg")
        self.bpStatusTB.setText(self.bpStatus)

        # Update data in user profile

        if isConnected and self.username is not None:
            pass

            # Format: (time is already included in the class), body_temperature, heartRate, bp, diastolic, systolic, respiration_rate
            if self.ctr >= 5 and self.bodyTemp != 0:
                logStatus = db.recordData([str(self.username), self.bodyTemp, self.heartRate,
                                           self.diastolic, self.systolic, self.bpStatus, self.respirationRate])
                self.ctr = 0

        self.ctr = self.ctr+1

    def readPorts(self):

        # Temperature and heart rate port.

        try:
            tempPortData = self.tempPort.readline()
            tempPortData = tempPortData.decode()

            if tempPortData[0] == "X":  # Find this pattern.

                if self.flag == 0:
                    self.tempPort.write("0".encode())
                    self.flag = 1

                tempPortData = tempPortData.split(",")

                body_temperature = float(tempPortData[1])

                # print(body_temperature)

                return body_temperature
        except Exception as exp:
            print(str(exp))

        return 0

        # ECG port is moved in the real time graph window.

        # ecgPortData = self.ecgPort.readline()
        # ecgPortData = ecgPortData.decode()

        # print(ecgPortData)

    def viewECGButtonClicked(self):
        try:
            pass

            # if self.timer.isActive():
            #     self.timer.stop()

            # if not self.isECGOpen:
            #
            #     self.app = ApplicationWindow(self.username)
            #     self.app.show()
            #
            #     self.isECGOpen = True

            # Open ecgGraph.py

            if not self.isECGOpen:

                self.closePort()

                if self.timer.isActive():
                    self.timer.stop()

                self.w = ApplicationWindow(username=self.username, systolic=self.systolic,
                                           diastolic=self.diastolic, heartRate=self.heartRate,
                                           symptoms=self.symptoms)
                self.w.show()
                self.hide()

        except Exception as exp:
            print(str(exp))

    def closeEvent(self, event):

        if self.timer.isActive():
            self.timer.stop()

        self.closePort()

        # self.closePort()
        event.accept()


class ApplicationWindow(QtWidgets.QMainWindow):
    '''
    The PyQt5 main window.

    '''

    def __init__(self, systolic, diastolic, heartRate, symptoms=None, username=None):
        super(ApplicationWindow, self).__init__()

        self.username = username
        self.systolic = systolic
        self.diastolic = diastolic
        self.heartRate = heartRate
        self.symptoms = symptoms

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
        self.myFig = MyFigureCanvas(x_len=50, y_range=[-100, 1023], interval=20)
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
            self.myFig.closeECGPort()
            self.mainWindow = Main(username=self.username,
                                   systolic=self.systolic, diastolic=self.diastolic, heartRate=self.heartRate,
                                   symptoms=self.symptoms)
            self.mainWindow.show()
            self.hide()
        except Exception as exp:
            print(str(exp))

    def closeEvent(self, event):

        print("Graph closed.")
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
        FigureCanvas.__init__(self, mpl_fig.Figure())
        self.flag = 0
        self.openECGPort()

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

    def openECGPort(self):
        self.ecgPort = serial.Serial(port=ecgPortName, baudrate=9600)
        self.ecgDataList = []

    def closeECGPort(self):
        print("Port closing....")
        if self.ecgPort.isOpen():
            print("Port closed.")
            self.ecgPort.close()

    def readECGPort(self):
        pass

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        try:
            self.ecgReading = self.ecgPort.readline()
            self.ecgReading = self.ecgReading.decode()

            if self.ecgReading[0] == "X":  # Find this pattern.
                if self.flag == 0:
                    self.ecgPort.write("1".encode())
                    self.flag = 1
                self.ecgReading = float(self.ecgReading.split(",")[2])

                print(self.ecgReading)

                y.append(self.ecgReading)     # Add new datapoint
                y = y[-self._x_len_:]                        # Truncate list _y_
                self._line_.set_ydata(y)
            else:
                pass
        except Exception as exp:
            print(str(exp))

        # time.sleep(1)

        return self._line_,


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Login()
    w.show()
    app.exec_()
