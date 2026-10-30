from fastapi import FastAPI, HTTPException
from database import get_connection
from client import *

app = FastAPI()

@app.get("/")
def accueil():
    return {"message": "API connectée à MariaDB"}

@app.get("/clientshow")
def get_clients():
   show_clients();

@app.get("/clients")
def get_clients():
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM client")
                clients = cursor.fetchall()
            return clients
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

@app.get("/clients/{user_id}")
def get_user(user_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE id = %s",
                    (user_id,)
                )
                user = cursor.fetchone()
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable"
        )

    return user
