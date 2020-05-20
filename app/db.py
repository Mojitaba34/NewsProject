import MySQLdb
from app import config

def get_database_connection():
    """connects to the MySQL database and returns the connection"""
    return MySQLdb.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USERNAME,
        passwd=config.MYSQL_PASSWORD,
        db = config.MYSQL_DB_NAME,
        charset='utf8'
    )


def BuildTables():
    db = get_database_connection()
    cursor = db.cursor()

    try:
        
        # Create tbl_news If not Exists
        cursor.execute(""" CREATE TABLE IF NOT EXISTS tbl_news
        ( 
            id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT ,
            news_title VARCHAR(100),
            news_content TEXT,
            news_link TEXT,
            news_img_link TEXT,
            news_date DATETIME
            );
            """)
        # Create tbl_admin If not Exists
        cursor.execute(""" CREATE TABLE IF NOT EXISTS tbl_admin
        (
            id_admin INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
            username VARCHAR(30),
            password VARCHAR(30),
            email VARCHAR(40) UNIQUE
        );
        """)
        # Create tbl_robots If not Exists
        cursor.execute(""" CREATE TABLE IF NOT EXISTS tbl_robots
        (
            id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
            state_news_price TINYINT(1),
            state_crypto_price TINYINT(1),
            time_crawler int(5)
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
        return 'tables created successfully'

    except Exception as e:
        return f'erorr in connection. {e} '

    finally:
        db.commit()
        db.close()


def InsertTblNews(data):
    """This Method received the data argument and insert into table news after check data exists or not"""
    db = get_database_connection()
    cursor = db.cursor()
    try:
        count = 0
        for post in range(data.__len__()):
            if CheckExistsTitleNews(data[post]['title']) == False:
                cursor.execute("INSERT INTO tbl_news (news_title, news_content, news_link, news_img_link, news_date) VALUES (%s, %s, %s, %s, %s)",(data[post]['title'],data[post]['content'],data[post]['link'],data[post]['news_img_link'],"date.today()"))
                db.commit()
                count+=1
        return f'{count} data inserted '
    except Exception as e:
        return f'an Erorr {e} .'
    
    db.close()
    return 'none'


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
            rowCount = cursor.execute(
            """SELECT news_title FROM tbl_news;"""
            )
        except Exception as _:
            return False

        if rowCount > 0 :
            db_titles = [] # this list for database Titles
            data_db = cursor.fetchall()

            for db_title in data_db:
                db_titles.append(db_title[0]) # append titles in db_titles

            return True if title in db_titles else False # this if for check exists title in db_titles
            #print(f'{data_titles} and {db_titles}')
        else:
            print('khali ast')
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
    cursor.execute('SELECT news_title,news_content,news_link,news_img_link FROM tbl_news ORDER BY id DESC LIMIT %s, %s;', (ofsset,limit))
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
    cursor.execute(f'SELECT news_title,news_content,news_link,news_img_link FROM tbl_news ORDER BY id DESC LIMIT {limit}')
    data = list(cursor.fetchall())
    return data

