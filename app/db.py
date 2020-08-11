import mysql.connector
from app.admin import config
import datetime
from persiantools.jdatetime import JalaliDateTime
import time

"""
Connection To Db
"""

def get_database_connection():
    """connects to the MySQL database and returns the connection"""
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USERNAME,
        passwd=config.MYSQL_PASSWORD,
        db = config.MYSQL_DB_NAME,
        port=config.MYSQL_PORT,
        charset='utf8'
    )


"""
Build Tables Default
"""
def BuildTables():
    db = get_database_connection()
    cursor = db.cursor()

    try:
        
        # Create tbl_news If not Exists
        cursor.execute(""" CREATE TABLE IF NOT EXISTS tbl_news
        ( 
            id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT ,
            news_title VARCHAR(500),
            news_content TEXT,
            news_link TEXT,
            news_img_link TEXT,
            news_date VARCHAR(10),
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
        return 'tables created successfully'

    except Exception as e:
        return f'erorr in connection. {e} '

    finally:
        db.commit()
        db.close()


"""
Insert Data To tbl_news
"""
def InsertTblNews(data,state):
    """This Method received the data argument and insert into table news after check data exists or not"""
    db = get_database_connection()
    cursor = db.cursor()
    date_time = JalaliDateTime.now() # give us dateTime shamsi
    try:
        for news_Data in data:
            if CheckExistsTitleNews(news_Data['title']) == False:
                insert_query = "INSERT INTO tbl_news (news_title, news_content, news_link, news_img_link, news_date,status) VALUES (%s, %s, %s, %s, %s,%s)"
                insert_val = (str(news_Data['title']),str(news_Data['content']),str(news_Data['link']),str(news_Data['news_img_link']),str(date_time.jalali_date()),str(state))
                cursor.execute(insert_query,insert_val)
            db.commit()
        return f'{cursor.rowcount} data inserted '
    except Exception as e:
        return f'an Erorr {e} .'
    
    db.close()
    return 'none'


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
def read_data(ofsset, limit):
    db = get_database_connection()
    cursor = db.cursor()
    cursor.execute('SELECT news_title,news_content,news_link,news_img_link,news_date FROM tbl_news ORDER BY news_date DESC LIMIT %s, %s;', (ofsset,limit))
    data = list(cursor.fetchall())
    return data


"""
Geting data from DataBase to import in index page for Corona News
"""
def read_data_Corona_news(ofsset, limit):
    db = get_database_connection()
    cursor = db.cursor()
    cursor.execute('SELECT news_title,news_content,news_link,news_img_link,news_date FROM tbl_news WHERE status = 3 ORDER BY news_date DESC LIMIT %s, %s;', (ofsset,limit))
    data = list(cursor.fetchall())
    return data



"""
We need a rows number to figure out how many pages do we have
"""

def row_count():
    db = get_database_connection()
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM tbl_news')
    data = cursor.fetchone()
    return data[0]


"""
Geting data from DataBase to import in to the Slider
"""
def read_data_for_slider(limit):
    db = get_database_connection()
    cursor = db.cursor()
    cursor.execute('SELECT news_title,news_content,news_link,news_img_link FROM tbl_news  WHERE news_link LIKE %s ORDER BY news_date DESC LIMIT %s', ("%" + "tejaratnews" + "%", limit))
    data = list(cursor.fetchall())
    return data


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
    cursor.execute("SELECT * FROM tbl_news WHERE news_link LIKE %s ORDER BY news_date DESC LIMIT 10"  , ("%" + "arzdigital" + "%",))
    data = cursor.fetchall()
    cursor.close()
    return data
    