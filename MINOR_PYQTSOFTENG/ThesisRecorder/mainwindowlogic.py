from PyQt5 import QtCore, QtGui, QtWidgets
import logindesign
import mainwindowdesign
import registerdesign
import studentdesign
import pendingdesign
import adduserdesign
import pymysql
import shutil
import os
import datetime
from tkinter import Tk,messagebox

class LoginWindow(QtWidgets.QMainWindow, logindesign.Ui_MainWindow):

    def __init__(self, parent=None):

        # New Constructor
        super(LoginWindow, self).__init__(parent)

        self.setupUi(self)
        self.setFixedSize(504, 255)

        # Button Event Listener
        self.loginButton.clicked.connect(self.loginButtonClicked)

    def loginButtonClicked(self):
        uName = self.uNameTextbox.text()
        pw = self.passTextbox.text()

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        with conn.cursor() as cur:
            query = "SELECT * FROM thesisrecorder.users WHERE `Username`=%s AND `Password`=%s"
            cur.execute(query, (uName, pw))
            res = cur.fetchall()

        if (len(res) != 0):
            for item in res:
                if (item[2] == "Admin"):
                    print("Admin login!")
                    self.openMainWindow(uName)
                    break
                elif (item[2] == "Student"):
                    print("Student login!")
                    self.openStudentWindow(uName)
                    break
        else:
            print("No record!")
            messagebox.showinfo("Error", "Invalid username/password!")

        conn.close()

    def openMainWindow(self,uname):
        self.dialog = MainWindow(uname)
        self.hide()
        self.dialog.show()

    def openStudentWindow(self,uName):
        print("Student Login")
        self.dialog=StudentWindow(username=uName)
        self.hide()
        self.dialog.show()

########################################################################################################################

