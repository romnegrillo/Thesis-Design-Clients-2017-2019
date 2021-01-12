from PyQt5 import QtCore, QtGui, QtWidgets
import logindesign
from mainwindowlogic import MainWindow
import pymysql

class LoginWindow(QtWidgets.QMainWindow, logindesign.Ui_MainWindow):

    conn = pymysql.connect(host='localhost',
                             user='root',
                             password='toor',
                             db='thesisrecorder')
    
    def __init__(self,parent=None):

        # New Constructor
        super(LoginWindow, self).__init__(parent)
        
        self.setupUi(self)
        self.setFixedSize(504, 255)

        # Button Event Listener
        self.loginButton.clicked.connect(self.loginButtonClicked)


    def loginButtonClicked(self):
        uName=self.uNameTextbox.text()
        pw=self.passTextbox.text()

        with self.conn.cursor() as cur:
            query="SELECT * FROM thesisrecorder.users WHERE `Username`=%s AND `Password`=%s"
            cur.execute(query,(uName,pw))
            res=cur.fetchall()
    
        if(len(res)!=0):
            for item in res:
                if(item[2]=="Admin"):
                    print("Admin login!")
                    self.openMainWindow()   
                    break
                elif(item[2]=="Student"):
                     print("Student login!")
                     break
        else:
            print("No record!")

    def openMainWindow(self):
        self.dialog = MainWindow()
        self.hide()
        self.dialog.show()

if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w=LoginWindow()
    w.show()
    sys.exit(app.exec_())
