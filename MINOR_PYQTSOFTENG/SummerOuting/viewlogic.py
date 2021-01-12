from PyQt5 import QtCore, QtGui, QtWidgets
import viewwindow
import pymysql

class ViewWindow(QtWidgets.QMainWindow, viewwindow.Ui_MainWindow):

    tableSelect = 1

    def __init__(self, parent=None):

        ############################################
        super(ViewWindow, self).__init__(parent)
        self.setFixedSize(662, 465)

        ############################################
        print("Called")
        self.setupUi(self)
        self.displayJ1()
        self.displayJ2()
        self.displayJ3()
        self.displayTotal()

        ############################################
        self.tableWidgetJ1.verticalHeader().setVisible(False);
        self.tableWidgetJ2.verticalHeader().setVisible(False);
        self.tableWidgetJ3.verticalHeader().setVisible(False);
        self.tableWidgetTotal.verticalHeader().setVisible(False);

        self.tableWidgetJ1.setColumnWidth(0, 20)
        self.tableWidgetJ2.setColumnWidth(0, 20)
        self.tableWidgetJ3.setColumnWidth(0, 20)
        self.tableWidgetTotal.setColumnWidth(0, 20)

        self.tableWidgetJ1.setColumnWidth(1, 200)
        self.tableWidgetJ2.setColumnWidth(1, 200)
        self.tableWidgetJ3.setColumnWidth(1, 200)
        self.tableWidgetTotal.setColumnWidth(1, 200)

        # self.dialog=MainWindow(self)
        self.pushButton.clicked.connect(self.backButtonPressed)

    def backButtonPressed(self):
        print("Back Button Pressed")
        #self.dialog=MainWindow(self)
        #self.dialog.show()
        #self.hide()

    def displayJ1(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        with conn.cursor() as cur:
            query = "SELECT * FROM summerouting.judgeonerecord;"
            cur.execute(query)
            value = cur.fetchall()
            rowLen = len(value)
            self.tableSelect = 1
            self.displayTable(value, rowLen)

        conn.close()

    def displayJ2(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        with conn.cursor() as cur:

            query = "SELECT * FROM summerouting.judgetworecord;"
            cur.execute(query)
            value = cur.fetchall()
            rowLen = len(value)
            self.tableSelect = 2
            self.displayTable(value, rowLen)

        conn.close()

    def displayJ3(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        with conn.cursor() as cur:
            query = "SELECT * FROM summerouting.judgethreerecord;"
            cur.execute(query)
            value = cur.fetchall()
            rowLen = len(value)
            self.tableSelect = 3
            self.displayTable(value, rowLen)

        conn.close()

    def displayTotal(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='thesisrecorder')

        with conn.cursor() as cur:
            query = "SELECT * FROM summerouting.masterrecord;"
            cur.execute(query)
            value = cur.fetchall()
            rowLen = len(value)
            self.tableSelect = 4
            self.displayTable(value, rowLen)

        conn.close()

    def displayTable(self, value, rowLen):
        # print(value)

        print("Table Updated")

        if (rowLen != 0):

            if self.tableSelect == 1:
                currTable = self.tableWidgetJ1
                self.tableWidgetJ1.setRowCount(rowLen)
            elif self.tableSelect == 2:
                currTable = self.tableWidgetJ2
                self.tableWidgetJ2.setRowCount(rowLen)
            elif self.tableSelect == 3:
                currTable = self.tableWidgetJ3
                self.tableWidgetJ3.setRowCount(rowLen)
            elif self.tableSelect == 4:
                currTable = self.tableWidgetTotal
                self.tableWidgetTotal.setRowCount(rowLen)

            for i in range(0, len(value)):
                currTable.setItem(i, 0, QtWidgets.QTableWidgetItem(str(value[i][0])))
                currTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(value[i][1])))
                currTable.setItem(i, 2, QtWidgets.QTableWidgetItem(str(value[i][2])))
                currTable.setItem(i, 3, QtWidgets.QTableWidgetItem(str(value[i][3])))
                currTable.setItem(i, 4, QtWidgets.QTableWidgetItem(str(value[i][4])))
                currTable.setItem(i, 5, QtWidgets.QTableWidgetItem(str(value[i][5])))
                currTable.setItem(i, 6, QtWidgets.QTableWidgetItem(str(value[i][6])))
                currTable.setItem(i, 7, QtWidgets.QTableWidgetItem(str(value[i][7])))
                currTable.setItem(i, 8, QtWidgets.QTableWidgetItem(str(value[i][8])))
if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w=ViewWindow()
    w.show()
    sys.exit(app.exec_())