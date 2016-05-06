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
        this.initOrderTable()
        this.initOrderDetailTable()

    def initOrderTable(this):
        cursor = this.connection.cursor()
        cursor.execute('CREATE TABLE Orders(\
            OrderNumber INTEGER PRIMARY KEY NOT NULL, \
            Name TEXT NOT NULL, Address TEXT NOT NULL, Phone TEXT NOT NULL, \
            shippment INTEGER)')

    def initOrderDetailTable(this):
        cursor = this.connection.cursor()
        cursor.execute('CREATE TABLE OrdersDetail(\
            OrderNumber INTEGER NOT NULL, \
            ID INTEGER NOT NULL, ItemAmout INTEGER, PRIMARY KEY (OrderNumber,ID))')

    def insertOrder(this,orderNumber,ship,info,items):
        cursor = this.connection.cursor()
        this.needCommit = True
        data = [orderNumber,info[0],info[1],info[2],ship]
        cursor.execute('INSERT INTO Orders (OrderNumber,Name,Address,Phone,shippment) VALUES (?,?,?,?,?);',data)
        for i in items:
            data = [orderNumber,i[0],i[4]]
            cursor.execute('INSERT INTO OrdersDetail (OrderNumber,ID,ItemAmout) VALUES (?,?,?);',data)
        
    def lookupMaxOrderID(this):
        cursor = this.connection.cursor()
        cursor.execute('SELECT OrderNumber FROM Orders ORDER BY OrderNumber DESC LIMIT 1')
        currentMaxItem = cursor.fetchone()
        if currentMaxItem == None:
            return None
        else:
            return currentMaxItem[0]

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

class orderDB:
    sqlCon = None
    needCommit = False
    numFormater = "{:0>3d}"
    numLength = 3
    from setting import t_format, csvOrderLocate
    from time import strftime, localtime as now

    def __init__(this):
        this.sqlCon = sqliteDB()

    def __del__(this):
        if this.needCommit:
            this.sqlCon.forceCommit()


    def genOrderNum(this):
        curOrder = str(this.sqlCon.lookupMaxOrderID())
        if (curOrder == "None"):
            return this.strftime(this.t_format,this.now()) + '0'*this.numLength
        else :
            curDateTime = this.strftime(this.t_format,this.now())
            lastDate = curOrder[:-this.numLength]
            lastNum = int(curOrder[-this.numLength:])
            sameDate = True
            for idx,val in enumerate(curDateTime):
                if val != lastDate[idx]:
                    sameDate = False
                    break
            if sameDate:
                nextNum = str(curNum + 1)
                if len(nextNum) >= this.numLength:
                    ## if more than 100 order in 1 Second, there will have some problem!!
                    print("ERROR: Too many order!!")
                    return None
                else:
                    return curDate + nextNum
            else:
                return this.strftime(this.t_format,this.now()) + '0'*this.numLength

    def insertOrder(this,orderNumber,ship,info,items):
        this.sqlCon.insertOrder(orderNumber,ship,info,items)
        this.sqlCon.forceCommit()
        this.insertToCSV(orderNumber,ship,info,items)

    def insertToCSV(this,orderNumber,ship,info,items):
        import csv
        with open(this.csvOrderLocate,'a',newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter="\t",quotechar='"', quoting=csv.QUOTE_MINIMAL)
            shippment = ship
            for i in items:
                csvwriter.writerow([orderNumber,info[0],info[1],info[2],i[0],i[1],i[2],i[4],shippment])
                shippment = 0

