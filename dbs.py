import sqlite3
import setting as sets

class sqliteDB:
    needCommit = False
    connection = None

    def __init__(self):
        self.connection = sqlite3.connect(sets.sqliteFile)

    def __del__(self):
        if self.needCommit:
            self.connection.commit()
        self.connection.close

    def forceCommit(self):
        self.connection.commit()
    
    def initTables(self):
        cursor = self.connection.cursor()
        cursor.execute('CREATE TABLE items(\
                ID INTEGER PRIMARY KEY NOT NULL, \
                Name TEXT NOT NULL, \
                Price INTEGER NOT NULL, \
                OnSale BOOLEAN, \
                canOrder BOOLEAN)')

