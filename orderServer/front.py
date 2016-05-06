#from watchServer import site
from flask import Blueprint,render_template,request
from dbs import sqliteDB 
from setting import Shipment,OTPKeys
from pyotp  import TOTP

front = Blueprint('front',__name__,
			 template_folder='templates')
def fetchOrderInfo():
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

            try:
                curItemNum = int(request.form.get('Order-item-'+itemID))
                if curItemNum > 0:
                    orders.append((itemID,itemName,itemPrice,itemPriceUnit,curItemNum))
            except:
                None
                    
    else:
        infos= []
        orders= []

    return (infos,orders)


@front.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        dbConn = sqliteDB()
        onSale = dbConn.getItems(True)
        notAvalaiale = dbConn.getItems(False,False)
        onOrder = dbConn.getItems(False,True)
    
        return render_template('index.html',onSale=onSale,notAva=notAvalaiale,onOrder=onOrder)

    elif request.method == 'POST':
        orderInfos = fetchOrderInfo()

        return render_template('confirm.html',infos=orderInfos[0],orders=orderInfos[1],ship=Shipment,user=OTPKeys)

@front.route('/confirm',methods=['POST'])
def confirm():
    orderInfos = fetchOrderInfo()
    confirmerIDX = request.form.get("ConfirmerIdx")
    confirmerOTP = request.form.get("ConfirmerOTP")

    authedcated = False

    try:
        Confirmer = OTPKeys[int(confirmerIDX)]

        OTP = TOTP(Confirmer[1])
        if (OTP.verify(confirmerOTP)):
            authedcated = True
    except:
        Confirmer = None

    return render_template('makeorder.html',auth=authedcated,infos=orderInfos[0],orders=orderInfos[1],ship=Shipment)
    return str(authedcated)+str(orderInfos)

