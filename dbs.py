import sqlite3
import setting as sets

class sqliteDB:
    needCommit = False
    connection = None

    def __init__(this):
        this.connection = sqlite3.connect(sets.sqliteFile)

    def __del__(this):
        if this.needCommit:
            this.connection.commit()
        this.connection.close

    def forceCommit(this):
        this.connection.commit()
        needCommit = False
    
    def initTables(this):
        cursor = this.connection.cursor()
        cursor.execute('CREATE TABLE items(\
            ID INTEGER PRIMARY KEY NOT NULL, Name TEXT NOT NULL UNIQUE, \
            Image TEXT, Price INTEGER NOT NULL, PriceUnit, ContTEXT, \
            OnSale BOOLEAN, canOrder BOOLEAN)')

    def lookupMaxID(this):
        cursor = this.connection.cursor()
        cursor.execute('SELECT ID FROM items ORDER BY ID DESC LIMIT 1')
        currentMaxItem = cursor.fetchone()
        if currentMaxItem == None:
            return 0
        else:
            return currentMaxItem[0]

    
    def insertItem(this,name,Price,PriceUnit='',Image = '',OnSale=False,CanOrder=False,ContTEXT=''):
        currentMaxID = this.lookupMaxID()
        print(currentMaxID)

        vals = ( currentMaxID+1, name, int(Price),Image,bool(OnSale),bool(CanOrder), PriceUnit, ContTEXT )
        cursor = this.connection.cursor()
        cursor.execute('INSERT INTO items (ID, Name, Price, Image, OnSale, canOrder, PriceUnit, ContTEXT) VALUES (?,?,?,?,?,?,?,?)', vals)
        this.needCommit = True

    def getItems(this,OnSale,CanOrder = None):
        vals = [OnSale]
        if CanOrder != None:
            vals.append(CanOrder)
            sqlext = 'and canOrder = ?'
        else:
            sqlext = ''
        
        cursor = this.connection.cursor()
        cursor.execute('SELECT ID, Name, Image, Price, PriceUnit, ContTEXT FROM items WHERE OnSale = ? '+sqlext,vals)

        return cursor.fetchall()

