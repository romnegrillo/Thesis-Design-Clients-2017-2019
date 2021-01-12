# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adminwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(603, 452)
        MainWindow.setStyleSheet("#MainWindow\n"
"{\n"
"background-color: qconicalgradient(cx:1, cy:1, angle:0, stop:0 rgba(255, 131, 0, 255), stop:1 rgba(255, 255, 255, 255))\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(30, 50, 541, 371))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 61, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 61, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(20, 100, 61, 16))
        self.label_4.setObjectName("label_4")
        self.unameTB = QtWidgets.QLineEdit(self.tab)
        self.unameTB.setGeometry(QtCore.QRect(80, 40, 113, 20))
        self.unameTB.setObjectName("unameTB")
        self.passTB = QtWidgets.QLineEdit(self.tab)
        self.passTB.setGeometry(QtCore.QRect(80, 70, 113, 20))
        self.passTB.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passTB.setObjectName("passTB")
        self.confirmTB = QtWidgets.QLineEdit(self.tab)
        self.confirmTB.setGeometry(QtCore.QRect(80, 100, 113, 20))
        self.confirmTB.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmTB.setObjectName("confirmTB")
        self.addUserB = QtWidgets.QPushButton(self.tab)
        self.addUserB.setGeometry(QtCore.QRect(120, 140, 75, 23))
        self.addUserB.setObjectName("addUserB")
        self.deleteUserB = QtWidgets.QPushButton(self.tab)
        self.deleteUserB.setGeometry(QtCore.QRect(30, 140, 75, 23))
        self.deleteUserB.setObjectName("deleteUserB")
        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setGeometry(QtCore.QRect(240, 20, 256, 311))
        self.listWidget.setObjectName("listWidget")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(100, 30, 71, 20))
        self.label_5.setObjectName("label_5")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(180, 30, 161, 20))
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.browseB = QtWidgets.QPushButton(self.tab_2)
        self.browseB.setGeometry(QtCore.QRect(350, 30, 75, 23))
        self.browseB.setObjectName("browseB")
        self.graphicsView = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView.setGeometry(QtCore.QRect(10, 70, 256, 211))
        self.graphicsView.setStyleSheet("#graphicsView\n"
"{\n"
" border-image: url(\"gui_images/image_logo.png\");\n"
"\n"
"}")
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView_2.setGeometry(QtCore.QRect(270, 70, 256, 211))
        self.graphicsView_2.setStyleSheet("#graphicsView_2\n"
"{\n"
" border-image: url(\"gui_images/image_logo.png\");\n"
"\n"
"}")
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.addImgB = QtWidgets.QPushButton(self.tab_2)
        self.addImgB.setGeometry(QtCore.QRect(450, 300, 75, 23))
        self.addImgB.setObjectName("addImgB")
        self.tabWidget.addTab(self.tab_2, "")
        self.logoutB = QtWidgets.QPushButton(self.centralwidget)
        self.logoutB.setGeometry(QtCore.QRect(490, 20, 75, 23))
        self.logoutB.setObjectName("logoutB")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 603, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Welcome Admin"))
        self.label_2.setText(_translate("MainWindow", "Username:"))
        self.label_3.setText(_translate("MainWindow", "Password:"))
        self.label_4.setText(_translate("MainWindow", "Confirm:"))
        self.addUserB.setText(_translate("MainWindow", "Add User"))
        self.deleteUserB.setText(_translate("MainWindow", "Delete User"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Manage Users"))
        self.label_5.setText(_translate("MainWindow", "Selected File:"))
        self.browseB.setText(_translate("MainWindow", "Browse"))
        self.addImgB.setText(_translate("MainWindow", "Add Image"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Upload Image"))
        self.logoutB.setText(_translate("MainWindow", "Logout"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

