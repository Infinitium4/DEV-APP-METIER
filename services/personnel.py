from database import get_connection
from fastapi import HTTPException


def show_personnels():
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM personnel")
                personnels = cursor.fetchall()
            return personnels
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def show_personnel(personnel_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM personnel WHERE id = %s",
                    (personnel_id,)
                )
                personnel = cursor.fetchone()
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

    if personnel is None:
        raise HTTPException(
            status_code=404,
            detail="Personnel introuvable"
        )

    return personnel


def show_role_personnel(id_role: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM personnel WHERE id_role = %s",
                    (id_role,)
                )
                personnel = cursor.fetchone()
            return personnel
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )



def supprimer_personnel(personnel_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM personnel WHERE id = %s",
                    (personnel_id,)
                )

                deleted = cursor.rowcount

            connection.commit()

            if deleted == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Personnel introuvable"
                )

            return {"message": "Personnel supprimé"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def insert_personnel(nom: str,telephone: str, id_role: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO personnel (nom, telephone, id_role)
                    VALUES (%s, %s, %s)
                    """,
                    (nom, telephone, id_role)
                )

                personnel_id = cursor.lastrowid

            connection.commit()

            return {
                "message": "Personnel ajouté",
                "id": personnel_id
            }

        finally:
            connection.close()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def update_personnel(personnel_id: int, nom: str, telephone: str, id_role: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE personnel SET nom = %s, telephone = %s, id_role = %s
                    WHERE id = %s
                    """,
                    (nom, telephone, id_role, personnel_id)
                )

                updated = cursor.rowcount

            updated.commit()

            if updated == 0:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM personnel WHERE id = %s",
                        (personnel_id,)
                    )
                    if cursor.fetchone() is None:
                        raise HTTPException(
                            status_code=404,
                            detail="Personnel introuvable"
                        )

            return {"message": "Personnel mis à jour"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la modification du personnel"
        )