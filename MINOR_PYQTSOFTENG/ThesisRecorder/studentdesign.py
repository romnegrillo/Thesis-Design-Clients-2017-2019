# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'studentdesign.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(610, 370)
        MainWindow.setStyleSheet("#MainWindow\n"
"{\n"
"background-color:qconicalgradient(cx:1, cy:1, angle:0, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(40, 20, 271, 321))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 40, 81, 20))
        self.label.setObjectName("label")
        self.selectFileTextbox = QtWidgets.QLineEdit(self.groupBox)
        self.selectFileTextbox.setGeometry(QtCore.QRect(80, 40, 171, 20))
        self.selectFileTextbox.setObjectName("selectFileTextbox")
        self.browseButton = QtWidgets.QPushButton(self.groupBox)
        self.browseButton.setGeometry(QtCore.QRect(60, 190, 75, 23))
        self.browseButton.setObjectName("browseButton")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(40, 70, 41, 20))
        self.label_2.setObjectName("label_2")
        self.titleTextbox = QtWidgets.QLineEdit(self.groupBox)
        self.titleTextbox.setGeometry(QtCore.QRect(80, 70, 171, 20))
        self.titleTextbox.setObjectName("titleTextbox")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 61, 20))
        self.label_3.setObjectName("label_3")
        self.programTextbox = QtWidgets.QLineEdit(self.groupBox)
        self.programTextbox.setGeometry(QtCore.QRect(80, 100, 171, 20))
        self.programTextbox.setObjectName("programTextbox")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 130, 51, 20))
        self.label_4.setObjectName("label_4")
        self.categoryComboBox = QtWidgets.QComboBox(self.groupBox)
        self.categoryComboBox.setGeometry(QtCore.QRect(80, 130, 171, 22))
        self.categoryComboBox.setObjectName("categoryComboBox")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.addButton = QtWidgets.QPushButton(self.groupBox)
        self.addButton.setGeometry(QtCore.QRect(140, 190, 75, 23))
        self.addButton.setObjectName("addButton")
        self.deleteButton = QtWidgets.QPushButton(self.groupBox)
        self.deleteButton.setGeometry(QtCore.QRect(60, 220, 75, 23))
        self.deleteButton.setObjectName("deleteButton")
        self.openFileButton = QtWidgets.QPushButton(self.groupBox)
        self.openFileButton.setGeometry(QtCore.QRect(140, 220, 75, 23))
        self.openFileButton.setObjectName("openFileButton")
        self.logoutButton = QtWidgets.QPushButton(self.groupBox)
        self.logoutButton.setGeometry(QtCore.QRect(180, 290, 75, 23))
        self.logoutButton.setObjectName("logoutButton")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(340, 30, 241, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(335, 50, 251, 291))
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 610, 21))
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
        self.label.setText(_translate("MainWindow", "Selected File:"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))
        self.label_2.setText(_translate("MainWindow", "Title: "))
        self.label_3.setText(_translate("MainWindow", "Program:"))
        self.label_4.setText(_translate("MainWindow", "Category:"))
        self.categoryComboBox.setItemText(0, _translate("MainWindow", "Image Processing"))
        self.categoryComboBox.setItemText(1, _translate("MainWindow", "Machine Learning"))
        self.categoryComboBox.setItemText(2, _translate("MainWindow", "Embedded System"))
        self.categoryComboBox.setItemText(3, _translate("MainWindow", "Web Application"))
        self.categoryComboBox.setItemText(4, _translate("MainWindow", "Desktop Application"))
        self.categoryComboBox.setItemText(5, _translate("MainWindow", "Mobile Application"))
        self.addButton.setText(_translate("MainWindow", "Add"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.openFileButton.setText(_translate("MainWindow", "Open File"))
        self.logoutButton.setText(_translate("MainWindow", "Logout"))
        self.label_5.setText(_translate("MainWindow", "Your Files"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

