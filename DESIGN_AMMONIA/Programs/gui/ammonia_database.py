import sqlite3
import time

class AmmoniaDatabase:

    def __init__(self,dbName):
        self.dbName=dbName

    def createDatabase(self):
        query="CREATE TABLE records(id INT PRIMARY KEY, ammonia REAL, " + \
               "pH REAL, temp REAL, time TEXT);"
        self.conn=sqlite3.connect(self.dbName)
        self.curr=self.conn.cursor()
        self.curr.execute(query)
        self.conn.commit()
        
    def connectDatabase(self):
        self.conn=sqlite3.connect(self.dbName)
        self.curr=self.conn.cursor()

    def closeDatabase(self):
        self.curr.close()
        self.conn.close()

    def addData(self,ammonia,pH,temp):

        # Counting id and adding one will have conflicts.
        # Get the highest id first and add one to it. Use that id.
        query="SELECT id FROM records ORDER BY id DESC;"
        self.curr.execute(query)
        data=self.curr.fetchall()

        if len(data):
            ID=data[0][0]
            ID=ID+1
        else:
            ID=1

        timeNow=time.strftime("%I:%M %p %m/%d/%y",time.localtime())
            
        query="INSERT INTO records(id, ammonia,pH,temp,time) " + \
               "VALUES(?,?,?,?,?);"
        self.curr.execute(query,(ID,ammonia,pH,temp,timeNow))
        self.conn.commit()

        return True
        

    def getData(self):
        query="SELECT ammonia,pH,temp,time FROM records ORDER BY id DESC;"
        self.curr.execute(query)
        data=self.curr.fetchall()

        return data
    
    def getDataAtDate(self,date):
        query="SELECT ammonia,pH,temp,time from records WHERE SUBSTR(time,10)=?;"
        self.curr.execute(query,(date,))
        data=self.curr.fetchall()
        
        return data

    def clearDatabase(self):
        query="DELETE FROM records;"
        self.curr.execute(query)
        self.conn.commit()


# For testing only.
if __name__=="__main__":

    sqlObj=AmmoniaDatabase("./database/ammonia.db")
    #sqlObj.createDatabase()
    sqlObj.connectDatabase()
    data=sqlObj.getDataAtDate("02/11/19")

    if data:
        for i in data:
            ID=i[0]
            ammonia=i[1]
            pH=i[2]
            temp=i[3]
            timeRecorded=i[4]
            print(timeRecorded)
    #sqlObj.addData(0.003,7.53,26.23)
    #sqlObj.getData()
    sqlObj.closeDatabase()
    
    

    
