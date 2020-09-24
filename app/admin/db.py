import mysql.connector
from passlib.hash import pbkdf2_sha256
from app.admin import config
from persiantools.jdatetime import JalaliDateTime
import datetime
import time
from slugify import slugify_unicode
import random

def BuildTables():
    db = get_database_connection()
    cursor = db.cursor()

    try:
        # Create tbl_admin If not Exists
        cursor.execute(""" CREATE TABLE IF NOT EXISTS tbl_admin
        (
            id_admin INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
            username VARCHAR(30),
            password VARCHAR(200),
            email VARCHAR(40) UNIQUE,
            state_admin TINYINT DEFAULT 0
        );
        """)
        

        # Create tbl_news If not Exists
        cursor.execute(""" CREATE TABLE IF NOT EXISTS tbl_news
        ( 
            id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT ,
            news_title VARCHAR(500),
            news_slug VARCHAR(1000),
            news_content TEXT,
            news_link TEXT,
            news_img_link TEXT,
            news_date VARCHAR(20),
            status INT(1)
            );
            """)

        
        # Create tbl_contact If not Exists
        cursor.execute(""" CREATE TABLE IF NOT EXISTS tbl_contact_us
        (
            id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
            username VARCHAR(30),
            email VARCHAR(40) UNIQUE,
            subject VARCHAR(255),
            comment VARCHAR(255)
        );
        """)
        # Create tbl_ip If not Exists
        cursor.execute(""" CREATE TABLE IF NOT EXISTS tbl_ip
        (
            id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
            ip INT UNSIGNED,
            date VARCHAR(20)
        );
        """)

        # Create tbl_keyWords If not Exists
        cursor.execute(""" CREATE TABLE IF NOT EXISTS tbl_keywords
        (
            id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
            news_id INTEGER NOT NULL,
            FOREIGN KEY (news_id) REFERENCES tbl_news(id),
            keyword VARCHAR(100)
        );
        """)

        return 'table admin and robot created successfully'

    except Exception as e:
        return f'erorr in connection. {e} '

    finally:
        db.commit()
        db.close()



def get_database_connection():
    """connects to the MySQL database and returns the connection"""
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USERNAME,
        passwd=config.MYSQL_PASSWORD,
        db = config.MYSQL_DB_NAME,
        port = config.MYSQL_PORT,
        charset='utf8'
    )


def checkLogin(email,password):

    """ This Method 2 argument input and check these from tbl_admin exists or not
        so  @return True for Exists and @return False for Not Exists  """

    db = get_database_connection()
    cursor = db.cursor()
    login_query_email = "SELECT * FROM tbl_admin WHERE tbl_admin.email = %s;"
    """
        First Step Check Email User
        Secound Step check password hash
    """
    try:
        cursor.execute(login_query_email,(email, ))
        row_data = cursor.fetchall()
        # print('row_data ---- >',row_data)
        if len(row_data) == 1:
            for data_login in row_data:
                #data_login[0] # id
                #data_login[1] # username
                #data_login[2] # pass
                #data_login[3] # email
                #data_login[4] # state_admin
                state_admin = data_login[4]
                if state_admin == 1:
                    pass_state = pbkdf2_sha256.verify(password,data_login[2])
                    if pass_state==True:
                        return True,data_login[1],data_login[0]
                    else:
                        return False,"Password Invalid"
                else:
                    return False, "Please Wait for your account to be Confirmed."
        else:
            # print('row_data ---- >',row_data)
            return False,"this email not registered."
    except Exception as e:
        return False,e


def RegisterUser(username,password,email):
    """
    This Method get 3 argument and save in tbl_admin
    """
    db = get_database_connection()
    cursor = db.cursor()

    password_hash =  pbkdf2_sha256.hash(password)
    register_query = "INSERT INTO tbl_admin (username,password,email) VALUES (%s,%s,%s)"

    try:
        cursor.execute(register_query,(username,password_hash,email))
        db.commit()
        return True
    except Exception as e:
        return f"ERROR -> {e} ", False



