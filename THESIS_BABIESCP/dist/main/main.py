from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi
import sys
import babies_database
import serial
import serial.tools.list_ports
import babies_fuzzy
import csv
import math


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main_window.ui", self)
        self.setWindowTitle("Thesis")
        self.setFixedSize(self.size())

        self.csvFileName.setEnabled(False)

        # Button listeners.
        self.connectButton.clicked.connect(self.connectButtonClicked)
        self.disconnectButton.clicked.connect(self.disconnectButtonClicked)
        self.saveCSVButton.clicked.connect(self.saveCSVButtonClicked)
        self.clearDataButton.clicked.connect(self.clearDataButtonClicked)

        self.browseCSVButton.clicked.connect(self.browseCSVButtonClicked)
        self.graphCSVButton.clicked.connect(self.graphCSVButtonClicked)
        self.clearCSVButton.clicked.connect(self.clearCSVButtonClicked)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.ser = serial.Serial()

        self.babiesFuzzy = babies_fuzzy.BabiesFuzzy()

        self.loadPorts()
        self.loadDatabase()

    def connectButtonClicked(self):
        if(self.openPort()):
            self.startTimer()
            self.connectButton.setEnabled(False)
            self.disconnectButton.setEnabled(True)
            self.saveCSVButton.setEnabled(False)
            self.clearDataButton.setEnabled(False)

    def disconnectButtonClicked(self):
        self.stopTimer()
        self.closePort()

        self.connectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)
        self.saveCSVButton.setEnabled(True)
        self.clearDataButton.setEnabled(True)

    def saveCSVButtonClicked(self):
        rowLen = self.tableWidget.rowCount()
        colLen = self.tableWidget.columnCount()

        # print(rowLen,colLen)

        if rowLen != 0:
            rowData = []
            colData = []

            for i in range(0, rowLen):
                colData = []
                for j in range(0, colLen):
                    colData.append(self.tableWidget.item(i, j).data(0))
                rowData.append(colData)

            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save Data", "", "CSV (*.csv)", options=options)

            if fileName:
                # print(fileName)
                fileName = fileName+".csv"
            else:
                return

            # for item in rowData:
            #    print(item)

