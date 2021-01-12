from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import Ui_MainWindow
import pymysql
import numpy as np
import viewwindow
from tkinter import Tk,messagebox

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

     print("Connection Created")

     def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setStyleSheet("#MainWindow\n"
"{\n"
"background-color: qconicalgradient(cx:1, cy:0.966, angle:0, stop:0 rgba(10, 90, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"}")
        self.candidateCB.currentTextChanged.connect(self.candidateCBChanged)
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.pushButton_2.clicked.connect(self.pushButton_2Clicked)
        self.setFixedSize(712, 411)
        self.updateMasterRecord()

     def candidateCBChanged(self, value):
         print(len(value))
         if value=="SAMANTHA TANQUECO":
            self.graphicsView.setStyleSheet("#graphicsView\n"
"{\n"
"background-image: url(\"images/candidates_resized/samantha.jpg\");\n"
"background-position: center; \n"
"background-repeat: no-repeat;\n"
"}")
         elif value=="BRIDALYN BEJERAS":
            self.graphicsView.setStyleSheet("#graphicsView\n"
"{\n"
"background-image: url(\"images/candidates_resized/bejeras.jpg\");\n"
"background-position: center; \n"
"background-repeat: no-repeat;\n"
"}")
         elif value=="CHRISTINE LOISSE ALBOS":
            self.graphicsView.setStyleSheet("#graphicsView\n"
"{\n"
"background-image: url(\"images/candidates_resized/albos.jpg\");\n"
"background-position: center; \n"
"background-repeat: no-repeat;\n"
"}")
         elif value=="DWIGHT TAGAPULOT":
            self.graphicsView.setStyleSheet("#graphicsView\n"
"{\n"
"background-image: url(\"images/candidates_resized/tagapulot.jpg\");\n"
"background-position: center; \n"
"background-repeat: no-repeat;\n"
"}")
         elif value=="JOHN MEDINA":
            self.graphicsView.setStyleSheet("#graphicsView\n"
"{\n"
"background-image: url(\"images/candidates_resized/medina.jpg\");\n"
"background-position: center; \n"
"background-repeat: no-repeat;\n"
"}")
         elif value=="CHRYSTOPHER ONG":
            self.graphicsView.setStyleSheet("#graphicsView\n"
"{\n"
"background-image: url(\"images/candidates_resized/ong.jpg\");\n"
"background-position: center; \n"
"background-repeat: no-repeat;\n"
"}")
         elif value=="EARL ZUNEGA":
            self.graphicsView.setStyleSheet("#graphicsView\n"
"{\n"
"background-image: url(\"images/candidates_resized/zunega.jpg\");\n"
"background-position: center; \n"
"background-repeat: no-repeat;\n"
"}")
         elif value=="CARL FRANCIS REYES":
            self.graphicsView.setStyleSheet("#graphicsView\n"
"{\n"
"background-image: url(\"images/candidates_resized/reyes.jpg\");\n"
"background-position: center; \n"
"background-repeat: no-repeat;\n"
"}")
         elif value=="JUMARIE MOCON":
            self.graphicsView.setStyleSheet("#graphicsView\n"
"{\n"
"background-image: url(\"images/candidates_resized/mocon.jpg\");\n"
"background-position: center; \n"
"background-repeat: no-repeat;\n"
"}")

     # Insert Button
     def pushButtonClicked(self):
          print("Update Button Clicked!")

          if self.judgeCB.currentText() and \
             not self.judgeCB.currentText().isspace() and \
             self.candidateCB.currentText() and \
             not self.candidateCB.currentText().isspace() and \
             self.catCB.currentText() and \
             not self.catCB.currentText().isspace() and \
             self.scoreTextbox.text() and \
             not self.scoreTextbox.text().isspace() and \
             self.scoreTextbox.text().isdigit():

              valid = False

              try:
                  score = float(self.scoreTextbox.text())

                  if (0 <= score <= 100):
                      valid = True
                  else:
                      messagebox.showinfo("Error", "Score in between 0 and 100 only!")
              except:
                  messagebox.showinfo("Error", "Invalid input!")


              if(valid):
                  judge = self.judgeCB.currentText()
                  cand=self.candidateCB.currentText()
                  cat=self.catCB.currentText()
                  score=self.scoreTextbox.text()

                  myDict={"SAMANTHA TANQUECO":1,
                          "BRIDALYN BEJERAS":2,
                          "CHRISTINE LOISSE ALBOS":3,
                          "DWIGHT TAGAPULOT":4,
                          "JOHN MEDINA":5,
                          "CHRYSTOPHER ONG":6,
                          "EARL ZUNEGA":7,
                          "CARL FRANCIS REYES":8,
                          "JUMARIE MOCON":9
                          }

                  conn = pymysql.connect(host='localhost',
                                         user='root',
                                         password='toor',
                                         db='summerouting')

                  with conn.cursor() as curr:

                       if(judge=="JUDGE NO. 1"):
                           print("Judge 1")

                           query="UPDATE summerouting.judgeonerecord " + \
                                 "SET `%s`= %s WHERE `ID`=%s;"%(cat,score,myDict[cand])
                           curr.execute(query)
                           conn.commit()

                           query="SELECT * FROM summerouting.judgeonerecord WHERE `ID`=%s;"
                           curr.execute(query, (myDict[cand]))
                           result=curr.fetchall()
                           result=np.array(result)
                           result=np.array(result[:,2:],dtype=float)
                           print(result)

                           for item in result:
                               total = item[0] * 0.15 + item[1] * 0.15 + item[2] * 0.30 + item[3] * 0.30 + item[4] * 0.05 + \
                                       item[5] * 0.05;
                               query = "UPDATE summerouting.judgeonerecord " + \
                                       "SET `Total`= %s WHERE `ID`=%s;" % (total, myDict[cand])
                               print(query)
                               curr.execute(query)
                               conn.commit()

                       elif(judge=="JUDGE NO. 2"):
                            print("Judge 2")

                            query = "UPDATE summerouting.judgetworecord " + \
                                    "SET `%s`= %s WHERE `ID`=%s;" % (cat, score, myDict[cand])
                            curr.execute(query)
                            conn.commit()

                            query = "SELECT * FROM summerouting.judgetworecord WHERE `ID`=%s;"
                            curr.execute(query, (myDict[cand]))
                            result = curr.fetchall()
                            result = np.array(result)
                            result = np.array(result[:, 2:], dtype=float)
                            print(result)

                            for item in result:
                                total = item[0] * 0.15 + item[1] * 0.15 + item[2] * 0.30 + item[3] * 0.30 + item[4] * 0.05 + \
                                        item[5] * 0.05;
                                query = "UPDATE summerouting.judgetworecord " + \
                                        "SET `Total`= %s WHERE `ID`=%s;" % (total, myDict[cand])
                                print(query)
                                curr.execute(query)
                                conn.commit()

                       elif(judge=="JUDGE NO. 3"):
                            print("Judge 3")

                            query = "UPDATE summerouting.judgethreerecord " + \
                                   "SET `%s`= %s WHERE `ID`=%s;" % (cat, score, myDict[cand])
                            curr.execute(query)
                            conn.commit()

                            query = "SELECT * FROM summerouting.judgethreerecord WHERE `ID`=%s;"
                            curr.execute(query, (myDict[cand]))
                            result = curr.fetchall()
                            result = np.array(result)
                            result = np.array(result[:, 2:], dtype=float)
                            print(result)

                            for item in result:
                                total = item[0] * 0.15 + item[1] * 0.15 + item[2] * 0.30 + item[3] * 0.30 + item[4] * 0.05 + \
                                      item[5] * 0.05;
                                query = "UPDATE summerouting.judgethreerecord " + \
                                      "SET `Total`= %s WHERE `ID`=%s;" % (total, myDict[cand])
                                print(query)
                                curr.execute(query)
                                conn.commit()

                  self.updateMasterRecord()
                  conn.close()

                  messagebox.showinfo("Success", "Database updated!")

          else:
              messagebox.showinfo("Error", "Invalid input!")



     def updateMasterRecord(self):

         conn = pymysql.connect(host='localhost',
                                user='root',
                                password='toor',
                                db='summerouting')

         with conn.cursor() as curr:
             query="SELECT * FROM summerouting.judgeonerecord;"
             curr.execute(query)
             res1=np.array(curr.fetchall())

         with conn.cursor() as curr:
             query="SELECT * FROM summerouting.judgetworecord;"
             curr.execute(query)
             res2=curr.fetchall()

         with conn.cursor() as curr:
             query="SELECT * FROM summerouting.judgethreerecord;"
             curr.execute(query)
             res3=curr.fetchall()

         res1=np.array(res1)
         res2=np.array(res2)
         res3=np.array(res3)

         res1 = np.array(res1[:, 2:], dtype=float)
         res2 = np.array(res2[:, 2:], dtype=float)
         res3 = np.array(res3[:, 2:], dtype=float)

         final=(res1+res2+res3)/3.0

         id=1

         for item in final:

             total = item[0]*0.15 + item[1]*0.15 + item[2]*0.30 + item[3]*0.30 + item[4]*0.05 + item[5]*0.05;

             with conn.cursor() as curr:
                 query = "UPDATE summerouting.masterrecord SET `Popularity Tickets`=%s, " + \
                          "`Event Tickets`=%s, " + \
                          "`Theme Wear`=%s, " + \
                          "`Swim Wear`=%s, " + \
                          "`Confidence`=%s, " + \
                          "`Audience Impact`=%s, " + \
                          "`Total`=%s " + \
                          "WHERE `ID`=%s"

                 curr.execute(query,(float(item[0]),float(item[1]),float(item[2]),float(item[3]), float(item[4]), float(item[5]), float(total),int(id)))
                 conn.commit()

             id=id+1

         conn.close()
         #print(final)

     def pushButton_2Clicked(self):
         self.openMainWindow()

     def openMainWindow(self):
        print("View Window Open")
        self.dialog = ViewWindow(self)
        self.dialog.show()
        self.hide()

     @staticmethod
     def backtoMain(self):
         self.show()

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
        self.dialog=MainWindow(self)
        self.dialog.show()
        self.hide()

    def displayJ1(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='toor',
                               db='summerouting')

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
                               db='summerouting')

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
                               db='summerouting')

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
                               db='summerouting')

        with conn.cursor() as cur:
            query = "SELECT * FROM summerouting.masterrecord ORDER BY `Total` DESC;"
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
    w=MainWindow()
    w.show()
    sys.exit(app.exec_())