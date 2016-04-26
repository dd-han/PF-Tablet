#from watchServer import site
from flask import Blueprint,render_template
from dbs import sqliteDB 

admin = Blueprint('admin',__name__,
			 template_folder='templates')

@admin.route('/initDB')
def initDB():
    dbConn = sqliteDB()
    dbConn.initTables()

    dbConn = None

    return "OK"
