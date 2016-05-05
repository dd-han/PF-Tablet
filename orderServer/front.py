#from watchServer import site
from flask import Blueprint,render_template,request
from dbs import sqliteDB 

front = Blueprint('front',__name__,
			 template_folder='templates')

@front.route('/',methods=['GET','POST'])
def index():

    if request.method == 'GET':
        dbConn = sqliteDB()
        onSale = dbConn.getItems(True)
        notAvalaiale = dbConn.getItems(False,False)
        onOrder = dbConn.getItems(False,True)
    
        return render_template('index.html',onSale=onSale,notAva=notAvalaiale,onOrder=onOrder)

    elif request.method == 'POST':
        Name = request.form.get("Name")
        Address = request.form.get("Address")
        Phone = request.form.get("Phone")
        
        infos = (Name,Address,Phone)
        orders = []
        if Name != '' and Address != '' and Phone != '':
            dbConn = sqliteDB()
            onOrder = dbConn.getItems(False,True)
            for i in onOrder:
                itemID = str(i[0])
                itemName = i[1]
                itemPrice = i[3]
                itemPriceUnit = i[4]

                curItemNum = int(request.form.get('Order-item-'+itemID))
                if curItemNum > 0:
                    orders.append((itemID,itemName,itemPrice,itemPriceUnit,curItemNum))
        else:
            infos= []
            orders= []

        return render_template('confirm.html',infos=infos,orders = orders)

