# From QtDesigner

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(504, 255)
        MainWindow.setStyleSheet("#MainWindow\n"
"{\n"
"background-color:qconicalgradient(cx:1, cy:1, angle:0, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(200, 80, 271, 131))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 30, 61, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 61, 16))
        self.label_2.setObjectName("label_2")
        self.uNameTextbox = QtWidgets.QLineEdit(self.groupBox)
        self.uNameTextbox.setGeometry(QtCore.QRect(100, 30, 141, 20))
        self.uNameTextbox.setObjectName("uNameTextbox")
        self.passTextbox = QtWidgets.QLineEdit(self.groupBox)
        self.passTextbox.setGeometry(QtCore.QRect(100, 60, 141, 20))
        self.passTextbox.setText("")
        self.passTextbox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passTextbox.setObjectName("passTextbox")
        self.loginButton = QtWidgets.QPushButton(self.groupBox)
        self.loginButton.setGeometry(QtCore.QRect(180, 90, 61, 23))
        self.loginButton.setObjectName("loginButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 9, 511, 41))
        font = QtGui.QFont()
        font.setFamily("Engravers MT")
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("#label_3\n"
"{\n"
"background-color: rgb(255, 248, 39);\n"
"}")
        self.label_3.setText("")
        self.label_3.setTextFormat(QtCore.Qt.PlainText)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(30, 80, 151, 131))
        self.graphicsView.setStyleSheet("#graphicsView\n"
"{\n"
"background-image: url(\"images/book_logo.png\");\n"
"}\n"
"")
        self.graphicsView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.graphicsView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.graphicsView.setObjectName("graphicsView")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 20, 511, 20))
        font = QtGui.QFont()
        font.setFamily("Engravers MT")
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("#label_4\n"
"{\n"
"background-color: rgb(255, 248, 39);\n"
"}")
        self.label_4.setTextFormat(QtCore.Qt.PlainText)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 504, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Authentication Required"))
        self.label.setText(_translate("MainWindow", "Username: "))
        self.label_2.setText(_translate("MainWindow", "Password:"))
        self.loginButton.setText(_translate("MainWindow", "Login"))
        self.label_4.setText(_translate("MainWindow", "THESIS RECORDER"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

