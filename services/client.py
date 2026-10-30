from database import get_connection

def show_clients():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL get_clients()")
            return cursor.fetchall()
    finally:
        connection.close()