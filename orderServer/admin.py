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
        return render_template('OTP-Auth.html',user=OTPKeys)
    else:
        UID = request.form.get('UserID')
        OTP = request.form.get('OTP')
        if auth(UID,OTP,'initDB'):
            dbConn = sqliteDB()
            dbConn.initTables()
        
            return "OK"
        else:
            return render_template('OTP-Auth.html',authFail=True),401

