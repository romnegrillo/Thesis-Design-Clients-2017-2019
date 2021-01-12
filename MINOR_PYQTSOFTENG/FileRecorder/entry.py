from PyQt5 import QtCore, QtGui, QtWidgets
import login
import main
import manageusers
import pymysql
import user
import datetime
import os
import shutil
from tkinter import Tk,messagebox

class LoginWindow(QtWidgets.QMainWindow, login.Ui_MainWindow):

    root=Tk()
    root.withdraw()
    root.iconbitmap("images/file_logo.ico")

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.loginClicked)

    def loginClicked(self):
        print("Login Button Clicked")

        uname=self.lineEdit.text()
        pw=self.lineEdit_2.text()

        print(uname)
        print(pw)

        if uname and \
           not uname.isspace() and \
           pw and \
           not pw.isspace():

            print("Valid Credentials")

            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='toor',
                                   db='filerecorder')

            with conn.cursor() as curr:
                query="SELECT * FROM filerecorder.users WHERE `Username`=%s AND `Password`=%s ;"
                curr.execute(query, (uname,pw))
                result=curr.fetchall()

            if(len(result)):
                print("Found record!")

                for item in result:
                    if item[5]=="Admin":
                        self.dialog=MainWindow()
                        self.hide()
                        self.dialog.show()
                    else:
                        self.dialog=UserWindow(uname)
                        self.hide()
                        self.dialog.show()
            else:
                messagebox.showinfo("Error", "Invalid username and/or password!")

            conn.close()
        else:
            messagebox.showinfo("Error", "All fields are required!")

class MainWindow(QtWidgets.QMainWindow, main.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.verticalHeader().setVisible(False);
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.cellClicked.connect(self.cellClicked)

        # pushButton - Manage Users
        # pushButton_2 - Open File
        # pushButton_3 - Delete File
        # pushButton_4 - Logout
        # pushButton_5 - ChangePass

        self.pushButton.clicked.connect(self.manageUsers)
        self.pushButton_2.clicked.connect(self.openFile)
        self.pushButton_3.clicked.connect(self.deleteFile)
        self.pushButton_4.clicked.connect(self.logout)
        self.pushButton_5.clicked.connect(self.changePass)
        self.updateTable()

    def changePass(self):

        pp=self.lineEdit.text()
        np=self.lineEdit_2.text()
        cp=self.lineEdit_3.text()

        if pp and np and cp and not pp.isspace() and not np.isspace() and not cp.isspace():

            if not (np==cp):
                messagebox.showinfo("Error", "Password and Confirm not the same!")
                return

            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='toor',
                                   db='filerecorder')

            with conn.cursor() as curr:
                query='UPDATE filerecorder.users SET `Password`=%s WHERE `Username`="admin";'
                curr.execute(query,np)
                conn.commit()
                messagebox.showinfo("Success", "Password updated!")

            conn.close()


    def updateTable(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='filerecorder')


        with conn.cursor() as curr:

            query = "SELECT * FROM filerecorder.records;"
            curr.execute(query)
            result = curr.fetchall()

            if (len(result)):

                self.tableWidget.setRowCount(len(result))

                for i in range(0, len(result)):
                    self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(result[i][0])))
                    self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(result[i][1])))
                    self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(result[i][2])))
                    self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(result[i][3])))

            else:
                self.tableWidget.setRowCount(0)

        conn.close()

    def manageUsers(self):
        self.dialog=ManageWindow()
        self.hide()
        self.dialog.show()

    def openFile(self):

        if self.selectedCellItem != 0 and \
                self.selectedCellItem.isdigit():

            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='toor',
                                   db='filerecorder')

            with conn.cursor() as curr:
                query = "SELECT `File Name` FROM filerecorder.records WHERE `File ID`=%s"
                curr.execute(query, self.selectedCellItem)
                result=curr.fetchall()

                for item in result:
                    dir=os.getcwd()+"\\adminrecord\\"+item[0]
                    os.startfile(dir)

            conn.close()

        else:
            messagebox.showinfo("Error", "Select File ID to open!")


    def deleteFile(self):

        if self.selectedCellItem != 0 and \
                self.selectedCellItem.isdigit():

            result = messagebox.askquestion("Delete", "Delete File?", icon='warning')

            if result == 'yes':
                pass
            else:
                return

            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='toor',
                                   db='filerecorder')

            with conn.cursor() as curr:
                query = "SELECT `File Name` FROM filerecorder.records WHERE `File ID`=%s"
                curr.execute(query, self.selectedCellItem)
                result=curr.fetchall()

                for item in result:
                    dir1 = os.getcwd() + "\\adminrecord\\" + item[0]
                    dir2 = os.getcwd() + "\\userrecord\\" + item[0]
                    break

                print(dir1)
                print(dir2)

                os.remove(dir1)
                os.remove(dir2)

                query = "DELETE FROM filerecorder.records WHERE `File ID`=%s"
                curr.execute(query, self.selectedCellItem)
                conn.commit()

            messagebox.showinfo("Success", "File removed from the list.")
            conn.close()
            self.updateTable()
        else:
            messagebox.showinfo("Error", "Select File ID to delete!")

    def cellClicked(self,row,col):
        self.selectedCellItem=self.tableWidget.item(row,col).text()
        print(self.selectedCellItem)

    def logout(self):
        self.dialog=LoginWindow()
        self.hide()
        self.dialog.show()

