from flask import (Flask,Blueprint,render_template,request,flash,redirect,url_for,Response,session)
from app.admin import db
from app.admin import config
from app.admin import api
from datetime import timedelta

admin = Blueprint('admin',
                    __name__,
                    template_folder="templates",
                    static_folder="static",
                    static_url_path='/static')



admin.secret_key = config.SECRET_KEY
admin.permanent_session_lifetime = timedelta(minutes=10)



def getData():
    """
    This Method get All Data From Db for Admin Panel
    """
    All_News = db.getCount_AllNews()
    News_Data= db.get_NewsData()
    Btc_Price = api.get_BTCPrice()
    CountTodayNews = db.getCount_TodayNews()
    CountTodayVisitors = db.getCount_TodayVisitors()

    dashboard_data = {"All_News":All_News,"BTCPrice":Btc_Price,"NewsData":News_Data,"CountTodayNews":CountTodayNews,"CountTodayVisitors": CountTodayVisitors}
    return dashboard_data

from app.admin import routes