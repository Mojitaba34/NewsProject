import mysql.connector
from passlib.hash import pbkdf2_sha256
from app.admin import config
from persiantools.jdatetime import JalaliDateTime

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
        
        # Create tbl_robots If not Exists
        cursor.execute(""" CREATE TABLE IF NOT EXISTS tbl_robots
        (
            id INTEGER PRIMARY KEY NOT NULL,
            state_news TINYINT(1),
            time_crawler int(5)
        );
        """)

        # inserting 3 deafult value into table for robots
        cursor.execute("""
            INSERT INTO tbl_robots(id, state_news, time_crawler) VALUES 
                (1, 1, 10),
                (2, 1, 30),
                (3, 1, 60);
                
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