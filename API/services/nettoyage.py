from API.database import get_connection
from fastapi import HTTPException


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



def _verifier_nettoyage_actif(cursor, nettoyage_id: int, id_personnel: int | None):
    cursor.execute(
        "SELECT id, id_personnel, date_fin FROM nettoyage WHERE id = %s FOR UPDATE",
        (nettoyage_id,),
    )
    nettoyage = cursor.fetchone()
    if nettoyage is None:
        raise HTTPException(status_code=404, detail="Nettoyage introuvable")
    if id_personnel is not None and nettoyage["id_personnel"] != id_personnel:
        raise HTTPException(status_code=403, detail="Ce nettoyage appartient à un autre agent")
    if nettoyage["date_fin"] is not None:
        raise HTTPException(status_code=409, detail="Ce nettoyage est déjà terminé")


def supprimer_nettoyage(nettoyage_id: int, id_personnel: int | None):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                _verifier_nettoyage_actif(cursor, nettoyage_id, id_personnel)
                cursor.execute("DELETE FROM nettoyage WHERE id = %s", (nettoyage_id,))
            connection.commit()
            return {"message": "Nettoyage supprimé"}
        finally:
            connection.close()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression du nettoyage") from None


def insert_nettoyage(date_debut: str, id_chambre: int, id_personnel: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                # Le verrou empêche deux agents de s'affecter la même chambre.
                cursor.execute("SELECT id, propre FROM chambre WHERE id = %s FOR UPDATE", (id_chambre,))
                chambre = cursor.fetchone()
                if chambre is None:
                    raise HTTPException(status_code=404, detail="Chambre introuvable")
                if chambre["propre"]:
                    raise HTTPException(status_code=409, detail="Cette chambre est déjà propre")
                cursor.execute(
                    "SELECT id FROM nettoyage WHERE id_chambre = %s AND date_fin IS NULL LIMIT 1",
                    (id_chambre,),
                )
                if cursor.fetchone() is not None:
                    raise HTTPException(status_code=409, detail="Un nettoyage est déjà en cours")
                cursor.execute(
                    """
                    INSERT INTO nettoyage (date_debut, id_chambre, id_personnel)
                    VALUES (%s, %s, %s)
                    """,
                    (date_debut, id_chambre, id_personnel),
                )
                nettoyage_id = cursor.lastrowid
            connection.commit()
            return {"message": "Nettoyage ajouté", "id": nettoyage_id}
        finally:
            connection.close()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors de la création du nettoyage") from None


def update_nettoyage(nettoyage_id: int, date_fin: str, id_personnel: int | None):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                _verifier_nettoyage_actif(cursor, nettoyage_id, id_personnel)
                cursor.execute(
                    "UPDATE nettoyage SET date_fin = %s WHERE id = %s",
                    (date_fin, nettoyage_id),
                )
            connection.commit()
            return {"message": "Nettoyage mis à jour"}
        finally:
            connection.close()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors de la modification du nettoyage") from None
