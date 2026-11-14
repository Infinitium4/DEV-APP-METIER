from API.database import get_connection
from fastapi import HTTPException

def show_clients():
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nom, prenom, telephone FROM client")
                clients = cursor.fetchall()
            return clients
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def show_client(client_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, nom, prenom, telephone FROM client WHERE id = %s",
                    (client_id,)
                )
                client = cursor.fetchone()
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Client introuvable"
        )

    return client


def supprimer_client(client_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM client WHERE id = %s",
                    (client_id,)
                )

                deleted = cursor.rowcount

            connection.commit()

            if deleted == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Client introuvable"
                )

            return {"message": "Client supprimé"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def insert_client(nom: str, prenom: str, telephone: str, mot_de_passe_hash: str):
    try:
        connection = get_connection()
        try:

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO client (nom, prenom, telephone, mot_de_passe_hash)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (nom, prenom, telephone, mot_de_passe_hash)
                )

                client_id = cursor.lastrowid

            connection.commit()

            return {
                "message": "Client ajouté",
                "id": client_id
            }

        finally:
            connection.close()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def update_client(client_id: int, nom: str, prenom: str, telephone: str):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE client SET nom = %s, prenom = %s, telephone = %s
                    WHERE id = %s
                    """,
                    (nom, prenom, telephone, client_id)
                )

                updated = cursor.rowcount

            connection.commit()

            if updated == 0:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM client WHERE id = %s",
                        (client_id,)
                    )
                    if cursor.fetchone() is None:
                        raise HTTPException(
                            status_code=404,
                            detail="Client introuvable"
                        )

            return {"message": "Client mis à jour"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la modification du client"
        )
