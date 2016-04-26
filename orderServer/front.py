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

    onSale = [1,3,5,7,9]
    notAvalaiale = [51]
    onOrder = [33]
    
    return render_template('index.html',onSale=onSale,notAva=notAvalaiale,onOrder=onOrder)
