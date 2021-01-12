# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startwindow.ui'
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
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 800, 50))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("#label\n"
"{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 225, 25, 255), stop:1 rgba(255, 255, 255, 255));\n"
"}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(110, 100, 581, 301))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.shutdownButton = QtWidgets.QPushButton(self.groupBox)
        self.shutdownButton.setGeometry(QtCore.QRect(400, 110, 141, 91))
        font = QtGui.QFont()
        font.setFamily("Simplified Arabic")
        font.setPointSize(16)
        self.shutdownButton.setFont(font)
        self.shutdownButton.setObjectName("shutdownButton")
        self.imageProcButton = QtWidgets.QPushButton(self.groupBox)
        self.imageProcButton.setGeometry(QtCore.QRect(40, 110, 141, 91))
        font = QtGui.QFont()
        font.setFamily("Simplified Arabic")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.imageProcButton.setFont(font)
        self.imageProcButton.setObjectName("imageProcButton")
        self.closeButton = QtWidgets.QPushButton(self.groupBox)
        self.closeButton.setGeometry(QtCore.QRect(220, 110, 141, 91))
        font = QtGui.QFont()
        font.setFamily("Simplified Arabic")
        font.setPointSize(16)
        self.closeButton.setFont(font)
        self.closeButton.setObjectName("closeButton")
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
        self.label.setText(_translate("MainWindow", "Coffe Leaf Rust Severity Detector"))
        self.groupBox.setTitle(_translate("MainWindow", "Menu"))
        self.shutdownButton.setText(_translate("MainWindow", "Shutdown\n"
"Raspberry Pi"))
        self.imageProcButton.setText(_translate("MainWindow", "Image\n"
"Processing"))
        self.closeButton.setText(_translate("MainWindow", "Close\n"
"Program"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

