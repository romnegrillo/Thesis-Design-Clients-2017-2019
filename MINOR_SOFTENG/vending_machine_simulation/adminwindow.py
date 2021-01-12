# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adminwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(702, 423)
        MainWindow.setStyleSheet("#MainWindow\n"
"{\n"
"background-color: rgb(85, 170, 255);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 241, 321))
        self.groupBox.setObjectName("groupBox")
        self.tb1 = QtWidgets.QLineEdit(self.groupBox)
        self.tb1.setGeometry(QtCore.QRect(90, 40, 141, 20))
        self.tb1.setObjectName("tb1")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tb2 = QtWidgets.QLineEdit(self.groupBox)
        self.tb2.setGeometry(QtCore.QRect(90, 70, 141, 20))
        self.tb2.setObjectName("tb2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.tb3 = QtWidgets.QLineEdit(self.groupBox)
        self.tb3.setGeometry(QtCore.QRect(90, 100, 141, 20))
        self.tb3.setObjectName("tb3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 100, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.addButton = QtWidgets.QPushButton(self.groupBox)
        self.addButton.setGeometry(QtCore.QRect(160, 280, 61, 31))
        self.addButton.setObjectName("addButton")
        self.deleteButton = QtWidgets.QPushButton(self.groupBox)
        self.deleteButton.setGeometry(QtCore.QRect(90, 280, 61, 31))
        self.deleteButton.setObjectName("deleteButton")
        self.editButton = QtWidgets.QPushButton(self.groupBox)
        self.editButton.setGeometry(QtCore.QRect(20, 280, 61, 31))
        self.editButton.setObjectName("editButton")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(280, 10, 401, 331))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(620, 350, 61, 31))
        self.backButton.setObjectName("backButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 702, 21))
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
        self.groupBox.setTitle(_translate("MainWindow", "CRUD"))
        self.label_2.setText(_translate("MainWindow", "Item Name:"))
        self.label_3.setText(_translate("MainWindow", "Quantity:"))
        self.label_4.setText(_translate("MainWindow", "Price/Item:"))
        self.addButton.setText(_translate("MainWindow", "ADD"))
        self.deleteButton.setText(_translate("MainWindow", "DELETE"))
        self.editButton.setText(_translate("MainWindow", "EDIT"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "quantity"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "price"))
        self.backButton.setText(_translate("MainWindow", "BACK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

