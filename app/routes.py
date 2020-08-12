from app import app
from flask import Flask , render_template, request, redirect, url_for,flash, jsonify, make_response
from app.robots.robots import crypto
from app.admin import db
import math, json
from app.admin import config
import readtime
import math


'''
This routes is for Home page and passing some data to home Page

'''
@app.route('/', methods=["GET", "POST"])
@app.route('/home')
def home():
    
    limit=6
    limit_corona = 8
    row_num = db.row_count()
    page_num = math.ceil(row_num / limit)
    if int(request.args.get('page', 1, type=int)) > page_num:
        return render_template('404.html')
    page = request.args.get('page', 1, type=int)
    pagination_link_limit = 5
    slider_limit = 3
    ofsset=limit * (page - 1)
    ofsset_corona=limit_corona * (page - 1)
    data = db.read_data(ofsset,limit)# reading data from data base to insert in news section
    Corona_data = db.read_data_Corona_news(ofsset_corona,limit_corona)
    row_num = db.row_count()
    page_num = math.ceil(row_num / limit)# getting page numbers for creating pagination
    # pagination page numbers show sort
    maxLeft = (page - math.ceil(pagination_link_limit/2)+1)# max Left pages number show from active page
    maxRight = (page + math.ceil(pagination_link_limit/2)-1)# max Right pages number show from active page
    if maxLeft < 1 :
        maxLeft = 1
        maxRight = pagination_link_limit
    if maxRight > page_num:
        maxLeft = page_num - (pagination_link_limit - 1)
        maxRight = page_num
        if maxLeft < 1:
            maxLeft = 1

    slider_data = db.read_data_for_slider(slider_limit)
    ip_address = request.environ['REMOTE_ADDR']# getting ip address
    db.insert_ip(ip_address)# inserting ip address
    print(db.ip_date_update(ip_address)) # update ip Date
    arzdigital_news = db.arzdigital_news()
    return render_template('index.html', data=data, arzdigital=arzdigital_news,page_num=page_num, slider_data=slider_data,
    maxLeft=maxLeft,maxRight=maxRight,configId=config.USERID_GOOGLE,corona_data=Corona_data)

@app.route('/about')
def about_us():
    return render_template('about.html')

@app.route('/contact', methods=["POST","GET"])
def contact_us():
    if request.method == "POST":
        username=request.form["name"]
        email=request.form["email"]
        subject=request.form["subject"]
        comment=request.form["comment"]
        if db.Insertcomment(username,email,subject,comment) == True:
            flash('your comment was submitted successfully','success')
    return render_template('contact.html')

@app.route('/arzdigital', methods=["GET", "POST"])
def arzdigital():
    return render_template('digital.html')

@app.route('/_pricesData', methods=["GET","POST"])
def getdata():
    price_data = crypto()
    data = price_data.get_data()
    return data


@app.route('/<slug>',methods=["GET"])
def landing(slug):
    data = db.check_slug(slug)
    for post in data:
        text = post[2]
    time = readtime.of_text(text)
    min = int(time.seconds) / 60
    return render_template('landing.html',data=data,time_read=str(math.floor(min)))