from database import get_connection
from fastapi import HTTPException


def show_roles():
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM role")
                roles = cursor.fetchall()
            return roles
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def show_role(role_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM role WHERE id = %s",
                    (role_id,)
                )
                role = cursor.fetchone()
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role introuvable"
        )

    return role


def supprimer_role(role_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM role WHERE id = %s",
                    (role_id,)
                )

                deleted = cursor.rowcount

            connection.commit()

            if deleted == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Role introuvable"
                )

            return {"message": "Role supprimé"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def insert_role(nom: str):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO role (nom)
                    VALUES (%s, %s, %s)
                    """,
                    (nom,)
                )

                role_id = cursor.lastrowid

            connection.commit()

            return {
                "message": "Role ajouté",
                "id": role_id
            }

        finally:
            connection.close()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def update_role(role_id: int, nom: str):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE role SET nom = %s
                    WHERE id = %s
                    """,
                    (nom, role_id)
                )

                updated = cursor.rowcount

            updated.commit()

            if updated == 0:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM role WHERE id = %s",
                        (role_id,)
                    )
                    if cursor.fetchone() is None:
                        raise HTTPException(
                            status_code=404,
                            detail="Role introuvable"
                        )

            return {"message": "Role mis à jour"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la modification du role"
        )