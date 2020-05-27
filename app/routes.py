from app import app
from flask import Flask , render_template, request, redirect, url_for,flash, jsonify, make_response
from app.robots import crypto
from app import db
import math


'''
This routes is for Home page and passing some data to home Page

'''
@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    pagination_link_limit = 5
    limit=6
    slider_limit = 3
    ofsset=limit * (page - 1)
    data = db.read_data(ofsset,limit)
    row_num = db.row_count()
    page_num = math.ceil(row_num / limit)
    # pagination page numbers show sort
    maxLeft = (page - math.ceil(pagination_link_limit/2)+1)
    maxRight = (page + math.ceil(pagination_link_limit/2)-1)
    if maxLeft < 1 :
        maxLeft = 1
        maxRight = pagination_link_limit
    if maxRight > page_num:
        maxLeft = page_num - (pagination_link_limit - 1)
        maxRight = page_num
        if maxLeft < 1:
            maxLeft = 1

    slider_data = db.read_data_for_slider(slider_limit)
    ip_address = request.remote_addr# getting ip address
    db.insert_ip(ip_address)# inserting ip address
    ip = db.read_ip()
    return render_template('index.html',data=data, page_num=page_num, slider_data=slider_data, ip=ip,
    maxLeft=maxLeft,maxRight=maxRight)

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

@app.route('/arzdigital')
def arzdigital():
    return render_template('digital.html')