from app import app
from flask import Flask , render_template, request, redirect, url_for,flash, jsonify, make_response,abort
from app.admin import db
import math, json
from app.admin import config
import readtime
import math
from urllib.parse import urlparse
import time
'''
This routes is for Home page and passing some data to home Page

'''
@app.route('/', methods=["GET", "POST"])
@app.route('/home')
def home():
    
    limit= 6
    limit_corona = 4
    bors_news_limit = 6
    row_num = db.row_count()
    page_num = math.ceil(row_num / limit)
    if int(request.args.get('page', 1, type=int)) > page_num:
        return render_template('404.html')
    page = request.args.get('page', 1, type=int)
    pagination_link_limit = 5
    slider_limit = 3
    ofsset=limit * (page - 1)
    ofsset_bors=bors_news_limit * (page - 1)
    todaynews = db.today_news(ofsset,limit)# reading data from data base to insert in news section
    Corona_data = db.read_data_Corona_news(limit_corona)
    bors_news_data = db.bors_news(ofsset_bors,bors_news_limit)
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

    # Random Data for head site
    random_tejarat = db.read_data_random_tejarat()
    random_tasnim = db.read_data_random_tasnim()
    random_arzdigital = db.read_data_random_arzdigital()
    random_bors = db.read_data_random_bors()
    random_corona = db.read_data_random_corona()


    # arzdigital news
    arzdigital = db.arzdigital_news()

    # corona news
    corona_news = db.read_corona_news()

    ip_address = request.environ['REMOTE_ADDR']# getting ip address
    db.insert_ip(ip_address)# inserting ip address
    print(db.ip_date_update(ip_address)) # update ip Date
    time.sleep(1)
    return render_template('index.html', data=todaynews,page_num=page_num,maxLeft=maxLeft,maxRight=maxRight,configId='UA-169005487-1',
    corona_data=Corona_data,bors_news_data=bors_news_data,arzdigital=arzdigital,random_arzdigital=random_arzdigital,random_bors=random_bors,
    random_corona=random_corona,random_tasnim=random_tasnim,random_tejarat=random_tejarat,corona_news=corona_news)

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


@app.route('/<slug>',methods=["GET"])
def landing(slug):
    data = db.check_slug(slug)
    ls = []
    if data == []:
        abort(404)

    #TODO : This is not Good for shoud be fix
    text = [post[2] for post in data]
    state = [post[6] for post in data]
    newsid = [post[7] for post in data]
    title = [post[1] for post in data]

    time = readtime.of_text(text[0])
    min = int(time.seconds) / 60

    related_news = db.related_news_sidebar(state[0])
    bors_news = db.bors_news_sidebar()
    arznews = db.arz_news_sidebar()

    keywords = db.get_news_keywords(newsid[0])
    list_keywords = str(keywords[0][0]).split(',')
    return render_template('landing.html',data=data,title=title,related_news=related_news,keywords = list_keywords,bors_news=bors_news,arz_news = arznews ,time_read=str(math.floor(min)))



@app.route("/sitemap.xml")
def sitemap():
    """
        Route to dynamically generate a sitemap of your website/application.
        lastmod and priority tags omitted on static pages.
        lastmod included on dynamic content such as blog posts.
    """

    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    # Static routes with static content
    static_urls = list()
    for rule in app.url_map.iter_rules():
        if not str(rule).startswith("/admin") and not str(rule).startswith("/user") and not str(rule).startswith("/_"):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                url = {
                    "loc": f"{host_base}{str(rule)}"
                }
                static_urls.append(url)

    # Dynamic routes with dynamic content
    dynamic_urls = list()
    news_post = db.sitemap()
    for post in news_post:
        url = {
            "loc": "{}/{}".format(host_base,post[0]),
            "lastmod": post[1]
            }
        dynamic_urls.append(url)

    xml_sitemap = render_template("sitemap.xml", static_urls=static_urls, dynamic_urls=dynamic_urls, host_base=host_base)
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response