def getCount_AllNews():

    """
    This Method Just Count All News Return From Database
    """
    db = get_database_connection()
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM tbl_news"
    try:
        cursor.execute(query)
        row_data = cursor.fetchall()
        for data in row_data:
               #data_login[0] # Count
               AllNews = data[0]
               return AllNews
    except Exception as e:
        return f"Error -- > {e}"



def getCount_TodayNews():
    """
    Method For Get TodayNews Count and return This 
    """
    db = get_database_connection()
    cursor = db.cursor()
    date_time = JalaliDateTime.now()

    query_TodayNews = "SELECT Count(*) FROM tbl_news WHERE tbl_news.news_date = %s;"

    try:
        cursor.execute(query_TodayNews,(str(date_time.jalali_date()), ))
        row_data = cursor.fetchall()
        for data in row_data:
            #data[0] # Count
            TodayNews = data[0]
            return TodayNews
    except Exception as e:
        return f"ERROR -- > {e}"


def get_NewsData():
    db = get_database_connection()
    cursor = db.cursor()
    query = "SELECT tbl_news.id,tbl_news.news_title,tbl_news.news_content,tbl_news.news_link,tbl_news.news_date FROM tbl_news ORDER BY news_date DESC"

    try:
        cursor.execute(query)
        row_data = cursor.fetchall()
        posts = []
        for data in row_data:
            # data [0] id_news
            # data [1] news_title
            # data [2] news_content
            # data [3] news_link
            # data [4] news_date
            post = {"id_news":data[0],"news_title":data[1],"news_content":data[2],"news_link":data[3],"news_date":data[4]}
            posts.append(post)
        return posts
    except Exception as e:
        return e


def newsEdit(id_news,Title,Desc):
    """
    This Method Give the Two Argument and Edite News Title and Desc
    @return True or False
    """
    db = get_database_connection()
    cursor = db.cursor()
    edit_news_query = """UPDATE tbl_news SET tbl_news.news_title = %s, tbl_news.news_content = %s WHERE tbl_news.id = %s; """

    edit_news_value = (str(Title),str(Desc),int(id_news))
    
    try:
        cursor.execute(edit_news_query,edit_news_value)
        db.commit()
        return f" Updated {cursor.rowcount} row. ",'success'
    except Exception as e:
        return f"Error -- > {e}",'danger'


def getCount_TodayVisitors():
    """
    This Method For Count Today Visitors By Ip
    @return True or False
    """
    db = get_database_connection()
    cursor = db.cursor()
    date_time = JalaliDateTime.now()

    visitors_query = """SELECT COUNT(*) FROM tbl_ip WHERE tbl_ip.date = %s;"""
    try:
        cursor.execute(visitors_query,(str(date_time.jalali_date()), ))
        row_data = cursor.fetchall()
        for data in row_data:
            #data[0] # Count
            CountVisitors = data[0]
            return CountVisitors
    except Exception as e:
        return f"ERROR -- > {e}"


def tejaratRobot_Update(state,timer):
    """
    This Method For Update Tejarat Robot Row in tbl_robots id == 1
    @return True or False
    """
    db = get_database_connection()
    cursor = db.cursor()

    tejarat_query = """UPDATE tbl_robots SET tbl_robots.state_news = %s , tbl_robots.time_crawler = %s WHERE tbl_robots.id = 1;"""
    tejarat_value = (state,timer)
    try:
        cursor.execute(tejarat_query,tejarat_value)
        db.commit()
        return f"Successfully Updated TejaratNews Robot.", "success"
        
    except Exception as e:
        return f"Not Updated beacuse {e}", "danger"


def TasnimRobot_Update(state,timer):
    """
    This Method For Update Tasnim Robot Row in tbl_robots id == 2
    @return Flash message Seccess or danger
    """
    db = get_database_connection()
    cursor = db.cursor()

    tasnim_query = """UPDATE tbl_robots SET tbl_robots.state_news = %s , tbl_robots.time_crawler = %s WHERE tbl_robots.id = 2;"""
    tasnim_value = (state,timer)
    try:
        cursor.execute(tasnim_query,tasnim_value)
        db.commit()
        return f"Successfully Updated TasnimNews Robot.", "success"
        
    except Exception as e:
        return f"Not Updated beacuse {e}", "danger"


