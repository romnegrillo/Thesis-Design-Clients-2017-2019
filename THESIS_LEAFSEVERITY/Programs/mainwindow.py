# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setStyleSheet("#MainWindow\n"
"{\n"
"background-color: qradialgradient(spread:repeat, cx:0.494, cy:0.226364, radius:1.255, fx:0.488682, fy:0.961, stop:0 rgba(55, 255, 25, 255), stop:1 rgba(255, 255, 255, 255));\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(10, 10, 661, 371))
        self.imageLabel.setStyleSheet("#imageLabel\n"
"{\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.imageLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.imageLabel.setText("")
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setObjectName("imageLabel")
        self.rgbButton = QtWidgets.QPushButton(self.centralwidget)
        self.rgbButton.setGeometry(QtCore.QRect(690, 10, 91, 51))
        self.rgbButton.setObjectName("rgbButton")
        self.totalAreaButton = QtWidgets.QPushButton(self.centralwidget)
        self.totalAreaButton.setGeometry(QtCore.QRect(690, 150, 91, 51))
        self.totalAreaButton.setObjectName("totalAreaButton")
        self.infectedAreaButton = QtWidgets.QPushButton(self.centralwidget)
        self.infectedAreaButton.setGeometry(QtCore.QRect(690, 220, 91, 51))
        self.infectedAreaButton.setObjectName("infectedAreaButton")
        self.binaryButton = QtWidgets.QPushButton(self.centralwidget)
        self.binaryButton.setGeometry(QtCore.QRect(690, 80, 91, 51))
        self.binaryButton.setObjectName("binaryButton")
        self.startMenuButton = QtWidgets.QPushButton(self.centralwidget)
        self.startMenuButton.setGeometry(QtCore.QRect(690, 400, 91, 51))
        self.startMenuButton.setObjectName("startMenuButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 400, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.severityLabel = QtWidgets.QLabel(self.centralwidget)
        self.severityLabel.setGeometry(QtCore.QRect(140, 400, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.severityLabel.setFont(font)
        self.severityLabel.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.severityLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.severityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.severityLabel.setObjectName("severityLabel")
        self.fungiLabel = QtWidgets.QLabel(self.centralwidget)
        self.fungiLabel.setGeometry(QtCore.QRect(410, 400, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fungiLabel.setFont(font)
        self.fungiLabel.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.fungiLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.fungiLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fungiLabel.setObjectName("fungiLabel")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(280, 400, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
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
        self.rgbButton.setText(_translate("MainWindow", "RGB"))
        self.totalAreaButton.setText(_translate("MainWindow", "Total Area"))
        self.infectedAreaButton.setText(_translate("MainWindow", "Infected Area"))
        self.binaryButton.setText(_translate("MainWindow", "Binary"))
        self.startMenuButton.setText(_translate("MainWindow", "Start Menu"))
        self.label_2.setText(_translate("MainWindow", "Percent\n"
"Severity"))
        self.severityLabel.setText(_translate("MainWindow", "0%"))
        self.fungiLabel.setText(_translate("MainWindow", "-"))
        self.label_5.setText(_translate("MainWindow", "Suggested\n"
"Fungicides"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

