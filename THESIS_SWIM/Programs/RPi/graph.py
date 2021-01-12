from PyQt5 import QtCore, QtGui, QtWidgets
from guidatagraph import Ui_MainWindow
import sys
import os
import matplotlib.pyplot as plt
plt.style.use('ggplot')

class MainLogic(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        self.updateListBox()
        self.pushButton.clicked.connect(self.graphClicked)
        self.pushButton_2.clicked.connect(self.closeClicked)
 
    def updateListBox(self):
        self.listWidget.clear()
        
        fileList=os.listdir("Records")

        for item in fileList:
            self.listWidget.addItem(str(item))

    def closeClicked(self):
        self.close()

    def graphClicked(self):

        try:
            filename=self.listWidget.currentItem().text()
                #print(filename)

            with open("Records/"+filename) as file:
                contents=file.readlines()

                #print(contents)

            phValueList=[]
            ORPValueList=[]
            timeValueList=[]
            timeValueWithoutNewLine=[]
            
            for item in contents:
                indexOfBar=[i for i,x in enumerate(item) if x=="-"]
                phValueList.append(float(item[0:indexOfBar[0]]))
                ORPValueList.append(float(item[indexOfBar[0]+1:indexOfBar[1]]))
                timeValueList.append(item[indexOfBar[1]+1:])
                 
            for item in timeValueList:
                #timeValueWithoutNewLine.append(''.join(list(item).remove("\n")))
                timeValueWithoutNewLine.append(item.replace("\n",""))
                
            print(timeValueWithoutNewLine)
            
            plt.figure(1)
            plt.ylabel("pH Value")
            plt.title("Graph of pH Value WRT Time")
            plt.plot(phValueList)
       

            plt.figure(2)
            plt.ylabel("ORP Value")
            plt.title("Graph of ORP Value WRT Time")
            plt.plot(ORPValueList)
            
            plt.show()
            
        except:
            print("Invalid file selected or cannot graph seleced file.")
            
def main():
    app = QtWidgets.QApplication(sys.argv)
    w=MainLogic()
    w.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
