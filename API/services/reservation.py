from API.database import get_connection
from fastapi import HTTPException
from datetime import date
from pymysql import MySQLError

def verifier_disponibilite(
    cursor,
    id_chambre: int,
    date_debut: date,
    date_fin: date,
):
    cursor.execute(
        """
        SELECT id
        FROM chambre
        WHERE id = %s
        FOR UPDATE
        """,
        (id_chambre,),
    )

    if cursor.fetchone() is None:
        raise HTTPException(
            status_code=404,
            detail="Chambre introuvable",
        )

    requete = """
        SELECT id
        FROM reservation
        WHERE id_chambre = %s
          AND date_debut < %s
          AND date_fin > %s
    """
    parametres = [id_chambre, date_fin, date_debut]

    requete += " LIMIT 1 FOR UPDATE"

    cursor.execute(requete, tuple(parametres))

    if cursor.fetchone() is not None:
        raise HTTPException(
            status_code=409,
            detail="Chambre déjà réservée sur cette période",
        )


def show_reservations():
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM reservation")
                reservations = cursor.fetchall()
            return reservations
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def show_reservation(reservation_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM reservation WHERE id = %s",
                    (reservation_id,)
                )
                reservation = cursor.fetchone()
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail="Reservation introuvable"
        )

    return reservation


def show_reservation_dates(reservation_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT date_debut, date_fin FROM reservation WHERE id = %s",
                    (reservation_id,)
                )
                reservation_dates = cursor.fetchone()
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

    if reservation_dates is None:
        raise HTTPException(
            status_code=404,
            detail="Reservation introuvable ou sans dates"
        )

    return reservation_dates


def show_reservation_client(id_client: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM reservation WHERE id_client = %s",
                    (id_client,)
                )
                reservation_client = cursor.fetchall()
            return reservation_client
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )
    

def show_reservation_chambre(id_chambre: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM reservation WHERE id_chambre = %s",
                    (id_chambre,)
                )
                reservation_chambre = cursor.fetchall()
            return reservation_chambre
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def supprimer_reservation(reservation_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM reservation WHERE id = %s",
                    (reservation_id,)
                )

                deleted = cursor.rowcount

            connection.commit()

            if deleted == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Reservation introuvable"
                )

            return {"message": "Reservation supprimé"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def insert_reservation(date_debut: date, date_fin: date, nb_personnes: int, id_chambre: int, id_client: int,):
    connection = None

    try:
        connection = get_connection()
        connection.begin()

        with connection.cursor() as cursor:
            verifier_disponibilite(cursor,id_chambre,date_debut,date_fin,)

            cursor.execute(
                "SELECT id FROM client WHERE id = %s",
                (id_client,),
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Client introuvable",
                )

            cursor.execute(
                """
                INSERT INTO reservation (date_debut, date_fin, nb_personnes, id_chambre, id_client)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (date_debut, date_fin, nb_personnes, id_chambre, id_client,),
            )

            reservation_id = cursor.lastrowid

        connection.commit()

        return {
            "message": "Réservation ajoutée",
            "id": reservation_id,
        }

    except HTTPException:
        if connection is not None:
            connection.rollback()
        raise

    except MySQLError:
        if connection is not None:
            connection.rollback()
        raise HTTPException(
            status_code=503,
            detail="Impossible d'enregistrer la réservation",
        ) from None

    finally:
        if connection is not None:
            connection.close()
