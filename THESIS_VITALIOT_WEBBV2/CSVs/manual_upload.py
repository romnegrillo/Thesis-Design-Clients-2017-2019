import csv
import pandas as pd
import pyrebase
import time

import pyrebase
from firebase_admin import credentials
import firebase_admin

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
 
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

##with open("Argie Olalan.csv") as f:
##    data = f.readlines()
##    timeCol = []
##    for d in data:
##        timeCol.append(d.split(",")[0])
##
##    print(timeCol)
        

##with open("mark.lucero01.csv") as f:
##    data = csv.reader(f, delimiter=",")
##    for row in data:
##        print(row)
##

my_csv = pd.read_csv("Tristan.csv")

timeCol = my_csv.iloc[:,0]
bodyTempCol = my_csv.iloc[:,1]
heartRateCol = my_csv.iloc[:,2]
systolicCol = my_csv.iloc[:,3]
diastolicCol = my_csv.iloc[:,4]
bpCol = my_csv.iloc[:,5]
respCol = my_csv.iloc[:,6]


##        vital_data = {
##                    "time": "01-01-01 01-01-91",
##                    "body_temp": str(self.bodyTemp),
##                    "heart_rate": str(self.heartRate),
##                    "systolic": str(self.systolic),
##                    "diastolic": str(self.diastolic),
##                    "blood_pressure": str(self.heartStatus),
##                    "respiration_rate": "0",
##
##                }
##                timeNow = time.strftime("%Y-%m-%d %H-%M-%S")
##
##                # print(vital_data)
##
##                # Update data in firebase
##                db.child("users").child(current_user_UID).child(
##                    "uservitalshistory").child(timeNow).set(vital_data)
##


for t,bt,h,s,d,b,r in zip(timeCol,bodyTempCol,heartRateCol,systolicCol,diastolicCol,bpCol,respCol):
   #print(t,b,h,s,d,b,r)

    vital_data = {
                "time": str(t),
                "body_temp": str(bt),
                "heart_rate": str(h),
                "systolic": str(s),
                "diastolic": str(d),
                "blood_pressure": str(b),
                "respiration_rate": str(r),

            }

    print(vital_data)
    #db.child("users").child("jy8Y0BtyHHaGZjUs7adpOulLgRo1").child("uservitalshistory").child(str(t)).set(vital_data)
    #time.sleep(1)