def ArzdigitalRobot_Update(state,timer):
    """
    This Method For Update arzdigital Robot Row in tbl_robots id == 3
    @return True or False
    """
    db = get_database_connection()
    cursor = db.cursor()

    arz_query = """UPDATE tbl_robots SET tbl_robots.state_news = %s , tbl_robots.time_crawler = %s WHERE tbl_robots.id = 3;"""
    arz_value = (state,timer)
    try:
        cursor.execute(arz_query,arz_value)
        db.commit()
        return f"Successfully Updated Arzdigital Robot.", "success"
        
    except Exception as e:
        return f"Not Updated beacuse {e}", "danger"


def get_robots():
    db = get_database_connection()
    cursor = db.cursor()
    item = list()
    query = """ SELECT * FROM tbl_robots; """

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            robotId = row[0]
            robotState = row[1]
            robotTimer = row[2]
            item.append([robotId,robotState,robotTimer])
        
        return item
    except Exception as e:
        return f"Error -- > {e}"



"""
Insert Data To tbl_news
"""
def InsertTblNews(data,state):
    """This Method received the data argument and insert into table news after check data exists or not"""
    db = get_database_connection()
    cursor = db.cursor()
    date_time = JalaliDateTime.now() # give us dateTime shamsi
    NewsDateTime = date_time.strftime('%Y/%m/%d %H:%M:%S')
    try:
        count = 0
        for news_Data in data:
            if CheckExistsTitleNews(news_Data['title']) == False:
                slug = slugify_unicode(str(news_Data['title']),allow_unicode=True)
                insert_query = "INSERT INTO tbl_news (news_title,news_slug, news_content, news_link, news_img_link, news_date,status) VALUES (%s ,%s , %s, %s, %s, %s,%s)"
                insert_val = (str(news_Data['title']),slug,str(news_Data['content']),str(news_Data['link']),str(news_Data['news_img_link']),str(NewsDateTime),str(state))
                cursor.execute(insert_query,insert_val)
            db.commit()
            lastId = get_last_news_id()
            keyword = keyword_generator(str(news_Data['title']))
            insert_keyword(lastId,keyword)
            count += 1
        return f'{count} data inserted'
    except Exception as e:
        return f'an Erorr {e} .'
    db.close()



def keyword_generator(title):
    text_data = title.split(' ')
    if text_data[-1] == '':
        del text_data[-1]
    data_list = []
    for txt in text_data:
        if len(txt) > 3 and 'داد' and 'می کند' and 'کند' and 'می شود' and 'می یابد' and 'کرد' and 'است'and 'رسید' not in txt:
            data_list.append(txt)
    data = list(dict.fromkeys(data_list))
    keyword_text = ''
    digits = '0123456789'
    sign = '!@#$%^&*()_+=-\\/'
    for text in data:
        keyword_text = keyword_text + (text + ',')
    remove_digits = str.maketrans('', '', digits)
    remove_sign = str.maketrans('', '', sign)
    res = keyword_text.translate(remove_digits)
    res = res.translate(remove_sign)
    return res


def get_last_news_id():
    """
        This method return last news id returned for us
    """
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
        """SELECT id FROM tbl_news ORDER BY tbl_news.id DESC LIMIT 1;"""
        )
        data_db = cursor.fetchone()
        return data_db[0]
    except Exception as e :
        return e



"""
Check Exists Title News With Crawled Title
"""
def CheckExistsTitleNews(title):
    """ This Method for get all titles in database and check with input title
        now, if title equal by database titles this data not insert to table News
        thats Mean check data exists ro not
    """
    if (title != None):
        # import connection database and build a cursor
        db = get_database_connection()
        cursor = db.cursor()

        # This try run query in mysql and fetch all data titles
        try:
            cursor.execute(
            """SELECT news_title FROM tbl_news;"""
            )
            data_db = cursor.fetchall()
        except Exception as _:
            return False

        if cursor.rowcount > 0 :
            db_titles = [] # this list for database Titles

            for db_title in data_db:
                db_titles.append(db_title[0]) # append titles in db_titles

            return True if title in db_titles else False # this if for check exists title in db_titles
            #print(f'{data_titles} and {db_titles}')
        else:
            return False
    else:
        return False
    db.close()



