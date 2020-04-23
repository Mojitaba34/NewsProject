import MySQLdb
import config

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
                cursor.execute("""INSERT INTO tbl_news (news_title, news_content, news_link, news_img_link, news_date) 
                        VALUES (%s, %s, %s, %s, %s)""",(data[post]['title'],data[post]['content'],data[post]['link'],data[post]['news_img_link'],date.today()))
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
