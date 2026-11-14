from API.database import get_connection
from fastapi import HTTPException
from API.services.personnel import show_personnel
from API.services.role import show_role


def show_nettoyages():
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM nettoyage")
                nettoyages = cursor.fetchall()
            return nettoyages
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def show_nettoyage(nettoyage_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM nettoyage WHERE id = %s",
                    (nettoyage_id,)
                )
                nettoyage = cursor.fetchone()
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

    if nettoyage is None:
        raise HTTPException(
            status_code=404,
            detail="Nettoyage introuvable"
        )

    return nettoyage


def show_nettoyage_dates(nettoyage_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT date_debut, date_fin FROM nettoyage WHERE id = %s",
                    (nettoyage_id,)
                )
                nettoyage_dates = cursor.fetchone()
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

    if nettoyage_dates is None:
        raise HTTPException(
            status_code=404,
            detail="Nettoyage introuvable ou sans dates"
        )

    return nettoyage_dates


def show_nettoyage_personnel(id_personnel: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM nettoyage WHERE id_personnel = %s",
                    (id_personnel,)
                )
                nettoyage_personnel = cursor.fetchall()
            return nettoyage_personnel
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )
    

def show_nettoyage_chambre(id_chambre: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM nettoyage WHERE id_chambre = %s",
                    (id_chambre,)
                )
                nettoyage_chambre = cursor.fetchall()
            return nettoyage_chambre
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )



def supprimer_nettoyage(nettoyage_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM nettoyage WHERE id = %s",
                    (nettoyage_id,)
                )

                deleted = cursor.rowcount

            connection.commit()

            if deleted == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Nettoyage introuvable"
                )

            return {"message": "Nettoyage supprimé"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def insert_nettoyage(date_debut: str, id_chambre: int, id_personnel: int):
    personnel = show_personnel(id_personnel)
    role = show_role(personnel["id_role"])

    if role["nom"].lower() == "entretien":
        try:
            connection = get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO nettoyage (date_debut, id_chambre, id_personnel)
                        VALUES (%s, %s, %s)
                        """,
                        (date_debut, id_chambre, id_personnel)
                    )

                    nettoyage_id = cursor.lastrowid

                connection.commit()

                return {
                    "message": "Nettoyage ajouté",
                    "id": nettoyage_id
                }

            finally:
                connection.close()

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erreur de connexion à la BDD"
            )


def update_nettoyage(nettoyage_id: int, date_fin: str, id_personnel: int):
    personnel = show_personnel(id_personnel)
    role = show_role(personnel["id_role"])

    if role["nom"].lower() == "entretien":
        try:
            connection = get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE nettoyage SET date_fin = %s
                        WHERE id = %s
                        """,
                        (date_fin, nettoyage_id)
                    )

                    updated = cursor.rowcount

                connection.commit()

                if updated == 0:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT id FROM nettoyage WHERE id = %s",
                            (nettoyage_id,)
                        )
                        if cursor.fetchone() is None:
                            raise HTTPException(
                                status_code=404,
                                detail="Nettoyage introuvable"
                            )

                return {"message": "Nettoyage mis à jour"}

            finally:
                connection.close()

        except HTTPException:
            raise

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erreur lors de la modification du nettoyage"
            )