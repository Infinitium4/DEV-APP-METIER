
import pymysql

def get_connection():
    return pymysql.connect(
        host="172.16.113.89",
        user="admin",
        password="root",
        database="ma_database",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )
