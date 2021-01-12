import sqlite3
import random

class VendingSQL:

    def __init__(self):
        self.conn=sqlite3.connect("vending_machine.db")
        self.cursor=self.conn.cursor()
        
    def checkAdmin(self,username,password):
        query="SELECT * FROM admin WHERE username=? and password=?;"
        self.cursor.execute(query,(username,password))
        result=self.cursor.fetchall()

        if(len(result)>0):
            return True

        return False

    def loadItems(self):
        query="SELECT * FROM product_list;"
        data=[]
        self.cursor.execute(query)
        result=self.cursor.fetchall()

        if(len(result)):
            for item in result:
                data.append(item)
            return data

        return data

    def addItems(self,item_name,quantity,price_per_item):        
        query="SELECT id FROM product_list ORDER BY id DESC;"
        self.cursor.execute(query)
        data=self.cursor.fetchall()
        newID="A1"
        
        if len(data)>0:
            itemIDInDB=str(data[0][0])
            itemNum=itemIDInDB[1:]
            itemNum=int(itemNum)+1
            newID="A"+str(itemNum)

        query="INSERT INTO product_list(id,name,quantity,price) VALUES(?,?,?,?);"
        self.cursor.execute(query,(newID,item_name,quantity,price_per_item))
        self.conn.commit()

    def deleteItem(self,item_id):
        query="DELETE FROM product_list WHERE id=?;"
        self.cursor.execute(query,(item_id,))
        self.conn.commit()

    def editItems(self,item_id,item_name,quantity,price_per_item):
        query="UPDATE product_list SET name=?, quantity=?, price=? " + \
               "WHERE id=?;"
        self.cursor.execute(query,(item_name,quantity,price_per_item,item_id))
        self.conn.commit()

    def isItemCodeValid(self,itemCode):
        query="SELECT * from product_list WHERE id=?"
        self.cursor.execute(query,(itemCode,))
        data=self.cursor.fetchall()

        if len(data)>0:
            return True,data[0][3]

        return False,0

    def getTotalOfItem(self,itemCode):
        query="SELECT quantity FROM product_list WHERE id=?;"
        self.cursor.execute(query,(itemCode,))

        result=self.cursor.fetchall()

        if len(result)>0:
            return result[0][0]

        return 0
        
    def vend(self,itemCode):

        remaining=self.getTotalOfItem(itemCode)
        
        if(remaining>0):
            remaining=remaining-1;
            query="UPDATE product_list SET quantity=? WHERE id=?;"
            self.cursor.execute(query,(remaining,itemCode))
            self.conn.commit()
            return True
        return False
             
test=VendingSQL()
print(test.vend("A2"))
