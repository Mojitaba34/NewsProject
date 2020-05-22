from flask import session,render_template,redirect,url_for,request,flash
from app.admin import admin
from app.admin import db
from app.admin import getData
"""
This Method and Url For --dashboard-- and --index-- in admin Panel
"""
@admin.route('/',methods=["GET"])
def dashboard():
    if session.get("user_data") != None:
        return render_template('container_controller.html',container='',user_data=session.get("user_data"),Data = getData())
    else:
        return redirect(url_for('admin.login'))



"""
This Method and Url For --login-- User in admin Panel
"""
@admin.route('/login',methods=["GET","POST"])
def login():
    if request.method== "POST":
        email_entered = request.form["email"]
        password = request.form["password"]
        ip_address = request.remote_addr
        if email_entered != "" and password != "":
            data = db.checkLogin(email_entered,password)
            if data[0]: # thats mean return True and login success
                username = data[1]
                id_user = data[2]
                session.permanent = True
                session["user_data"] = id_user, username,ip_address
                return redirect(url_for('admin.dashboard'))
            else:
                flash(data[1],"error")
                return render_template('login.html')
        else:
            flash("please compelete","error")
            print('invalid2')
            return render_template('login.html')
    else:
        if session.get("user_data") != None:
            return render_template('container_controller.html',container='',user_data=session.get("user_data"))
        else:
            return render_template('login.html')



"""
This Method and Url For --register-- User in admin Panel
"""
@admin.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        pswd = request.form["password"]
        if username != "" and email != "" and pswd != "":
            res = db.RegisterUser(username,pswd,email)
            if res == True:
                flash("registered Seccessed!","success")
                return redirect(url_for('admin.login'))
            else:
                flash("registered failed!","error")
                return render_template('register.html')
        else:
            flash("please enter full info","info")
            return render_template('register.html')
    else:
        if session.get("user_data") != None:
            return render_template('register.html')
        else:
            return render_template('register.html')


"""
This Method for Logout user of admin panel
"""
@admin.route('/logout')
def logout():
    session.pop("user_data",None)
    return redirect(url_for('admin.login'))



"""
This Method and Url -- News Robot Page -- in admin panel
"""
@admin.route('/news_robot')
def news_robot():
    if session.get("user_data") != None:
        return render_template('container_controller.html',container='news_robot',user_data=session.get("user_data"))
    else:
        return redirect(url_for('login'))



"""
This Method and Url -- Crypto Robot Page -- in admin panel
"""
@admin.route('/crypto_robot')
def crypto_robot():
    if session.get("user_data") != None:
        return render_template('container_controller.html',container='crypto_robot',user_data=session.get("user_data"))
    else:
        return redirect(url_for('login'))

