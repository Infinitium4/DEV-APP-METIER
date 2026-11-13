
import os
import pymysql

def get_connection():
    print(os.getenv("DB_HOST", "localhost"))
    print(int(os.getenv("DB_PORT", "3306")))
    print(os.getenv("DB_USER", "root"))
    print(os.getenv("DB_PASSWORD"))
    print(os.getenv("DB_NAME", "api_test"))
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "api_test"),
        cursorclass=pymysql.cursors.DictCursor
    )
    