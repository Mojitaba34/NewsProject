from flask import (Flask,Blueprint,render_template,request,flash,redirect,url_for,Response,session)
from app.admin import db
from app.admin import config
from app.admin import api
from datetime import timedelta

admin = Blueprint('admin',
                    __name__,
                    template_folder="templates",
                    static_folder="static",
                    static_url_path='/admin/static')



admin.secret_key = config.SECRET_KET
admin.permanent_session_lifetime = timedelta(minutes=30)


"""
This Method get All Data From Db for Admin Panel
"""
def getData():
    All_News = db.getCount_AllNews()
    News_Data= db.get_NewsData()
    Btc_Price = api.get_BTCPrice()

    dashboard_data = {"All_News":All_News,"BTCPrice":Btc_Price,"NewsData":News_Data}
    return dashboard_data

from app.admin import routes