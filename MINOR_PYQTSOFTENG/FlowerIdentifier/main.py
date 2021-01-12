from PyQt5 import QtWidgets
import loginwindow
import identifywindow
import adminwindow
import pymysql
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
import numpy as np
import cv2
import os
from rgbhistogram import RGBHistogram
from tkinter import Tk, messagebox
import shutil

class LoginWindow(QtWidgets.QMainWindow, loginwindow.Ui_MainWindow):

    root=Tk()
    root.withdraw()

    def __init__(self, parent=None):
        super(LoginWindow,self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.loginButton)
        self.pushButton_2.clicked.connect(self.identifyButton)

    def loginButton(self):

        username=self.lineEdit.text()
        password=self.lineEdit_2.text()

        if username and password and not username.isspace() and not password.isspace():

            conn=pymysql.connect(host="localhost", user="root", password="toor", db="flower")

            with conn.cursor() as curr:
                query="SELECT * FROM flower.users WHERE `Username`=%s AND `Password`=%s"
                curr.execute(query,(username,password))
                result=curr.fetchall()

                if len(result):
                    print("Account Exists!")
                    self.dialog=AdminWindow()
                    self.hide()
                    self.dialog.show()
                else:
                    messagebox.showinfo("Error", "Invalid username and/or password!")

            conn.close()

        else:
            messagebox.showinfo("Error", "All fields are required!")


    def identifyButton(self):
        self.dialog=IdentifyWindow()
        self.close()
        self.dialog.show()

class IdentifyWindow(QtWidgets.QMainWindow, identifywindow.Ui_MainWindow):

    def __init__(self, parent=None):
        super(IdentifyWindow,self).__init__(parent)
        self.setupUi(self)

        self.backB.clicked.connect(self.backButton)
        self.classifyB.clicked.connect(self.classifyButton)
        self.selectFileB.clicked.connect(self.selFileButton)

    def backButton(self):
        self.dialog=LoginWindow()
        self.hide()
        self.dialog.show()

    def selFileButton(self):

        try:
            dlg = QtWidgets.QFileDialog()
            dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            dlg.setNameFilters(["Images (*.png *.jpg)"])


            if dlg.exec_():

                fileName = dlg.selectedFiles()
                print(fileName)
                self.selectFileTB.setText(fileName[0])
                targetdir="current/{}".format("tempimage.png")
                print(targetdir)
                shutil.copy(fileName[0],targetdir)

                origImage=cv2.imread("current/tempimage.png")
                tempImage=cv2.imread("images/image_sunflower_0108.png")
                shape=tempImage.shape

                resize=cv2.resize(origImage, (shape[1],shape[0]),cv2.INTER_AREA)
                cv2.imwrite("current/tempimage.png", resize)
                newImg=cv2.imread("current/tempimage.png")
                #cv2.imshow("Testing Purposes", newImg)

                relPath = "current/tempimage.png"
                toBG = "#graphicsView\n" + \
                       "{\n" + \
                       " border-image: url(\"{0}\");\n".format("current/tempimage.png") + \
                       "\n" + \
                       "}"

                #print(toBG)
                self.graphicsView.setStyleSheet(toBG)

        except:
            print("Invalid image selected!")

    def classifyButton(self):

        try:
            if self.selectFileTB:

                data = []
                target = []

                imagePaths = os.getcwd() + "\\images"
                maskPaths = os.getcwd() + "\\masks"

                #imagePaths = os.listdir(imagePaths)
                #maskPaths = os.listdir(maskPaths)

                imagePaths=[]
                maskPaths=[]

                conn = pymysql.connect(host="localhost", user="root", password="toor", db="flower")

                with conn.cursor() as curr:
                    query = "SELECT `Flower Image Path` FROM flower.flowerpath;"
                    curr.execute(query)
                    result=curr.fetchall()

                    for item in result:
                        print(item[0])
                        imagePaths.append(item[0])

                    query = "SELECT `Mask Image Path` FROM flower.flowerpath;"
                    curr.execute(query)
                    result = curr.fetchall()

                    for item in result:
                        maskPaths.append(item[0])

                conn.close()


                desc = RGBHistogram([8, 8, 8])

                for (imagePath, maskPath) in zip(imagePaths, maskPaths):
                    image = cv2.imread(imagePath)
                    mask = cv2.imread(maskPath)
                    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

                    features = desc.describe(image, mask)

                    data.append(features)
                    target.append(imagePath.split("_")[-2])

                targetNames = np.unique(target)
                le = LabelEncoder()
                target = le.fit_transform(target)

                (trainData, testData, trainTarget, testTarget) = train_test_split(data, target,
                                                                                  test_size=0.3, random_state=42)
                model = RandomForestClassifier(n_estimators=25, random_state=84)
                model.fit(trainData, trainTarget)


                imagePath = "current/tempimage.png"
                print(imagePath)
                # maskPath="masks/"+maskPaths[1]

                image = cv2.imread(imagePath)
                # mask=cv2.imread(maskPath)
                # mask=cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

                features = desc.describe(image)
                print(trainTarget)
                flower = le.inverse_transform(model.predict([features]))[0]
                print(classification_report(testTarget, model.predict(testData),
                target_names = targetNames))

                prob=model.predict_proba([features])
                print(prob)

                highest=max(prob[0])
                print(highest)

                print("I think this flower is: {}".format(flower.upper()))
                self.label_2.setText("This flower is {1}% {0}".format(flower.upper(),float(highest)*100))
            else:
                messagebox("Error", "Browse for image!")
        except:
            messagebox("Error", "Invalid image!")