"""
inserting comments into database
"""
def Insertcomment(username,email,subject,comment):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO tbl_contact_us (username, email, subject,comment) VALUES (%s,%s,%s,%s)",(username,email,subject,comment))
        db.commit()
        return True
    except Exception as e:
        return f'an Erorr {e} .'

    db.close()
    return 'none'





"""
Geting data from DataBase to import in index page
"""
def today_news(ofsset, limit):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT news_slug,news_title,news_content,news_link,news_img_link,news_date FROM tbl_news WHERE tbl_news.status = 0 OR tbl_news.status = 1 ORDER BY news_date DESC LIMIT %s, %s;', (ofsset,limit))
        data = list(cursor.fetchall())
        return data
    except Exception as e:
        return f"ERROR -> {e}"


"""
Geting data from DataBase to import in index page for Corona News
"""
def read_data_Corona_news(limit):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT news_slug,news_title,news_content,news_link,news_img_link,news_date FROM tbl_news WHERE status = 3 ORDER BY news_date DESC LIMIT %s;', (limit,))
        data = list(cursor.fetchall())
        return data
    except Exception as e:
        return f"ERROR -> {e}"


"""
We need a rows number to figure out how many pages do we have
"""

def row_count():
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT COUNT(*) FROM tbl_news WHERE NOT status = 3 AND NOT status = 4 AND NOT status = 2')
        data = cursor.fetchone()
        return data[0]
    except Exception as e:
        return f"ERROR -> {e}"

"""
Geting data from DataBase random tejarat
"""
def read_data_random_tejarat():
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT news_slug,news_title,news_link,news_img_link FROM tbl_news  WHERE status = 1 ORDER BY news_date DESC LIMIT 6')
        data = list(cursor.fetchall())
        return random.choice(data)
    except Exception as e:
        return f"ERROR -> {e}"


"""
Geting data from DataBase random tasnim
"""
def read_data_random_tasnim():
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT news_slug,news_title,news_link,news_img_link FROM tbl_news  WHERE status = 0 ORDER BY news_date DESC LIMIT 6')
        data = list(cursor.fetchall())
        return random.choice(data)
    except Exception as e:
        return f"ERROR -> {e}"



"""
Geting data from DataBase random arzdigital
"""
def read_data_random_arzdigital():
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT news_slug,news_title,news_link,news_img_link FROM tbl_news  WHERE status = 2 ORDER BY news_date DESC LIMIT 6')
        data = list(cursor.fetchall())
        return random.choice(data)
    except Exception as e:
        return f"ERROR -> {e}"


"""
Geting data from DataBase random bors
"""
def read_data_random_bors():
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT news_slug,news_title,news_link,news_img_link FROM tbl_news  WHERE status = 4 ORDER BY news_date DESC LIMIT 6')
        data = list(cursor.fetchall())

        return random.choice(data)
    except Exception as e:
        return f"ERROR -> {e}"



"""
Geting data from DataBase random corona
"""
def read_data_random_corona():
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT news_slug,news_title,news_link,news_img_link FROM tbl_news  WHERE status = 3 ORDER BY news_date DESC LIMIT 6')
        data = list(cursor.fetchall())
        return random.choice(data)
    except Exception as e:
        return f"ERROR -> {e}"


def read_corona_news():
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT news_slug,news_title,news_link,news_img_link FROM tbl_news  WHERE status = 3 ORDER BY news_date DESC LIMIT 10')
        data = list(cursor.fetchall())
        return data
    except Exception as e:
        return f"ERROR -> {e}"

