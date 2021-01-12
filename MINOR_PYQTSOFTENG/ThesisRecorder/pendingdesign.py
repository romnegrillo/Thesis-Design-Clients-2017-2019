# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pendingdesign.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(589, 376)
        MainWindow.setStyleSheet("#MainWindow\n"
"{\n"
"background-color:qconicalgradient(cx:1, cy:1, angle:0, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 171, 201))
        self.groupBox.setObjectName("groupBox")
        self.backButton = QtWidgets.QPushButton(self.groupBox)
        self.backButton.setGeometry(QtCore.QRect(50, 150, 75, 23))
        self.backButton.setObjectName("backButton")
        self.deleteButton = QtWidgets.QPushButton(self.groupBox)
        self.deleteButton.setGeometry(QtCore.QRect(50, 110, 75, 23))
        self.deleteButton.setObjectName("deleteButton")
        self.openButton = QtWidgets.QPushButton(self.groupBox)
        self.openButton.setGeometry(QtCore.QRect(50, 30, 75, 23))
        self.openButton.setObjectName("openButton")
        self.addButton = QtWidgets.QPushButton(self.groupBox)
        self.addButton.setGeometry(QtCore.QRect(50, 70, 75, 23))
        self.addButton.setObjectName("addButton")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(230, 20, 331, 331))
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 589, 21))
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
        self.groupBox.setTitle(_translate("MainWindow", "Task"))
        self.backButton.setText(_translate("MainWindow", "Back"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.openButton.setText(_translate("MainWindow", "Open"))
        self.addButton.setText(_translate("MainWindow", "Add"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