class MainWindow(QtWidgets.QMainWindow, mainwindowdesign.Ui_MainWindow):

    selectedCellItem=0
    now = datetime.datetime.now()

    r=Tk()
    r.withdraw()
    r.iconbitmap("images/book_icon.ico")
    
    def __init__(self,parent=None):

        # New Constructor
        super(MainWindow, self).__init__(parent)
        
        self.setupUi(self)
        #self.uname=uname
        print("MainWindow Open!")

        # Added GUI Design
        self.setFixedSize(893, 367)
        self.tableWidget.setColumnWidth(0,50)
        self.tableWidget.setColumnWidth(1,300)
        self.tableWidget.setColumnWidth(5, 300)
        self.tableWidget.verticalHeader().setVisible(False);
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.selectFileTextbox.setDisabled(True)
        self.displayTable()

        # Button Event Listeners
        self.browseButton.clicked.connect(self.openFileNamesDialog)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.openFileButton.clicked.connect(self.openFileButtonClicked)
        self.addUserButton.clicked.connect(self.addUserButtonClicked)
        self.pendingButton.clicked.connect(self.pendingButtonClicked)
        self.logoutButton.clicked.connect(self.logoutButtonClicked)
        self.deleteUserButton.clicked.connect(self.deleteUserButtonClicked)

        # TableWidget Listeners
        self.tableWidget.cellClicked.connect(self.cellClicked)

    def deleteUserButtonClicked(self):
        self.dialog=DeleteUserWindow(self.uname)
        self.hide()
        self.dialog.show()

    def displayTable(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        with conn.cursor() as cur:
            query="SELECT * FROM thesisrecorder.thesisrecord;"
            cur.execute(query)
            value=cur.fetchall()
            rowLen=len(value)

        print(rowLen)
        
        if(rowLen!=0):
            self.tableWidget.setRowCount(rowLen)

            for i in range(0,len(value)):
                self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(value[i][0])))
                self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(str(value[i][1])))
                self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(str(value[i][2])))
                self.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem(str(value[i][3])))
                self.tableWidget.setItem(i,4,QtWidgets.QTableWidgetItem(str(value[i][4])))
                self.tableWidget.setItem(i,5,QtWidgets.QTableWidgetItem(str(value[i][5])))
        else:
            self.tableWidget.setRowCount(0)

        conn.close()
            
    def openFileNamesDialog(self):

        try:
            dlg = QtWidgets.QFileDialog()
            dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)

            if dlg.exec_():
                fileName = dlg.selectedFiles()
                print(fileName)
                self.selectFileTextbox.setText(fileName[0])
        except:
            print("An error has occured.")

         
    def addButtonClicked(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        print("Add Button Clicked")

        if self.selectFileTextbox.text() and \
           not self.selectFileTextbox.text().isspace() and \
            self.titleTextbox.text() and \
            not self.titleTextbox.text().isspace() and \
            self.programTextbox.text() and \
            not self.titleTextbox.text().isspace() and \
            self.categoryComboBox.currentText() and \
            not self.categoryComboBox.currentText().isspace():

            ID=1
            
            with conn.cursor() as cur:
                query="SELECT `ID` FROM thesisrecorder.thesisrecord;"
                cur.execute(query)
                res=cur.fetchall()
            
            print(res)
            
            idList=[]
            
            for item in res:
                idList.append(item[0])
                
            print(idList)

            if idList:
                ID=idList[-1]+1

            title=self.titleTextbox.text()
            program=self.programTextbox.text()
            category=self.categoryComboBox.currentText()
            date=str(self.now.month)+"/"+str(self.now.day)+"/"+str(self.now.year)
            fileName=self.selectFileTextbox.text()

            print(ID)
            print(title)
            print(program)
            print(category)
            print(date)
            print(fileName)

            fileOnly=fileName.split("/")
            myFile=fileOnly[len(fileOnly)-1]
            print("File Name: ", end="")
            print(myFile)

            fileList=os.listdir("thesisrecord")

            if myFile not in fileList:

                with conn.cursor() as cur:
                    query='INSERT INTO thesisrecorder.thesisrecord' + \
                    '(`ID`, `Title`, `Program`, `Category`, `Date Added`,`File Name`) ' + \
                    'VALUES(%s,%s,%s,%s,%s,%s);'
                    print(query)
                    cur.execute(query,(ID,title,program,category,date,myFile))
                    conn.commit()
                    shutil.copy(fileName,"thesisrecord/{}".format(myFile))

                messagebox.showinfo("Success", "Record updated!")
                self.displayTable()

            else:
                messagebox.showinfo("Error", "File already exists!")
        else:
            messagebox.showinfo("Error", "All fields are required!")

        conn.close()


    def deleteButtonClicked(self):
        print("Delete Button Clicked!")

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        try:

            if self.selectedCellItem != 0 and \
               self.selectedCellItem.isdigit():

                print("ID clicked!")

                filePath=""

                with conn.cursor() as cur:
                    query="SELECT `File Name` FROM thesisrecorder.thesisrecord WHERE `ID`=%s"
                    cur.execute(query,(self.selectedCellItem))
                    result=cur.fetchall()
                    filePath=result[0][0]
                    fileOnly = filePath.split("/")
                    myFile = fileOnly[len(fileOnly) - 1]
                    print("thesisrecord/{}".format(myFile))

                    if os.path.exists(os.getcwd()+"\\thesisrecord\{}".format(myFile)):
                        print("File exists!")
                        os.remove(os.getcwd()+"\\thesisrecord\{}".format(myFile))

                with conn.cursor() as cur:
                    query="DELETE FROM thesisrecorder.thesisrecord WHERE `ID`=%s"
                    cur.execute(query,(self.selectedCellItem))
                    conn.commit()

                messagebox.showinfo("Success", "File deleted!")
                self.displayTable()
            else:
                messagebox.showinfo("Error", "Select file ID!")

        except:
                messagebox.showinfo("Error", "ID does not exists")

        conn.close()

    def cellClicked(self,row,col):
        self.selectedCellItem=self.tableWidget.item(row,col).text()
        print(self.selectedCellItem)

    def openFileButtonClicked(self):

        try:
            if self.selectedCellItem:
                print(os.getcwd() + "\\thesisrecord\\" + self.selectedCellItem)
                os.startfile(os.getcwd() + "\\thesisrecord\\" + self.selectedCellItem)
        except:
            messagebox.showinfo("Error", "Invalid file selected!")


    def addUserButtonClicked(self):

        self.dialog=RegisterWindow()
        self.close()
        self.dialog.show()

    def pendingButtonClicked(self):

        print("Pending View")
        self.dialog=PendingWindow()
        self.close()
        self.dialog.show()

    def logoutButtonClicked(self):
        self.dialog=LoginWindow()
        self.hide()
        self.dialog.show()

########################################################################################################################

class RegisterWindow(QtWidgets.QMainWindow,registerdesign.Ui_MainWindow):


    def __init__(self, parent=None):
        super(RegisterWindow, self).__init__(parent)
        self.setupUi(self)

        self.regButton.clicked.connect(self.regButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

    def backButtonClicked(self):
        self.dialog=MainWindow()
        self.hide()
        self.dialog.show()

    def regButtonClicked(self):

        uName=self.lineEdit.text()
        passw=self.lineEdit_2.text()

        cBoxSelected=""

        if self.radioButton.isChecked():
            cBoxSelected=self.radioButton.text()
        else:
            cBoxSelected=self.radioButton_2.text()

        if uName and \
           not uName.isspace() and \
           passw and \
           not passw.isspace():

            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='toor',
                                   db='thesisrecorder')

            with conn.cursor() as curr:
                query="SELECT `Username` FROM thesisrecorder.users;"
                curr.execute(query)
                result=curr.fetchall()


                unameExists=False

                for item in result:
                    print(item[0])

                    if uName==item[0]:
                        unameExists=True

                if not unameExists:
                    with conn.cursor() as curr:
                        query="INSERT INTO thesisrecorder.users(`Username`, `Password`,`Type`) VALUES(%s,%s,%s)"
                        print(query)
                        curr.execute(query,(uName,passw,cBoxSelected))
                        conn.commit()
                        messagebox.showinfo("Success!", "User registration successful!")
                else:
                    messagebox.showinfo("Error!", "Username already registered!")

            conn.close()
        else:
            messagebox.showinfo("Error!", "All fields are required!")

        print("Done")

########################################################################################################################

class StudentWindow(QtWidgets.QMainWindow, studentdesign.Ui_MainWindow):


    now=datetime.datetime.now()

    def __init__(self,parent=None):
        super(StudentWindow, self).__init__(parent)
        self.setupUi(self)

        self.browseButton.clicked.connect(self.browseButtonClicked)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.openFileButton.clicked.connect(self.openFileButtonClicked)
        self.logoutButton.clicked.connect(self.logoutButtonClicked)
        self.username=username
        self.label_5.setText(self.username)
        self.updateListBox()

    def browseButtonClicked(self):
        try:
            dlg = QtWidgets.QFileDialog()
            dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)

            if dlg.exec_():
                fileName = dlg.selectedFiles()
                print(fileName)
                self.selectFileTextbox.setText(fileName[0])
        except:
            print("An error has occured.")

    def addButtonClicked(self):
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        print("Add Button Clicked")

        if self.selectFileTextbox.text() and \
                not self.selectFileTextbox.text().isspace() and \
                self.titleTextbox.text() and \
                not self.titleTextbox.text().isspace() and \
                self.programTextbox.text() and \
                not self.titleTextbox.text().isspace() and \
                self.categoryComboBox.currentText() and \
                not self.categoryComboBox.currentText().isspace():

            ID = 1

            with conn.cursor() as cur:
                query = "SELECT `ID` FROM thesisrecorder.thesispending;"
                cur.execute(query)
                res = cur.fetchall()

            print(res)

            idList = []

            for item in res:
                idList.append(item[0])

            print(idList)

            if idList:
                ID = idList[-1] + 1

            title = self.titleTextbox.text()
            print('Debug')
            program = self.programTextbox.text()
            print('Debug')
            category = self.categoryComboBox.currentText()
            print('Debug')
            date = str(self.now.month) + "/" + str(self.now.day) + "/" + str(self.now.year)
            print('Debug')
            fileName = self.selectFileTextbox.text()
            print('Debug')

            print(ID)
            print(title)
            print(program)
            print(category)
            print(date)
            print(fileName)

            fileOnly = fileName.split("/")
            myFile = fileOnly[len(fileOnly) - 1]
            print("File Name: ", end="")
            print(myFile)

            fileList = os.listdir("thesispending")

            if myFile not in fileList:

                with conn.cursor() as cur:
                    query = 'INSERT INTO thesisrecorder.thesispending' + \
                            '(`ID`, `Title`, `Program`, `Category`, `Date Added`,`File Name`,`User`) ' + \
                            'VALUES(%s,%s,%s,%s,%s,%s,%s);'
                    print(query)
                    cur.execute(query, (ID, title, program, category, date, myFile,self.username))
                    conn.commit()
                    shutil.copy(fileName, "thesispending/{}".format(myFile))

                messagebox.showinfo("Success", "Record updated!")

            else:
                messagebox.showinfo("Error", "File already exists!")
        else:
            messagebox.showinfo("Error", "All fields are required!")

        self.updateListBox()
        conn.close()

    def deleteButtonClicked(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')
        try:
            dir = os.getcwd() + "\\thesispending\\" + self.listWidget.currentItem().text()

            with conn.cursor() as curr:
                query="DELETE FROM thesisrecorder.thesispending WHERE `File Name`=%s"
                curr.execute(query,(self.listWidget.currentItem().text()))
                conn.commit()

            os.remove(dir)
            messagebox.showinfo("Success", "File Deleted!")

        except:
            messagebox.showinfo("Error", "Invalid file selected or it has been deleted!")

        conn.close()
        self.updateListBox()

    def openFileButtonClicked(self):

        try:
            dir=os.getcwd()+"\\thesispending\\"+self.listWidget.currentItem().text()
            os.startfile(dir)
        except:
            messagebox.showinfo("Error", "Invalid file selected! Select valid file from the list!")


    def logoutButtonClicked(self):
        self.dialog=LoginWindow()
        self.hide()
        self.dialog.show()

    def updateListBox(self):
        print("List updated!")
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        with conn.cursor() as curr:
            query="SELECT `File Name` FROM thesisrecorder.thesispending WHERE `User`=%s"
            print(query)
            print(self.username)
            curr.execute(query,(self.username))
            result=curr.fetchall()
            self.listWidget.clear()
            for item in result:
                filename=str(item[0])
                filename=filename.split("/")
                filename=filename[len(filename)-1]
                self.listWidget.addItem(filename)
                print(filename)

        conn.close()

########################################################################################################################

class PendingWindow(QtWidgets.QMainWindow, pendingdesign.Ui_MainWindow):

    def __init__(self, parent=None):
        super(PendingWindow, self).__init__(parent)
        self.setupUi(self)

        self.openButton.clicked.connect(self.openButtonClicked)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)
        self.updateListBox()

    def updateListBox(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        with conn.cursor() as curr:
            query="SELECT `File Name` FROM thesisrecorder.thesispending"
            print(query)
            curr.execute(query)
            result=curr.fetchall()

        self.listWidget.clear()

        if len(result):
            for item in result:
                self.listWidget.addItem(item[0])

        conn.close()

    def openButtonClicked(self):

        try:
            dir=os.getcwd()+"\\thesispending\\"+self.listWidget.currentItem().text()
            os.startfile(dir)
        except:
            messagebox.showinfo("Error", "Invalid file selected or file has been deleted!")

    def addButtonClicked(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')
        try:
            file=self.listWidget.currentItem().text()

            with conn.cursor() as curr:
                query="SELECT * FROM thesisrecorder.thesispending WHERE `File Name`=%s;"
                curr.execute(query,(file))
                result=curr.fetchall()

                query = "SELECT `ID` FROM thesisrecorder.thesisrecord;"
                curr.execute(query)
                ids = curr.fetchall()
                idList=[]

                for id in ids:
                    idList.append(id[0])

                if len(idList):
                    nextID=len(idList)+1
                else:
                    nextID=1

                print("IDs",end=' ')
                print(idList)

                print("Next ID: ", end=' ')
                print(nextID)

            for item in result:
                title = item[1]
                program=item[2]
                cat=item[3]
                date=item[4]
                filename=item[5]

            print(title)
            print(program)
            print(cat)
            print(date)
            print(filename)

            with conn.cursor() as curr:

                query="INSERT INTO thesisrecorder.thesisrecord(`ID`, `Title`, `Program`,`Category`,`Date Added`,`File Name`) " + \
                      "VALUES(%s,%s,%s,%s,%s,%s)"
                print(query)
                curr.execute(query,(nextID,title,program,cat,date,filename))
                conn.commit()

                query="DELETE FROM thesisrecorder.thesispending WHERE `File Name`=%s;"
                print(query)
                curr.execute(query,filename)
                conn.commit()

                messagebox.showinfo("Success!", "File Added to Main Record!")

                dir = os.getcwd() + "\\thesispending\\" + self.listWidget.currentItem().text()
                shutil.copy(dir,"thesisrecord/{}".format(self.listWidget.currentItem().text()))

            conn.close()

        except:
            messagebox.showinfo("Error!", "Invalid file selected or it has been deleted!")

    def deleteButtonClicked(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        try:
            dir = os.getcwd() + "\\thesispending\\" + self.listWidget.currentItem().text()

            with conn.cursor() as curr:
                query = "DELETE FROM thesisrecorder.thesispending WHERE `File Name`=%s"
                curr.execute(query, (self.listWidget.currentItem().text()))
                conn.commit()

            messagebox.showinfo("Success", "File Deleted!")
            dir = os.getcwd() + "\\thesispending\\" + self.listWidget.currentItem().text()
            print(dir)
            os.remove(dir)
            self.updateListBox()

        except:
            messagebox.showinfo("Error", "Invalid file selected or file has been deleted!")

        conn.close()


    def backButtonClicked(self):
        self.dialog=MainWindow()
        self.hide()
        self.dialog.show()

########################################################################################################################

class DeleteUserWindow(QtWidgets.QMainWindow, adduserdesign.Ui_MainWindow):

    def __init__(self, parent=None):

        super(DeleteUserWindow, self).__init__(parent)
        self.setupUi(self)
        #self.user=user
        self.pushButton.clicked.connect(self.deleteButton)
        self.pushButton_2.clicked.connect(self.backButton)
        self.tableWidget.cellClicked.connect(self.cellClicked)
        self.updateTable()

    def cellClicked(self,row,col):
        self.selectedCellItem=self.tableWidget.item(row,col).text()
        print(self.selectedCellItem)

    def updateTable(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        with conn.cursor() as cur:
            query = "SELECT * FROM thesisrecorder.users;"
            cur.execute(query)
            value = cur.fetchall()
            rowLen = len(value)

        print(rowLen)

        if (rowLen != 0):
            self.tableWidget.setRowCount(rowLen)

            for i in range(0, len(value)):
                self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(value[i][0])))
                self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(value[i][2])))

        else:
            self.tableWidget.setRowCount(0)

        conn.close()


    def deleteButton(self):

        if self.selectedCellItem:

            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='toor',
                                   db='thesisrecorder')

            valid=False

            with conn.cursor() as curr:
                query="SELECT `Username` FROM thesisrecorder.users;"
                curr.execute(query)
                result=curr.fetchall()

                for item in result:

                    if self.selectedCellItem == item[0]:

                        if item[0] == "admin":
                            messagebox.showinfo("Error", "Cannot delete main admin account!")
                            return

                        valid=True
                        break

                if valid:
                    query="DELETE FROM thesisrecorder.users WHERE `Username`=%s;"
                    curr.execute(query, self.selectedCellItem)
                    conn.commit()
                    messagebox.showinfo("Success", "Account deleted!")
                    self.updateTable()
                else:
                    messagebox.showinfo("Error", "Selected username does not exist!")

            conn.close()

    def backButton(self):
        self.dialog=MainWindow()
        self.hide()
        self.dialog.show()


########################################################################################################################

if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w=LoginWindow()
    w.show()
    sys.exit(app.exec())
