from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi
import sys
import pyrebase
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import urllib.request
import time
import socket

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

AIRCON_RELAY = 20
HUMIDIFIER_RELAY = 21

aircon_flag = 0
humidifier_flag =0

firebaseConfig = {
    "apiKey": "AIzaSyBFvKEuq5DawSRMC74x1ZQSZun-09lPP3w",
    "authDomain": "thesissmartplug.firebaseapp.com",
    "databaseURL": "https://thesissmartplug.firebaseio.com",
    "projectId": "thesissmartplug",
    "storageBucket": "thesissmartplug.appspot.com",
    "messagingSenderId": "406194003414",
    "appId": "1:406194003414:web:d74cbeafbfc02663d69877"
}

GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD

GPIO.setup(AIRCON_RELAY, GPIO.OUT) # set a port/pin as an output  
GPIO.setup(HUMIDIFIER_RELAY, GPIO.OUT) # set a port/pin as an output  

GPIO.output(AIRCON_RELAY, 0)       # set port/pin value to 0/GPIO.LOW/False  
GPIO.output(HUMIDIFIER_RELAY, 0)       # set port/pin value to 0/GPIO.LOW/False  


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("mainwindow.ui", self)
        

        try:
            self.initStatus()
        except Exception as exp:
            print(str(exp))

    def initStatus(self):
        self.cloudStatusLabel.setStyleSheet("color: red;")
        self.manualRadioButton.setChecked(True)

        self.humidity = 0
        self.temperature = 0
        self.mode = "MANUAL"
        self.aircon = "OFF"
        self.humidifier = "OFF"

        if self.connectToTheCloud():
            self.connected = True
            self.startTime = time.time()

            stream_mode = self.db.child("mode").stream(self.stream_mode_handler)
            stream_aircon = self.db.child("aircon").stream(self.stream_aircon_handler)
            stream_humidifier = self.db.child("humidifier").stream(self.stream_humidifier_handler)

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update)
            self.timer.start(1000)
        else:
            print("Cannot connect to the internet.")

    def connectToTheCloud(self):
        try:
            print("Checking firebase config...")
            self.firebase = pyrebase.initialize_app(firebaseConfig)
            self.db = self.firebase.database()

            while not self.ping():
                print("Connecting...")

            self.cloudStatusLabel.setStyleSheet("color: green;")
            self.cloudStatusLabel.setText("Connected")
            print("Connected.")

            return True
        except Exception as exp:
            print(str(exp))

        return False

    def ping(self):
            try:
                # connect to the host -- tells us if the host is actually
                # reachable
                socket.create_connection(("www.google.com", 80))
                return True
            except Exception as exp:
                print(str(exp))
                
            return False

    def update(self):

        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
         
        if humidity is not None and temperature is not None:

            try:
                self.temperature = round(temperature,2)
                self.humidity = round(humidity,2)

                T = self.temperature
                RH = self.humidity
                
                T = int((T * 9/5) + 32)
                HI = 0.5 * (T + 61.0 + ((T-68.0)*1.2) + (RH*0.094)) 
                HI = (T - 32) * (5/9)
                HI = round(HI,2)
                
                
                self.heatIndex=HI
                
            except Exception as exp:
                print(str(exp))
                self.temperature = 0
                self.humidity = 0
                self.heatIndex=0
                 
        else:
            self.temperature = 0
            self.humidity = 0
            self.heatIndex=0
             
            

        if self.mode == "MANUAL":
            print("Manual mode running...")
            self.manualRadioButton.setChecked(True)
            self.automaticRadioButton.setChecked(False)
            
            aircon_flag = 0
            humidifier_flag =0
             

            # Turn relay on and off here base from database values.

            if self.aircon == "ON":
                GPIO.output(AIRCON_RELAY, 1)       # set port/pin value to 0/GPIO.LOW/False  
            else:
                GPIO.output(AIRCON_RELAY, 0)       # set port/pin value to 0/GPIO.LOW/False  


            if self.humidifier == "ON":
                GPIO.output(HUMIDIFIER_RELAY, 1)       # set port/pin value to 0/GPIO.LOW/False  
            else:
                GPIO.output(HUMIDIFIER_RELAY, 0)       # set port/pin value to 0/GPIO.LOW/False  
            
        else:

            # Turn relay on and off here base on data conditions.

            print("Auto mode running...")

            
            self.manualRadioButton.setChecked(False)
            self.automaticRadioButton.setChecked(True)
            self.currentTime = time.time()

            if (self.currentTime - self.startTime) >= 3600:
                aircon_flag=0
                humidifier_flag=0
             
            
        
             # If on, don't turn off until one hour (aircon and humidifier)
            if self.temperature <=25 and aircon_flag!=1:
                GPIO.output(AIRCON_RELAY, 0)
                self.db.update({"aircon":"OFF"})
            else:
                GPIO.output(AIRCON_RELAY, 1)
                aircon_flag=1
                self.db.update({"aircon":"ON"})

            
            if self.humidity <= 55 and humidifier_flag!=1:
                GPIO.output(HUMIDIFIER_RELAY, 0)
                self.db.update({"humidifier":"OFF"})
            else:
                GPIO.output(HUMIDIFIER_RELAY, 1)
                humidifier_flag=1
                self.db.update({"humidifier":"ON"})
                    
        self.tempLabel.setText(str(self.temperature) + " C")
        self.humidLabel.setText(str(self.humidity) + " %")
        #self.heatIndexLabel.setText(str(self.heatIndex) + " %")

        self.airconPlugLabel.setText(str(self.aircon))
        self.humidifierPlugLabel.setText(str(self.humidifier))

        try:

            self.db.update({"temperature":str(self.temperature)})
            
            self.db.update({"humidity":str(self.humidity)})
            
            #self.db.update({"heat_index":str(self.heatIndex)})
            
        except Exception as exp:
            print(str(exp))

    def stream_mode_handler(self, message):
        self.mode = message["data"]

    def stream_aircon_handler(self, message):
        self.aircon = message["data"]

    def stream_humidifier_handler(self, message):
        self.humidifier = message["data"]

    def closeEvent(self, event):
        if self.timer.isActive():
            
            self.timer.stop()
        GPIO.cleanup()
        event.accept()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
