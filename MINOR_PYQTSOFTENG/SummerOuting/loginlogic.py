from PyQt5 import QtCore, QtGui, QtWidgets
import loginwindow
from mainlogic import MainWindow
import pymysql
from tkinter import Tk,messagebox

class LoginWindow(QtWidgets.QMainWindow, loginwindow.Ui_MainWindow):

    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='toor',
                           db='summerouting')

    r = Tk()
    r.withdraw()
    r.iconbitmap("images/sun_icon.ico");

    def __init__(self, parent=None):

        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(464, 257)

        # Login Button
        self.pushButton.clicked.connect(self.loginButtonClicked)

        # New Window Listener
        self.dialog = MainWindow(self)

    def openMainWindow(self):
        self.hide()
        self.dialog.show()

    def loginButtonClicked(self):

        print("Login Button Clicked")

        with self.conn.cursor() as curr:
            query="SELECT * FROM summerouting.users WHERE `Username`=%s AND `Password`=%s;"

            username=self.lineEdit.text()
            password=self.lineEdit_2.text()

            print(username)
            print(password)

            curr.execute(query,(username,password))
            result=curr.fetchall()

            if len(result)!=0:
                self.openMainWindow()
            else:
                messagebox.showinfo("Error","User does not exists!")

if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w=LoginWindow()
    w.show()
    sys.exit(app.exec())