import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


class GoogleSheetDatabase:

    def __init__(self, sheetName=None, keyFileNameJSON=None):
        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(keyFileNameJSON, self.scope)
        self.client = gspread.authorize(self.creds)

        self.sheetName = sheetName
        self.keyFileName = keyFileNameJSON

        self.connect()

    def connect(self):

        if self.sheetName is None and \
                self.keyFileName is None:
            return False
        else:
            self.userDB = self.client.open("test").get_worksheet(0)
            self.vitalDB = self.client.open("test").get_worksheet(1)
            self.symptomsDB = self.client.open("test").get_worksheet(2)

    def login(self, username=None, password=None):

        for d in self.userDB.get_all_records():
            if str(d["username"]) == username and \
               str(d["password"]) == password:
                #print("User exists!")

                if (d["type"] == "admin"):
                    return False
                else:
                    return True

        #print("User does not exists!")
        return False

    def recordData(self, vitalData):

        numOfRows = len(self.vitalDB.get_all_values())

        vitalData.insert(1, time.strftime(("%Y/%m/%d %H:%m")))

        self.vitalDB.insert_row(vitalData, numOfRows+1)

        return True

    def recordSymptoms(self, symptomsData):

        numOfRows = len(self.symptomsDB.get_all_values())

        # Check if username exists in the symptoms data.

        cell = None

        try:

            cell = self.symptomsDB.find(symptomsData[0])
        except gspread.CellNotFound:
            pass

        # Update if it exists
        if cell:
            for col, data in enumerate(symptomsData, 1):
                # print(col)
                self.symptomsDB.update_cell(cell.row, col, data)
        # Create if it does not
        else:
            self.symptomsDB.insert_row(symptomsData, numOfRows+1)

    def getUserDetails(self, username):

        for d in self.userDB.get_all_records():
            if str(d["username"]) == username:
                # print(d)
                return d

        return None

    def getDoctorNumber(self, username):
        for d in self.userDB.get_all_records():
            if d["username"] == username:
                return d["doctor_number"]


# For testing only.
if __name__ == "__main__":
    db = GoogleSheetDatabase("test", "database-f587d7d76e58.json")

    if(db.login("jasalas", "jasalas")):
        print("User exists!")
        print("+63"+str(db.getDoctorNumber("jasalas")))
    else:
        print("User does not exits.")


# Login phase.
# if(db.login("grayfullbuster", "icemake")):
##        print("User exists!")
##
# Getting userinfo for display in main.
##        userDetails = db.getUserDetails("grayfullbuster")
##
# if userDetails is not None:
# print(userDetails["first_name"])
# print(userDetails["middle_name"])
# print(userDetails["last_name"])
# print(userDetails["age"])
# print(userDetails["gender"])
# print(userDetails["address"])
##
# Logging symptoms.
##
# Logging sensor data.
##        logStatus = db.recordData(["grayfullbuster", 100, 200, 300, 400, 500, 600])
##
# else:
##        print("User does not exists!")
