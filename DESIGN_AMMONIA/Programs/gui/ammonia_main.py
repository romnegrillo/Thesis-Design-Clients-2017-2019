from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.uic import loadUi
import sys
import serial
import serial.tools.list_ports
import ammonia_database
import datetime
import xlsxwriter

class AmmoniaMain(QtWidgets.QMainWindow):

    def __init__(self):
        super(AmmoniaMain,self).__init__()
        loadUi("ammonia_main.ui",self)

        self.setFixedSize(self.size())
        self.setWindowTitle("Ammonia Factor Monitor")

        self.connectButton.clicked.connect(self.connectButtonClicked)
        self.disconnectButton.clicked.connect(self.disconnectButtonClicked)
        self.showDateButton.clicked.connect(self.showDateButtonClicked)
        self.showAllButton.clicked.connect(self.showAllButtonClicked)
        self.createCSV.clicked.connect(self.createCSVClicked)

        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.colNames=["ammonia","pH","temperature","time"]
        
        self.loadPorts()
        self.loadDatabase()

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.updateData)

    def loadPorts(self):
        self.isPortConnected=False
        self.connectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)
        portObj=serial.tools.list_ports.comports()
        portList=[]
        #print(portObj)
        
        if len(portObj):
            for port in portObj:
                portList.append(port.device)

            #print(portList)
            self.portsCB.addItems(portList)
            
    def loadDatabase(self):
        self.isDatabaseConnected=False
        self.showChoice=1
        self.sqlObj=ammonia_database.AmmoniaDatabase("./database/ammonia.db")
        self.sqlObj.connectDatabase()
        self.showDatabase()

    def connectButtonClicked(self):
        #print("Connect button.")
        selectedPort=self.portsCB.currentText()
        #print(selectedPort)

        if selectedPort:
            if not self.isPortConnected:
                self.s=serial.Serial(selectedPort,9600,timeout=1)
                self.isPortConnected=True
                self.connectButton.setEnabled(False)
                self.disconnectButton.setEnabled(True)
                self.timer.start(1000)
        else:
            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("No port selected!")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()


    def disconnectButtonClicked(self):
        #print("Disconnect button.")

        if self.isPortConnected:
            self.s.close()
            self.isPortConnected=False
            self.connectButton.setEnabled(True)
            self.disconnectButton.setEnabled(False)
            self.timer.stop()

    def updateData(self):
        data=self.s.readline()
        ammonia=0
        pH=0
        temp=0
        waterStatus=0
        
        data=data.decode()
        #print(data)
        
        try:
            if data:
                data=data.split(",")

                for i in range(0,len(data)):
                    if i==0:
                        ammonia=float(data[i])
                    elif i==1:
                        pH=float(data[i])
                    elif i==2:
                        temp=float(data[i])
                    elif i==3:
                        waterStatus=data[i]

                self.ammoniaLabel.setText(str(ammonia))
                self.phLabel.setText(str(pH))
                self.tempLabel.setText(str(temp))
                self.sqlObj.addData(ammonia,pH,temp)
                self.showDatabase()
            
            else:
                #print("Serial timeout.")
                pass

        except Exception as exp:
            print(str(exp))

    def showDatabase(self):

        dateStr=str(self.dateEdit.date().toPyDate())
        dateStr=datetime.datetime.strptime(dateStr, '%Y-%m-%d')
        dateStr=dateStr.strftime('%m/%d/%y')

        if self.showChoice==1:
            data=self.sqlObj.getData()
            
        elif self.showChoice==2:
            data=self.sqlObj.getDataAtDate(dateStr)
            #print(dateStr)
            #print(data)
        
        if len(data):
            rowLen=len(data)
            colLen=len(data[0])

            self.tableWidget.setRowCount(rowLen)
            self.tableWidget.setColumnCount(colLen)

            for i in range(0,rowLen):
                for j in range(0,colLen):
                    self.tableWidget.setItem(i,j, QtWidgets.QTableWidgetItem(str(data[i][j])))
        else:
            
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.tableWidget.clear()
            
            #msg=QtWidgets.QMessageBox()
            #msg.setWindowTitle("Empty")
            #msg.setText("No record!")
            #msg.setIcon(QtWidgets.QMessageBox.Information)
            #msg.exec_()

        self.tableWidget.setHorizontalHeaderLabels(self.colNames)
            
    
    def showDateButtonClicked(self):
        self.showChoice=2
        self.showDatabase()

    def showAllButtonClicked(self):
        self.showChoice=1
        self.showDatabase() 

    def createCSVClicked(self):
        rowLen=self.tableWidget.rowCount()
        colLen=self.tableWidget.columnCount()

        #print(rowLen,colLen)
        
        if rowLen!=0:
            rowData=[]
            colData=[]
            
            for i in range(0,rowLen):
                colData=[]
                for j in range(0,colLen):
                    colData.append(self.tableWidget.item(i,j).data(0))
                rowData.append(colData)

            #for item in rowData:
            #    print(item)

            
            dateStr=str(self.dateEdit.date().toPyDate())
            dateStr=datetime.datetime.strptime(dateStr, '%Y-%m-%d')
            dateStr=dateStr.strftime('%m/%d/%y')
            childFolder="./generated excel files/"

            if self.showChoice==1:
                fileName=childFolder+"record_allrecords.xlsx"
            else:
                fileName=childFolder+"record_"+dateStr.replace("/","-")+".xlsx"

            workbook = xlsxwriter.Workbook(fileName)
            worksheet = workbook.add_worksheet()
            worksheet.set_column(0,2,10.0)
            worksheet.set_column(0,2,15.0)
            worksheet.set_column(3,3,20.0)

            for j,name in enumerate(self.colNames):
                worksheet.write(0,j,name)                


            for i,rowEntry in enumerate(rowData):
                for j,colEntry in enumerate(rowEntry):
                    worksheet.write(i+2,j,colEntry)


            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText(fileName.replace(childFolder,'') + " successfully generated!")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.exec_()
            

                
            workbook.close()
            
            
        else:
            msg=QtWidgets.QMessageBox()
            msg.setWindowTitle("Empty")
            msg.setText("Selected table is empty!")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.exec_()
            

        
    def closeEvent(self,event):
        if self.timer.isActive():
            self.timer.stop()
        if self.isPortConnected:
            self.s.close()
        self.sqlObj.closeDatabase()

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    w=AmmoniaMain()
    w.show()
    app.exec_()
        