class ManageWindow(QtWidgets.QMainWindow, manageusers.Ui_MainWindow):

    def __init__(self, parent=None):
        super(ManageWindow, self).__init__(parent)
        self.setupUi(self)

        self.tableWidget.verticalHeader().setVisible(False);
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.cellClicked.connect(self.cellClicked)

        # pushButton - Add
        # pushButton_1 - Delete
        # pushButton_2 - Logout

        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.delete)
        self.pushButton_3.clicked.connect(self.logout)

        self.updateTable()

    def updateTable(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='filerecorder')

        with conn.cursor() as curr:
            query="SELECT * FROM filerecorder.users;"
            curr.execute(query)
            result=curr.fetchall()

            if(len(result)):

                self.tableWidget.setRowCount(len(result))


                for i in range(0,len(result)):
                    self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(result[i][0])))
                    self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(result[i][1])))
                    self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(result[i][3])))
                    self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(result[i][4])))

            else:
                self.tableWidget.rowCount(0)

        conn.close()

    def add(self):

        uname=self.unameTB.text()
        pw=self.pwTB.text()
        pwC=self.confirmTB.text()
        fn=self.fnTB.text()
        ln=self.lnTB.text()

        if uname and pw and pwC and fn and ln and \
           not uname.isspace() and not pw.isspace() and \
            not pwC.isspace() and not fn.isspace() and \
            not ln.isspace():

            if not (pw==pwC):
                messagebox.showinfo("Error", "Password and Confirm not the same!")
                return

            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='toor',
                                   db='filerecorder')

            fileID=1

            with conn.cursor() as curr:

                facID=1

                query="SELECT `Faculty ID` FROM filerecorder.users;"
                curr.execute(query)
                result=curr.fetchall()
                print(len(result))

                if not (len(result) == 0):
                    facID=len(result)+1

                query="SELECT `Username` FROM filerecorder.users;"
                curr.execute(query)
                result=curr.fetchall()

                for item in result:

                    if item[0]==uname:
                        messagebox.showinfo("Error", "Username already exists!")
                        conn.close()
                        return

                query="INSERT INTO filerecorder.users(`Faculty ID`, `Username`, `Password`, `First Name`, `Last Name`, `Account Type`) " + \
                      "VALUES(%s,%s,%s,%s,%s,%s);"
                curr.execute(query,(facID,uname,pw,fn,ln,"User"))
                conn.commit()

                self.updateTable()
                messagebox.showinfo("Success", "User added to the database!")

            conn.close()
        else:
            messagebox.showinfo("Error", "All field are required!")


    def delete(self):

        if self.selectedCellItem != 0 and \
                self.selectedCellItem.isdigit():

            result = messagebox.askquestion("Delete", "Delete User?", icon='warning')

            if result == 'yes':
                pass
            else:
                return

            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='toor',
                                   db='filerecorder')

            with conn.cursor() as curr:
                query="DELETE FROM filerecorder.users WHERE `Faculty ID`=%s"
                curr.execute(query, self.selectedCellItem)
                conn.commit()

            messagebox.showinfo("Success", "User removed from the list.")
            conn.close()
            self.updateTable()
        else:
            messagebox.showinfo("Error", "Select Faculty ID to delete!")

    def cellClicked(self,row,col):
        self.selectedCellItem=self.tableWidget.item(row,col).text()
        print(self.selectedCellItem)

    def logout(self):
        self.dialog=MainWindow()
        self.hide()
        self.dialog.show()

class UserWindow(QtWidgets.QMainWindow, user.Ui_MainWindow):

    def __init__(self,uname,parent=None):

        super(UserWindow, self).__init__(parent)
        self.setupUi(self)

        # lineEdit - Browse Textbox
        # pushButton - Browse
        # pushButton_2 - Add File
        # pushButton_3 - Logout
        # pusbutton_4 - Open File
        # label_2 - Username Logged In

        self.uname=uname
        self.label_2.setText(uname)
        self.pushButton.clicked.connect(self.browseFile)
        self.pushButton_2.clicked.connect(self.addFile)
        self.pushButton_3.clicked.connect(self.logout)
        self.pushButton_4.clicked.connect(self.openFile)
        self.pushButton_5.clicked.connect(self.changePass)
        self.updateListBox()

    def openFile(self):

        try:
            dir = os.getcwd() + "\\adminrecord\\" + self.listWidget.currentItem().text()
            os.startfile(dir)
        except:
            messagebox.showinfo("Error", "Invalid file selected! Select valid file from the list!")

    def changePass(self):

        pp = self.lineEdit_3.text()
        np = self.lineEdit_2.text()
        cp = self.lineEdit_4.text()

        if pp and np and cp and not pp.isspace() and not np.isspace() and not cp.isspace():

            if not (np == cp):
                messagebox.showinfo("Error", "Password and Confirm not the same!")
                return

            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='toor',
                                   db='filerecorder')

            with conn.cursor() as curr:
                query = 'UPDATE filerecorder.users SET `Password`=%s WHERE `Username`=%s;'
                curr.execute(query, (np,self.uname))
                conn.commit()
                messagebox.showinfo("Success", "Password updated!")

            conn.close()

    def updateListBox(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='filerecorder')

        with conn.cursor() as curr:
            query="SELECT `File Name` FROM filerecorder.records WHERE `Uploader`=%s;"
            curr.execute(query, self.uname)
            result=curr.fetchall()

            if not (len(result) == 0):
                self.listWidget.clear()
                for item in result:
                    self.listWidget.addItem(item[0])
        conn.close()

    def browseFile(self):

        try:
            dlg = QtWidgets.QFileDialog()
            dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)

            if dlg.exec_():
                fileName = dlg.selectedFiles()
                print(fileName)
                self.lineEdit.setText(fileName[0])
        except:
            print("An error has occured.")

    def addFile(self):

        fselect=self.lineEdit.text()

        if fselect and \
           not fselect.isspace() and \
           os.path.exists(fselect):

            splitdir=len(fselect.split("/"))
            filename=fselect.split("/")[splitdir-1]
            print(filename)

            fileList=os.listdir("adminrecord")
            print(fileList)

            if filename in fileList:
                messagebox.showinfo("Error", "File already exists! Change file name!")
                return

            fileID=1

            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='toor',
                                   db='filerecorder')

            with conn.cursor() as curr:
                query="SELECT `File ID` FROM filerecorder.records;"
                curr.execute(query)
                result=curr.fetchall()
                print(len(result))

                if not (len(result) == 0):
                    fileID=len(result)+1

                now=datetime.datetime.now()
                dateUploaded=str(now.month) + "/" + str(now.day) + "/" + str(now.year)

                query="INSERT INTO filerecorder.records(`File ID`, `File Name`, `Uploader`, `Date Uploaded`) " + \
                      "VALUES(%s,%s,%s,%s)"
                curr.execute(query,(fileID,filename,self.uname,dateUploaded))
                conn.commit()

                destUser=os.getcwd()+"\\userrecord\\"+filename
                destAdmin=os.getcwd()+"\\adminrecord\\"+filename

                shutil.copy(fselect,destUser)
                shutil.copy(fselect,destAdmin)

                messagebox.showinfo("Success", "File Added to the database!")

                self.updateListBox()

            conn.close()
        else:
            messagebox.showinfo("Error", "Invalid file selected!")

    def logout(self):
        self.dialog=LoginWindow()
        self.hide()
        self.dialog.show()

if __name__ == '__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    w=LoginWindow()
    w.show()
    sys.exit(app.exec_())
