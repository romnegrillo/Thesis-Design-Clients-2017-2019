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
        MainWindow.resize(712, 411)
        MainWindow.setStyleSheet("#MainWindow\n"
"{\n"
"background-color: qconicalgradient(cx:1, cy:0.966, angle:0, stop:0 rgba(10, 90, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(50, 20, 301, 191))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 50, 61, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 61, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(40, 110, 51, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(40, 20, 61, 16))
        self.label_4.setObjectName("label_4")
        self.judgeCB = QtWidgets.QComboBox(self.groupBox)
        self.judgeCB.setGeometry(QtCore.QRect(90, 20, 171, 22))
        self.judgeCB.setObjectName("judgeCB")
        self.judgeCB.addItem("")
        self.judgeCB.addItem("")
        self.judgeCB.addItem("")
        self.candidateCB = QtWidgets.QComboBox(self.groupBox)
        self.candidateCB.setGeometry(QtCore.QRect(90, 50, 171, 22))
        self.candidateCB.setObjectName("candidateCB")
        self.candidateCB.addItem("")
        self.candidateCB.addItem("")
        self.candidateCB.addItem("")
        self.candidateCB.addItem("")
        self.candidateCB.addItem("")
        self.candidateCB.addItem("")
        self.candidateCB.addItem("")
        self.candidateCB.addItem("")
        self.candidateCB.addItem("")
        self.catCB = QtWidgets.QComboBox(self.groupBox)
        self.catCB.setGeometry(QtCore.QRect(90, 80, 171, 22))
        self.catCB.setObjectName("catCB")
        self.catCB.addItem("")
        self.catCB.addItem("")
        self.catCB.addItem("")
        self.catCB.addItem("")
        self.catCB.addItem("")
        self.catCB.addItem("")
        self.scoreTextbox = QtWidgets.QLineEdit(self.groupBox)
        self.scoreTextbox.setGeometry(QtCore.QRect(90, 110, 171, 20))
        self.scoreTextbox.setObjectName("scoreTextbox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(180, 140, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 140, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(390, 20, 271, 361))
        self.graphicsView.setStyleSheet("#graphicsView\n"
"{\n"
"background-image: url(\"images/candidates_resized/samantha.jpg\");\n"
"background-position: center; \n"
"background-repeat: no-repeat;\n"
"}")
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(50, 230, 301, 141))
        self.graphicsView_2.setStyleSheet("#graphicsView_2\n"
"{\n"
"background-image: url(\"images/sun_logo.png\");\n"
"background-position: center; \n"
"background-repeat: no-repeat;\n"
"}")
        self.graphicsView_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.graphicsView_2.setObjectName("graphicsView_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 712, 21))
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
        self.groupBox.setTitle(_translate("MainWindow", "Scoring"))
        self.label.setText(_translate("MainWindow", "Candidate:"))
        self.label_2.setText(_translate("MainWindow", "Category:"))
        self.label_3.setText(_translate("MainWindow", "Score:"))
        self.label_4.setText(_translate("MainWindow", "Judge:"))
        self.judgeCB.setItemText(0, _translate("MainWindow", "JUDGE NO. 1"))
        self.judgeCB.setItemText(1, _translate("MainWindow", "JUDGE NO. 2"))
        self.judgeCB.setItemText(2, _translate("MainWindow", "JUDGE NO. 3"))
        self.candidateCB.setItemText(0, _translate("MainWindow", "SAMANTHA TANQUECO"))
        self.candidateCB.setItemText(1, _translate("MainWindow", "BRIDALYN BEJERAS"))
        self.candidateCB.setItemText(2, _translate("MainWindow", "CHRISTINE LOISSE ALBOS"))
        self.candidateCB.setItemText(3, _translate("MainWindow", "DWIGHT TAGAPULOT"))
        self.candidateCB.setItemText(4, _translate("MainWindow", "JOHN MEDINA"))
        self.candidateCB.setItemText(5, _translate("MainWindow", "CHRYSTOPHER ONG"))
        self.candidateCB.setItemText(6, _translate("MainWindow", "EARL ZUNEGA"))
        self.candidateCB.setItemText(7, _translate("MainWindow", "CARL FRANCIS REYES"))
        self.candidateCB.setItemText(8, _translate("MainWindow", "JUMARIE MOCON"))
        self.catCB.setItemText(0, _translate("MainWindow", "Popularity Tickets"))
        self.catCB.setItemText(1, _translate("MainWindow", "Event Tickets"))
        self.catCB.setItemText(2, _translate("MainWindow", "Theme Wear"))
        self.catCB.setItemText(3, _translate("MainWindow", "Swim Wear"))
        self.catCB.setItemText(4, _translate("MainWindow", "Confidence"))
        self.catCB.setItemText(5, _translate("MainWindow", "Audience Impact"))
        self.pushButton.setText(_translate("MainWindow", "UPDATE"))
        self.pushButton_2.setText(_translate("MainWindow", "VIEW"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