# workbook = xlsxwriter.Workbook(fileName)
# worksheet = workbook.add_worksheet()
# worksheet.set_column(0,1,20.0)
# worksheet.set_column(1,5,10.0)
##
##
# for j,name in enumerate(self.colNames):
# worksheet.write(0,j,name)
##
# for i,rowEntry in enumerate(rowData):
# for j,colEntry in enumerate(rowEntry):
# worksheet.write(i,j,colEntry)

            try:
                with open(fileName, mode="w", newline="") as f:
                    writer = csv.writer(f, delimiter=",")
                    writer.writerow(self.colNames)

                    # Write lists of rows separated by comma.
                    for rowEntry in (rowData):
                        writer.writerow(rowEntry)
            except Exception as exp:
                print(str(exp))

            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("File successfully generated!")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.exec_()

        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Empty Database")
            msg.setText("Database is empty!")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.exec_()

    def clearDataButtonClicked(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Clear Database")
        msg.setText("Are you sure you want to clear the database?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)

        if msg.exec() == QtWidgets.QMessageBox.Yes:
            self.babiesDB.clearDB()
            self.loadDataFromDB()

    def loadPorts(self):
        self.disconnectButton.setEnabled(False)
        portObj = serial.tools.list_ports.comports()
        portList = []
        # print(portObj)

        if len(portObj):
            for port in portObj:
                portList.append(port.device)

            # print(portList)
            self.portsCB.addItems(portList)

    def openPort(self):
        selectedPort = self.portsCB.currentText()
        print(selectedPort)

        if selectedPort:
            try:
                self.ser = serial.Serial(selectedPort, 9600, timeout=1)

                return True
            except:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Error opening port!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()

            return False
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("No port selected!")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()

    def closePort(self):
        if self.ser.isOpen():
            self.ser.close()

    def startTimer(self):
        if not self.timer.isActive():
            print("Timer started.")
            self.timer.start(1000)

    def stopTimer(self):
        if self.timer.isActive():
            self.timer.stop()

    def updateTimer(self):
        # print("test")

        data = self.ser.readline()
        data = data.decode()

        print(data)

        try:
            if data:
                # Format:
                # NODE1,1,2,3,NODE2,4,5,6,NODE3,7,8,9,NODE4,10,11,12
                data = data.split(",")
                data = [float(x) for x in data if self.isNumber(x)]

                # Format will be now:
                # 1,2,3,4,5,6,7,8,9,10,11,12
                print("Format")
                print(data)

                try:
                    L1 = round(math.sqrt((data[0]**2)+(data[1]**2)+(data[2]**2)), 4)
                    L2 = round(math.sqrt((data[3]**2)+(data[4]**2)+(data[5]**2)), 4)
                    L3 = round(math.sqrt((data[6]**2)+(data[7]**2)+(data[8]**2)), 4)
                    L4 = round(math.sqrt((data[9]**2)+(data[10]**2)+(data[11]**2)), 4)
                except Exception as exp:
                    print(str(exp))

                print("Magnitudes")
                print(L1, L2, L3, L4)

                self.babiesDB.addDataDB(L1, L2, L3, L4)
                self.loadDataFromDB()
        except Exception as exp:
            print(str(exp))

    def isNumber(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def loadDatabase(self):
        self.babiesDB = babies_database.BabiesDatabase("./database/babies_records.db")
        self.babiesDB.connectDB()

        self.colNames = ["time", "left_arm", "right_arm", "left_leg", "right_leg"]
        self.loadDataFromDB()

    def loadDataFromDB(self):
        data = self.babiesDB.getDataDB()

        if len(data):
            rowLen = len(data)
            colLen = len(data[0])

            self.tableWidget.setRowCount(rowLen)
            self.tableWidget.setColumnCount(colLen)

            for i in range(0, rowLen):
                for j in range(0, colLen):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
        else:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.tableWidget.clear()

        self.tableWidget.setHorizontalHeaderLabels(self.colNames)
        header = self.tableWidget.horizontalHeader()

        if len(data):
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

    #################################################################
    # Second Tab
    #################################################################

    def browseCSVButtonClicked(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select CSV File", "", "CSV (*.csv)", options=options)
        self.fullFiles = files[0]
        print(self.fullFiles)

        data = []

        if files:

            # print("debug")
            # with open(self.fullFiles) as csv_file:
            #     try:
            #         fileName = files[0][files[0].rindex("/")+1:]
            #         self.csvFileName.setText(fileName)
            #         csv_reader = csv.reader(csv_file, delimiter=',')
            #         line_count = 0
            #         for row in csv_reader:
            #             if line_count == 0:
            #                 pass
            #             else:
            #                 data.append(row)
            #
            #             line_count += 1
            #
            #         for items in data:
            #             print(items)

            # CSV will produce list of lists.
            # Pass the data to fuzzy logic class to interpret it.

            try:
                self.csvFileName.setText(self.fullFiles[self.fullFiles.rfind("/"):])
                self.babiesFuzzy.readCSV(self.fullFiles)
                self.cpClassificationLabel.setText(self.babiesFuzzy.getClassification())
            except Exception as exp:
                print(str(exp))

    def graphCSVButtonClicked(self):
        retValue = self.babiesFuzzy.readCSV(self.fullFiles)

        if retValue == 0:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Empty or invalid CSV file.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

    def clearCSVButtonClicked(self):
        self.cpClassificationLabel.setText("")
        self.csvFileName.setText("")
        self.babiesFuzzy.closeAllPlots()
        

    #################################################################

    def closeEvent(self, event):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Exit")
        msg.setText("Are you sure you want to exit?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)

        if msg.exec() == QtWidgets.QMessageBox.Yes:
            self.stopTimer()
            self.closePort()
            self.babiesFuzzy.closeAllPlots()
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
