from database import get_connection
from fastapi import HTTPException


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


def insert_reservation(date_debut: str, date_fin: str, nb_personnes: int, id_chambre: int, id_client: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO reservation (date_debut, date_fin, nb_personnes, id_chambre, id_client)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (date_debut, date_fin, nb_personnes, id_chambre, id_client)
                )

                reservation_id = cursor.lastrowid

            connection.commit()

            return {
                "message": "Reservation ajouté",
                "id": reservation_id
            }

        finally:
            connection.close()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def update_reservation(reservation_id: int, date_debut: str, date_fin: str, nb_personnes: int, id_chambre: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE reservation SET date_debut = %s, date_fin = %s, nb_personnes = %s, id_chambre = %s
                    WHERE id = %s
                    """,
                    (date_debut, date_fin, nb_personnes, id_chambre, reservation_id)
                )

                updated = cursor.rowcount

            updated.commit()

            if updated == 0:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM reservation WHERE id = %s",
                        (reservation_id,)
                    )
                    if cursor.fetchone() is None:
                        raise HTTPException(
                            status_code=404,
                            detail="Reservation introuvable"
                        )

            return {"message": "Reservation mis à jour"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la modification du reservation"
        )