class AdminWindow(QtWidgets.QMainWindow, adminwindow.Ui_MainWindow):

    def __init__(self, parent=None):
        super(AdminWindow,self).__init__(parent)
        self.setupUi(self)
        self.initList()
        self.logoutB.clicked.connect(self.logoutButton)
        self.addUserB.clicked.connect(self.addUserButton)
        self.deleteUserB.clicked.connect(self.deleteUserButton)
        self.browseB.clicked.connect(self.browseButton)
        self.addImgB.clicked.connect(self.addImageButton)

    def logoutButton(self):
        self.dialog=LoginWindow()
        self.hide()
        self.dialog.show()

    def browseButton(self):

        try:
            dlg = QtWidgets.QFileDialog()
            dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            dlg.setNameFilters(["Images (*.png *.jpg)"])

            if dlg.exec_():
                fileName = dlg.selectedFiles()
                self.lineEdit_4.setText(fileName[0])
                print(fileName)

                targetdir = "currentupload/{}".format("tempimage.png")
                print(targetdir)
                shutil.copy(fileName[0], targetdir)

                origImage = cv2.imread("currentupload/tempimage.png")
                tempImage = cv2.imread("images/image_sunflower_0108.png")
                shape = tempImage.shape

                resize = cv2.resize(origImage, (shape[1], shape[0]), cv2.INTER_AREA)
                cv2.imwrite("currentupload/tempimage.png", resize)

                relPath = "currentupload/tempimage.png"
                redo=relPath

                toBG = "#graphicsView\n" + \
                       "{\n" + \
                       " border-image: url(\"{0}\");\n".format(relPath) + \
                       "\n" + \
                       "}"
                self.graphicsView.setStyleSheet(toBG)

                img=cv2.imread(relPath)
                #cv2.imshow("Test",img)
                img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ret,img=cv2.threshold(img,100,255,cv2.THRESH_BINARY)

                cv2.imwrite("currentupload/tempimage_mask.png",img)
                #cv2.imshow("Test2",img)

                relPath = "currentupload/tempimage_mask.png"
                toBG = "#graphicsView_2\n" + \
                       "{\n" + \
                       " border-image: url(\"{0}\");\n".format(relPath) + \
                       "\n" + \
                       "}"

                self.graphicsView_2.setStyleSheet(toBG)

                toBG = "#graphicsView\n" + \
                       "{\n" + \
                       " border-image: url(\"{0}\");\n".format(redo) + \
                       "\n" + \
                       "}"

                self.graphicsView.setStyleSheet(toBG)

        except:
            print("Invalid image selected!")

    def addImageButton(self):

        imgname, ok = QtWidgets.QInputDialog.getText(self, 'Text Input Dialog', 'Name of Flower?')

        if ok:
            origimgname=imgname
            pref1=1
            pref2=1
            imgname="image_"+origimgname+"_"+str(pref1)+".png"
            maskname="mask_"+origimgname+"_"+str(pref2)+".png"

            try:
                imgPath="currentupload/tempimage.png"
                imgMaskPath="currentupload/tempimage_mask.png"

                origImgList=os.listdir(os.getcwd()+"\\images")
                print(origImgList)

                i=1
                print("Debug")
                while imgname in origImgList:
                    i=i+1
                    pref1=i
                    pref2=i
                    imgname = "image_" + origimgname + "_" + str(pref1)
                    maskname = "mask_" + origimgname + "_" + str(pref2)

                print("Debug")
                print(imgPath)
                print(imgMaskPath)
                print(imgname)
                print(maskname)
                shutil.copy(imgPath, "images/{}.png".format(imgname))
                shutil.copy(imgMaskPath, "masks/" +maskname+".png")

                messagebox.showinfo("Success", "Image Added")
            except:
                messagebox("Error", "Invalid image selected!")

    def initList(self):

        conn=pymysql.connect(host="localhost", user="root", password="toor", db="flower")

        with conn.cursor() as curr:
            query="SELECT * FROM flower.users"
            curr.execute(query)
            result=curr.fetchall()
            self.listWidget.clear()
            for item in result:
                self.listWidget.addItem(item[0])

        conn.close()

    def addUserButton(self):

        uname=self.unameTB.text()
        password=self.passTB.text()
        confirm=self.confirmTB.text()

        if uname and password and confirm and \
            not uname.isspace() and \
            not password.isspace() and \
            not confirm.isspace():

            conn = pymysql.connect(host="localhost", user="root", password="toor", db="flower")

            with conn.cursor() as curr:
                query="SELECT * FROM flower.users WHERE `Username`=%s;"
                curr.execute(query,uname)
                result=curr.fetchall()

                if not len(result):
                    if password == confirm:
                        query="INSERT INTO flower.users(`Username`, `Password`) VALUES(%s,%s);"
                        curr.execute(query,(uname,password))
                        conn.commit()
                        self.initList()
                        messagebox.showinfo("Success", "User added!")
                    else:
                        messagebox.showinfo("Error", "Password and Confirm not the same!")
                else:
                    messagebox.showinfo("Error", "Username already exists!")

            conn.close()

    def deleteUserButton(self):

        try:
            selectedUname=self.listWidget.currentItem().text()

            if selectedUname:
                print(selectedUname)
                conn=pymysql.connect(host="localhost", user="root", password="toor", db="flower")

                with conn.cursor() as curr:
                    query="DELETE FROM flower.users WHERE `Username`=%s"
                    curr.execute(query,selectedUname)
                    conn.commit()
                    self.initList()
                    messagebox.showinfo("Success", "User has been deleted!")
                    selectedUname=""
            else:
                messagebox.showinfo("Error", "Select username from the list!")
        except:
            messagebox.showinfo("Error", "Select username from the list!")

if __name__ == '__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    w=LoginWindow()
    w.show()
    sys.exit(app.exec_())