"""
Inserting ip address in to the db
"""
def insert_ip(ip):
    db = get_database_connection()
    cursor = db.cursor()
    date = JalaliDateTime.now()
    try:
        if CheckExistsIpAddress(ip) == False:
            insert = "INSERT INTO tbl_ip (ip,date) VALUES (INET_ATON(%s),%s)"
            val = (ip, str(date.strftime("%Y/%m/%d")))
            cursor.execute(insert,val)
        db.commit()
        return "Done"
    except Exception as e:
        return f'an Erorr {e} .'

    db.close()
    return 'none'

def ip_date_update(ip):
    db = get_database_connection()
    cursor = db.cursor()
    date = JalaliDateTime.now()
    try:
        # insert = """UPDATE tbl_ip SET date= '%s' WHERE ip = INET_ATON('%s');"""
        # val = (date.strftime("%Y/%m/%d-%H:%M:%S"), ip)
        cursor.execute(f"UPDATE tbl_ip SET date= '{date.strftime('%Y/%m/%d')}' WHERE ip = INET_ATON('{ip}');")
        db.commit()
    except Exception as e:
        return f'an Erorr {e} .'

"""
Check Exists ip address
"""
def CheckExistsIpAddress(ip):
    """ This Method for get all titles in database and check with input title
        now, if title equal by database titles this data not insert to table News
        thats Mean check data exists ro not
    """
    if (ip != None):
        # import connection database and build a cursor
        db = get_database_connection()
        cursor = db.cursor()

        # This try run query in mysql and fetch all data ip
        try:
            cursor.execute(
            """SELECT INET_NTOA(ip) FROM tbl_ip;"""
            )
            data_db = cursor.fetchall()
        except Exception as _:
            return False

        if cursor.rowcount > 0 :
            db_ip = [] # this list for database ip

            for db_ip in data_db:
                db_ip.append(db_ip[0]) # append ips in db_ip

            return True if ip in db_ip else False # this if for check exists ip in db_ip
        else:
            print('khali ast')
            return False
    else:
        return False
    db.close()



"""
arzdigital news QUERY
"""

def arzdigital_news():
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT news_slug,news_title,news_content,news_link,news_img_link FROM tbl_news WHERE news_link LIKE %s ORDER BY news_date DESC LIMIT 10;"  , ("%" + "arzdigital" + "%",))
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        return f"ERROR -> {e}"

def check_slug(text):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT news_slug,news_title,news_content,news_link,news_img_link,news_date,status,id FROM tbl_news WHERE tbl_news.news_slug = %s ; "  , (text, ))
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        return f"ERROR -> {e}"

def related_news_sidebar(state):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT news_slug,news_title FROM tbl_news WHERE tbl_news.status = %s ORDER BY tbl_news.news_date DESC LIMIT 8 ; "  , (state, ))
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        return f"ERROR -> {e}"

def bors_news_sidebar():
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT news_slug,news_title,news_img_link FROM tbl_news WHERE tbl_news.status = 4 LIMIT 5 ; " )
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        return f"ERROR -> {e}"

def arz_news_sidebar():
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT news_slug,news_title FROM tbl_news WHERE tbl_news.status = 2 ORDER BY tbl_news.news_date DESC LIMIT 5 ; " )
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        return f"ERROR -> {e}"

def sitemap():
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT news_slug,news_date FROM tbl_news ;")
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        return f"ERROR -> {e}"
    
def bors_news(ofsset,limit):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT news_slug,news_title,news_content,news_link,news_img_link FROM tbl_news  WHERE status = 4 ORDER BY news_date DESC LIMIT %s, %s",(ofsset,limit))
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        return f"ERROR -> {e}"



def insert_keyword(last_id,keywords):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        insert = "INSERT INTO tbl_keywords (news_id,keyword) VALUES (%s,%s)"
        val = (last_id,str(keywords))
        cursor.execute(insert,val)
        db.commit()
    except Exception as ex:
        return ex


def get_news_keywords(newsid):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT keyword FROM tbl_keywords WHERE tbl_keywords.news_id = %s;" , (newsid, ))
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as ex:
        return ex