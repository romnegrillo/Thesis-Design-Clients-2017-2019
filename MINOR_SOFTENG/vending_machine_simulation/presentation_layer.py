from PyQt5 import QtWidgets,QtGui,QtCore
import sys
import startwindow
import adminwindow
import userwindow
import threading

# This scirpt is the presentation layer.
import application_layer
import data_layer

class StartWindow(QtWidgets.QMainWindow, startwindow.Ui_MainWindow):

    def __init__(self):
        super(StartWindow,self).__init__()
        self.setupUi(self)
        self.sqlObj=data_layer.VendingSQL()
        threading.Thread.__init__(self)

        self.loginButton.clicked.connect(self.loginButtonClicked)
        self.vendingButton.clicked.connect(self.vendingButtonClicked)

    def loginButtonClicked(self):

        username=self.tb1.text()
        password=self.tb2.text()

        if username and not username.isspace() and \
           password and not password.isspace():
            #print(username,password)

            if(self.sqlObj.checkAdmin(username,password)):
                self.adminWindow=AdminWindow()
                self.adminWindow.show()
                self.close()
            else:
                msg=QtWidgets.QMessageBox()

                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Invalid username and/or password.")

                msg.exec_() 
        else:
            msg=QtWidgets.QMessageBox()

            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Invalid username and/or password.")

            msg.exec_()

    def vendingButtonClicked(self):
        self.userWindow=UserWindow()
        self.userWindow.show()
        self.close()
    
class AdminWindow(QtWidgets.QMainWindow, adminwindow.Ui_MainWindow):

    def __init__(self):
        threading.Thread.__init__(self)
        super(AdminWindow,self).__init__()
        self.setupUi(self)
        self.sqlObj=data_layer.VendingSQL()
        self.vendingObj=application_layer.VendingMachine()
        
        self.backButton.clicked.connect(self.backButtonClicked)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.editButton.clicked.connect(self.editButtonClicked)
        self.tableWidget.cellClicked.connect(self.cellClicked)
        self.selectedItem=None
        
        try:
            self.loadItems()
        except Exception as exp:
            print(str(exp))
            
    def backButtonClicked(self):
        self.startWindow=StartWindow()
        self.startWindow.show()
        self.close()

    def loadItems(self):
        
        data=self.sqlObj.loadItems()
        
        if (len(data)>0):
            self.tableWidget.verticalHeader().setVisible(False)
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableWidget.setRowCount(len(data))
            for i,item in enumerate(data):
                for j in range(len(item)):
                    #print(item[j])
                    self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(item[j])))
        else:
            self.tableWidget.setRowCount(0)
            
    def addButtonClicked(self):
        
        item_name=self.tb1.text()
        quantity=self.tb2.text()
        price_per_item=self.tb3.text()

        if(self.vendingObj.isItemNameValid(item_name) and \
           self.vendingObj.isQuantityValid(quantity) and \
           self.vendingObj.isPricePerItemValid(price_per_item)):

            if self.vendingObj.isMoneyValid(int(price_per_item)):
                self.sqlObj.addItems(item_name,quantity,price_per_item)
                self.loadItems()
                self.clearFields()
                msg=QtWidgets.QMessageBox()

                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setWindowTitle("Success")
                msg.setText("Item added.")

                msg.exec_()
            else:
                msg=QtWidgets.QMessageBox()

                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Valid beverage amounts are only 20,50 and 100 only.")



                msg.exec_()
                
        else:
            msg=QtWidgets.QMessageBox()

            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Invalid input.\nItem name must be alphanumeric only.\nQuantity and price must be an integer.")

            msg.exec_()

    def cellClicked(self,row,col):
        self.selectedItem = self.tableWidget.item(row, 0).text()

        itemName=self.tableWidget.item(row, 1).text()
        quantity=self.tableWidget.item(row, 2).text()
        price=self.tableWidget.item(row, 3).text()

        #print(itemName,quantity,price)

        self.tb1.setText(str(itemName))
        self.tb2.setText(str(quantity))
        self.tb3.setText(str(price))
        
    def deleteButtonClicked(self):
        if self.selectedItem is not None:
            self.sqlObj.deleteItem(self.selectedItem)
            self.loadItems()
            self.selectedItem=None
            self.clearFields()

            msg=QtWidgets.QMessageBox()

            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Success")
            msg.setText("Item deleted.")

            msg.exec_()
        else:
            msg=QtWidgets.QMessageBox()

            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Select item to delete.")

            msg.exec_()
    
    def editButtonClicked(self):
        item_name=self.tb1.text()
        quantity=self.tb2.text()
        price_per_item=self.tb3.text()

        if(self.vendingObj.isItemNameValid(item_name) and \
           self.vendingObj.isQuantityValid(quantity) and \
           self.vendingObj.isPricePerItemValid(price_per_item)) and \
           self.selectedItem is not None:

            try:
                self.sqlObj.editItems(self.selectedItem,item_name,quantity,price_per_item)
            except Exception as exp:
                print(str(exp))
            self.loadItems()
            self.clearFields()
            msg=QtWidgets.QMessageBox()

            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Success")
            msg.setText("Item edited.")

            msg.exec_()
        else:
            msg=QtWidgets.QMessageBox()

            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Select item to edit and\or complete all fields.")

            msg.exec_()

    def clearFields(self):
        self.tb1.setText(str(""))
        self.tb2.setText(str(""))
        self.tb3.setText(str(""))

class UserWindow(QtWidgets.QMainWindow, userwindow.Ui_MainWindow):

    def __init__(self):
        threading.Thread.__init__(self)
        super(UserWindow,self).__init__()
        self.setupUi(self)
        self.sqlObj=data_layer.VendingSQL()
        self.vendingObj=application_layer.VendingMachine()
        
        self.backButton.clicked.connect(self.backButtonClicked)
        self.buyButton.clicked.connect(self.buyButtonClicked)
        
        self.loadItems()
        
    def loadItems(self):
        
        data=self.sqlObj.loadItems()
        
        if (len(data)>0):
            self.tableWidget.verticalHeader().setVisible(False)
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableWidget.setRowCount(len(data))
            for i,item in enumerate(data):
                for j in range(len(item)):
                    #print(item[j])
                    self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(item[j])))
        else:
            self.tableWidget.setRowCount(0)
            
    def backButtonClicked(self):
        self.startWindow=StartWindow()
        self.startWindow.show()
        self.close()

    def buyButtonClicked(self):

        try:
            itemCode=self.tb1.text()
            money=self.tb2.text()

            #print(itemCode,money)
        
            if itemCode and not itemCode.isspace() and \
               money and not money.isspace():
                if self.vendingObj.isMoneyValid(money):
                    pass
                else:
                    msg=QtWidgets.QMessageBox()

                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setWindowTitle("Error")
                    msg.setText("Valid paper money amounts are 20,50 and 100 only.")

                    msg.exec_()
                    return

                isValidItem=self.sqlObj.isItemCodeValid(itemCode)
                
                if isValidItem[0]:
                    moneyAmount=int(isValidItem[1])

                    if int(money)>=moneyAmount:
                        change=int(money)-moneyAmount
                        
                        msg=QtWidgets.QMessageBox()

                        if self.sqlObj.vend(itemCode):
                            msg.setIcon(QtWidgets.QMessageBox.Information)
                            msg.setWindowTitle("Success")
                            toDisplay="Vending successful.\nYour change is: "+str(change)
                            msg.setText(toDisplay)

                            msg.exec_()
                        else:
                            msg.setIcon(QtWidgets.QMessageBox.Warning)
                            msg.setWindowTitle("Error")
                            #toDisplay="Vending successful.\nYour change is: "+str(change)
                            msg.setText("Item empty!")

                            msg.exec_()           
                    else:
                        msg=QtWidgets.QMessageBox()

                        msg.setIcon(QtWidgets.QMessageBox.Warning)
                        msg.setWindowTitle("Error")
                        msg.setText("Money not enough.")

                        msg.exec_()
                        return
                else:
                    msg=QtWidgets.QMessageBox()

                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setWindowTitle("Error")
                    msg.setText("Item code is invalid.")

                    msg.exec_()
                
            else:
                msg=QtWidgets.QMessageBox()

                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText("All fields are required.")

                msg.exec_()
        except Exception as exp:
            print(str(exp))

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    w=StartWindow()
    w.show()
    sys.exit(app.exec_())
