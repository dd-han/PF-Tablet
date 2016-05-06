#from watchServer import site
from flask import Blueprint,render_template,request
from dbs import sqliteDB 
from setting import OTPKeys

admin = Blueprint('admin',__name__,
			 template_folder='templates')

def auth(userID,OTP,path = 'Unknow'):
    from pyotp import TOTP
    from setting import OTPAdminLOG, Log_t_format
    from time import strftime, localtime as now

    User = OTPKeys[int(userID)]
    OTPi = TOTP(User[1])
    f = open(OTPAdminLOG,'a')
    if (OTPi.verify(OTP)):
        f.writelines( strftime(Log_t_format,now())+"\t"+path+"\tAuthencate Successful\n" )
        f.close()
        return True
    else:
        f.writelines( strftime(Log_t_format,now())+"\t"+path+"\tAuthencate Failed!!!!\n" )
        f.close()
        return False

@admin.route('/initDB',methods=['GET','POST'])
def initDB():
    if request.method == 'GET':
        return render_template('admin-Auth.html',user=OTPKeys)
    else:
        UID = request.form.get('UserID')
        OTP = request.form.get('OTP')
        if auth(UID,OTP,'initDB'):
            dbConn = sqliteDB()
            dbConn.initTables()
        
            return "OK"
        else:
            return render_template('admin-Auth.html',authFail=True),401

@admin.route('/list',methods=['GET','POST'])
def list():
    if request.method == 'GET':
        return render_template('admin-Auth.html',user=OTPKeys)
    else:
        UID = request.form.get('UserID')
        OTP = request.form.get('OTP')
        if auth(UID,OTP,'list'):
            return render_template('admin-Auth.html',authFail=True),401
        else:
            dbConn = sqliteDB()
            orders = dbConn.listOrders()
            newOrders = []
            for idx,val in enumerate(orders):
                ssum = 0
                ssum = ssum + val[4]
                
                newOrders.append([])
                for j in val:
                    newOrders[idx].append(j)

                lookup = dbConn.listDetailOrder(val[0])
                lookupDetail = []
                for idx2,val2 in enumerate(lookup):
                    itemInfo = dbConn.getItem(val2[1])

                    ssum = ssum + ( itemInfo[3] * val2[2] )
                    lookupDetail.append([])
                    lookupDetail[idx2].append(val2[2])
                    for val3 in itemInfo:
                        lookupDetail[idx2].append(val3)

                newOrders[idx].append(ssum)
                newOrders[idx].append(lookupDetail)
        
            return render_template('admin-listOrder.html',orders=newOrders)
            return str(newOrders)

