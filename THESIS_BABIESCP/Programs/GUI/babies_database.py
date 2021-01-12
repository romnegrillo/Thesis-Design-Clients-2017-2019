import sqlite3
import time


class BabiesDatabase:

    def __init__(self, dbName):
        self.dbName = dbName

    def connectDB(self):
        self.conn = sqlite3.connect(self.dbName)
        self.curr = self.conn.cursor()

    def createDB(self):
        query = "CREATE TABLE records(id INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT, " + \
            "left_hand REAL, right_hand REAL, " + \
            "left_foot REAL, right_foot REAL);"
        self.curr.execute(query)
        self.conn.commit()

    def addDataDB(self, left_hand, right_hand, left_foot, right_foot):
        query = "INSERT INTO records(time, left_hand, right_hand, " + \
            "left_foot, right_foot) VALUES(?,?,?,?,?);"

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        self.curr.execute(query, (now, left_hand, right_hand, left_foot, right_foot))
        self.conn.commit()

    def getDataDB(self):
        query = "SELECT time,left_hand,right_hand,left_foot,right_foot FROM records ORDER BY time DESC;"
        self.curr.execute(query)
        data = self.curr.fetchall()

        return data

    def clearDB(self):
        query = "DELETE FROM records;"
        self.curr.execute(query)
        self.conn.commit()

    def closeDB(self):
        self.curr.close()
        self.conn.close()


if __name__ == "__main__":
    # For testing purposes only.

    test = BabiesDatabase("babies_records.db")
    test.connectDB()
    # test.createDB()
    test.addDataDB(1, 2, 3, 33.45)
    print(test.getDataDB())
