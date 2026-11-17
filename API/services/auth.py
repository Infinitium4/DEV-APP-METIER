import os

from fastapi import HTTPException
from pymysql import MySQLError

from API.database import get_connection
from API.securite import creer_token, verifier_mot_de_passe


def authentifier(telephone: str, mot_de_passe: str, type_utilisateur: str):
    cle = os.getenv("JWT_SECRET_KEY")
    if not cle:
        raise HTTPException(status_code=503, detail="Clé JWT non configurée")

    # Le nom de table vient exclusivement de cette liste fixe.
    table = {"client": "client", "personnel": "personnel"}[type_utilisateur]
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT id, mot_de_passe_hash FROM {table} WHERE telephone = %s LIMIT 2",
                    (telephone.strip(),),
                )
                utilisateurs = cursor.fetchall()
        finally:
            connection.close()
    except MySQLError:
        raise HTTPException(status_code=503, detail="Base de données indisponible") from None

    # Refuser aussi les téléphones ambigus : pas de choix arbitraire de compte.
    if len(utilisateurs) != 1 or not verifier_mot_de_passe(
        mot_de_passe, utilisateurs[0]["mot_de_passe_hash"]
    ):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    return {
        "access_token": creer_token(utilisateurs[0]["id"], type_utilisateur, cle),
        "token_type": "bearer",
    }
