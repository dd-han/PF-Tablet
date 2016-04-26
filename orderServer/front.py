#from watchServer import site
from flask import Blueprint,render_template
from dbs import sqliteDB 

front = Blueprint('front',__name__,
			 template_folder='templates')

@front.route('/')
def index():
    dbConn = sqliteDB()

    #print('dbConn = None')
    #dbConn = None

    onSale = dbConn.getItems(True)
    notAvalaiale = dbConn.getItems(False,False)
    onOrder = dbConn.getItems(False,True)
    
    return render_template('index.html',onSale=onSale,notAva=notAvalaiale,onOrder=onOrder)
