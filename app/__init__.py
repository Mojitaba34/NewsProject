from flask import Flask
import db
import robots
app = Flask(__name__)

db.BuildTables() # First Step Check exists and build Tables Database

# This is For test robto
# TODO: __init__ file for robot
"""
arzdigital = robots.news_from_arzdigital()
tasnim = robots.news_from_tasnimnews()
tejarat = robots.news_from_tejaratnews()
"""

from app import routes # route import 
from app.admin.routes import admin # admin route import
app.register_blueprint(admin,url_prefix='/admin') # add admin route with blueprint