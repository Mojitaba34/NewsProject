import mysql.connector
from passlib.hash import pbkdf2_sha256
from app.admin import config


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
            email VARCHAR(40) UNIQUE
        );
        """)
        
        return 'table admin created successfully'

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
                print(data_login[2])
                pass_state = pbkdf2_sha256.verify(password,data_login[2])
                if pass_state==True:
                    return True,data_login[1],data_login[0]
                else:
                    return False,"Password Invalid"
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
        return f"ERROR -> {e} "
        return False


"""
This Method Just Count All News Return From Database
"""
def getCount_AllNews():

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


"""
Method For Get TodayNews Count and return This 
TODO: Check Date
"""
def getCount_TodayNews():
    db = get_database_connection()
    cursor = db.cursor()
    query_TodayNews = "SELECT Count(*) FROM tbl_news WHERE tbl_news.news_data = {}" # TODO: Import and check date time Persina Or English
    try:
        cursor.execute()
        row_data = cursor.fetchall()
        for data in row_data:
            #data_login[0] # Count
            TodayNews = data[0]
            return TodayNews
    except Exception as e:
        return "ERROR -- > {e}"



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