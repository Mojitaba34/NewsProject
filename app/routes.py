from app import app
from flask import Flask , render_template
from app.robots import news_from_arzdigital, news_from_tasnimnews, news_from_tejaratnews

'''
This view is for Home page and passing some data to home Page

'''
@app.route('/')
def home():
    test = news_from_tejaratnews()
    return render_template('index.html',temp=test.return_dic())
