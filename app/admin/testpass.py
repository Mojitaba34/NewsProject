
import mysql.connector

# MYSQL.CONNECTOR Config
MYSQL_HOST = "localhost"
MYSQL_USERNAME = "efi" 
MYSQL_PASSWORD = "123"
MYSQL_DB_NAME = "newsdb"

def get_database_connection():
    """connects to the MySQL database and returns the connection"""
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USERNAME,
        passwd=MYSQL_PASSWORD,
        db = MYSQL_DB_NAME,
        charset='utf8'
    )



db = get_database_connection()
cursor = db.cursor()

query = """ SELECT * FROM tbl_robots; """

try:
    cursor.execute(query)
    rows = cursor.fetchall()
    robots = dict()
    item = list()
    for row in rows:
        robotId = row[0]
        robotState = row[1]
        robotTimer = row[2]
        item.append([robotId,robotState,robotTimer])
        
    print(item)
except Exception as e:
    print("error")
