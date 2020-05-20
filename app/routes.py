from app import app
from flask import Flask , render_template, request, redirect, url_for,flash
from app.robots import crypto
from app import db
import math

'''
This routes is for Home page and passing some data to home Page

'''
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    limit=6
    slider_limit = 3
    ofsset=limit * (page - 1)
    data = db.read_data(ofsset,limit)
    row_num = db.row_count()
    page_num = math.ceil(row_num / limit) + 1
    slider_data = db.read_data_for_slider(slider_limit)
    return render_template('index.html',data=data, page_num=page_num, slider_data=slider_data)

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