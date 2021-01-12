# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'identifywindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(535, 440)
        MainWindow.setStyleSheet("#MainWindow\n"
"{\n"
"background-color: qconicalgradient(cx:1, cy:1, angle:0, stop:0 rgba(255, 131, 0, 255), stop:1 rgba(255, 255, 255, 255))\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(30, 70, 471, 311))
        self.graphicsView.setObjectName("graphicsView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 30, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.selectFileTB = QtWidgets.QLineEdit(self.centralwidget)
        self.selectFileTB.setGeometry(QtCore.QRect(170, 30, 181, 20))
        self.selectFileTB.setObjectName("selectFileTB")
        self.selectFileB = QtWidgets.QPushButton(self.centralwidget)
        self.selectFileB.setGeometry(QtCore.QRect(360, 30, 75, 23))
        self.selectFileB.setObjectName("selectFileB")
        self.classifyB = QtWidgets.QPushButton(self.centralwidget)
        self.classifyB.setGeometry(QtCore.QRect(30, 390, 75, 23))
        self.classifyB.setObjectName("classifyB")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 390, 311, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.backB = QtWidgets.QPushButton(self.centralwidget)
        self.backB.setGeometry(QtCore.QRect(426, 390, 75, 23))
        self.backB.setObjectName("backB")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 535, 21))
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
        self.label.setText(_translate("MainWindow", "Selected File:"))
        self.selectFileB.setText(_translate("MainWindow", "Browse"))
        self.classifyB.setText(_translate("MainWindow", "Classify"))
        self.label_2.setText(_translate("MainWindow", "-"))
        self.backB.setText(_translate("MainWindow", "Back"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

