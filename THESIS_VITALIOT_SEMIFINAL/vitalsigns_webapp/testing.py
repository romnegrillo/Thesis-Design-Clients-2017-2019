import pyrebase
from firebase_admin import credentials
import firebase_admin
import os

config = {
    "apiKey": "AIzaSyDGD8ewVOBVxl6O1r35Npy2RRw2dlWGdP8",
    "authDomain": "mapuavitalsignsdatabase.firebaseapp.com",
    "databaseURL": "https://mapuavitalsignsdatabase.firebaseio.com",
    "projectId": "mapuavitalsignsdatabase",
    "storageBucket": "mapuavitalsignsdatabase.appspot.com",
    "messagingSenderId": "582213066054",
    "appId": "1:582213066054:web:ab72ca16bf4849166bd947",
    "measurementId": "G-G5FC6W67QF",
    "serviceAccount": str(os.getcwd())+"/vitalsigns/static/vitalsigns/mapuavitalsignsdatabase-firebase-adminsdk-uphv7-0cff4fb849.json"

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
user = auth.sign_in_with_email_and_password("romnegrillo@gmail.com", "testing")
auth.refresh(user['refreshToken'])
print(db.child("users").child(user["localId"]).child("userinfo").get().val()["isAdmin"])

