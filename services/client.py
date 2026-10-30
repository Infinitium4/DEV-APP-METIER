from database import get_connection
from fastapi import HTTPException


def show_clients():
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


def show_client(client_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM client WHERE id = %s",
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


def show_client_num(client_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT num_tel FROM client WHERE id = %s",
                    (client_id,)
                )
                client_num = cursor.fetchone()
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

    if client_num is None:
        raise HTTPException(
            status_code=404,
            detail="Client introuvable ou sans numéro"
        )

    return client_num


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


def insert_client(nom: str,email: str,telephone: str):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO client (nom, email, telephone)
                    VALUES (%s, %s, %s)
                    """,
                    (nom, email, telephone)
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


def update_client(client_id: int, nom: str,email: str,telephone: str):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE client SET nom = %s,email = %s,telephone = %s
                    WHERE id = %s
                    """,
                    (nom, email, telephone, client_id)
                )

                updated = cursor.rowcount

            updated.commit()

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