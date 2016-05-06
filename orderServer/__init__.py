# -*- coding: utf-8 -*-
# orderServer init file 
# some debug code of server like update/restart code

from flask import Flask
from orderServer.front import front
from orderServer.admin import admin

site = Flask(__name__)

#import orderServer.index
site.register_blueprint(front)
site.register_blueprint(admin,url_prefix='/admin')
