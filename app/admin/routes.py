from flask import session,render_template,redirect,url_for,request,flash,jsonify
from app.admin import admin
from app.admin import db
from app.admin import getData
from app.robots import robots
from string import digits

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
        robot_data = db.get_robots()
        return render_template('container_controller.html',container='news_robot',user_data=session.get("user_data"),robotdata=robot_data)
    else:
        return redirect(url_for('login'))


"""
This Method For 'TejaratNews' Get id Robot and save [timer, state] in db
"""
@admin.route('/tejarat',methods=["POST"])
def tejarat():
    if request.method == "POST":
        timer = request.form.get("timer")
        state = 0 if request.form.get("state") == 'on' else 1 # if for Checked Checkbox Value
        message = db.tejaratRobot_Update(state,timer) # Updated Method in db
        flash(message[0],message[1]) # Flash Compeleted
        return redirect(url_for("admin.news_robot"))


"""
This Method For 'TejaratNews' Get id Robot and save [timer, state] in db
"""
@admin.route('/tasnim',methods=["POST"])
def tasnim():
    if request.method == "POST":
        timer = request.form.get("timer")
        state = 0 if request.form.get("state") == 'on' else 1 # if for Checked Checkbox Value
        message = db.TasnimRobot_Update(state,timer) # Updated Method in db
        flash(message[0],message[1]) # Flash Compeleted
        return redirect(url_for("admin.news_robot"))


"""
This Method For 'TejaratNews' Get id Robot and save [timer, state] in db
"""
@admin.route('/arzdigital',methods=["POST"])
def arzdigital():
    if request.method == "POST":
        timer = request.form.get("timer")
        state = 0 if request.form.get("state") == 'on' else 1 # if for Checked Checkbox Value
        message = db.ArzdigitalRobot_Update(state,timer) # Updated Method in db
        flash(message[0],message[1]) # Flash Compeleted
        return redirect(url_for("admin.news_robot"))


"""
This Method and Url -- Crypto Robot Page -- in admin panel
"""
@admin.route('/crypto_robot')
def crypto_robot():
    if session.get("user_data") != None:
        return render_template('container_controller.html',container='crypto_robot',user_data=session.get("user_data"))
    else:
        return redirect(url_for('login'))

@admin.route('/edit_news',methods=["POST"])
def NewsEdit():
    if request.method == "POST":
        NewsId = request.form['NewsId']
        Title = request.form['Title']
        Description = request.form['Description']
        if Title != "" and Description != "":
            # Update Table News
            msg = db.newsEdit(NewsId,Title,Description)
            flash(msg[0],msg[1])
            
        else:
            flash('لطفا اطلاعات را تکمیل کنید')
        
    return redirect(url_for("admin.dashboard"))


@admin.route('/run',methods=["GET"])
def runRob():
    state_tasnim = 0
    state_tejart = 1
    state_arzdigi = 2
    state_Corona = 3
    state_bors = 4
    if session.get("user_data") != None:
        tasnim_news = robots.news_from_tasnimnews()
        data_tasnim = tasnim_news.getData()   
        print("--------------Tasnim----------------")
        print("tasnim=  "+db.InsertTblNews(data_tasnim,state_tasnim))        


        tejarat_news = robots.news_from_tejaratnews()
        data_tejarat = tejarat_news.getData()
        print("--------------Tejarat----------------")
        print("tejarat=  "+db.InsertTblNews(data_tejarat,state_tejart))


        arzdigital_news = robots.news_from_arzdigital()
        data_arzdigital = arzdigital_news.getData()
        print("--------------Arzdigital----------------")
        print("arzdigital=  "+db.InsertTblNews(data_arzdigital,state_arzdigi))

        mehr_news = robots.news_from_mehrnews()
        data_corona = mehr_news.getData()
        print("--------------Corona----------------")
        print("Mehr_news=  "+db.InsertTblNews(data_corona,state_Corona))

        Bors_news_data = robots.Bors_news()
        data_bors = Bors_news_data.getData()
        print("--------------Bors----------------")
        print("Bors=  "+db.InsertTblNews(data_bors,state_bors))

        return redirect(url_for("admin.dashboard"))