def show_clients():
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DESCRIBE client")
                clients = cursor.fetchall()
            return clients
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )