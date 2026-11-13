from database import get_connection
from fastapi import HTTPException


def show_chambres():
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM chambre")
                chambres = cursor.fetchall()
            return chambres
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def show_chambre(chambre_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM chambre WHERE id = %s",
                    (chambre_id,)
                )
                chambre = cursor.fetchone()
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

    if chambre is None:
        raise HTTPException(
            status_code=404,
            detail="chambre introuvable"
        )

    return chambre


def show_chambres_sales():
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT numero, nb_lit FROM chambre WHERE propre=FALSE"
                )
                chambres_sales = cursor.fetchall()
            return chambres_sales
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def show_chambre_proprete(chambre_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT propre FROM chambre WHERE id = %s",
                    (chambre_id,)
                )
                chambre_proprete = cursor.fetchone()
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

    if chambre_proprete is None:
        raise HTTPException(
            status_code=404,
            detail="chambre introuvable ou sans proprete defini"
        )

    return chambre_proprete


def show_chambres_libres():
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT numero, nb_lit FROM chambre WHERE reserve=FALSE"
                )
                chambres_libres = cursor.fetchall()
            return chambres_libres
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def show_chambre_libre(chambre_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT reserve FROM chambre WHERE id = %s",
                    (chambre_id,)
                )
                chambre_reserve = cursor.fetchone()
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )

    if chambre_reserve is None:
        raise HTTPException(
            status_code=404,
            detail="chambre introuvable ou sans statut reservé defini"
        )

    return chambre_reserve


def show_chambre_reservable():
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT numero, nb_lit FROM chambre WHERE reserve=FALSE AND propre=TRUE"
                )
                chambres_reservables = cursor.fetchall()
            return chambres_reservables
        finally:
            connection.close()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )



def supprimer_chambre(chambre_id: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM chambre WHERE id = %s",
                    (chambre_id,)
                )

                deleted = cursor.rowcount

            connection.commit()

            if deleted == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Chambre introuvable"
                )

            return {"message": "Chambre supprimé"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def insert_chambre(nb_lit: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO chambre (nb_lit, reserve, propre)
                    VALUES (%s, FALSE, TRUE)
                    """,
                    (nb_lit,)
                )

                chambre_id = cursor.lastrowid

            connection.commit()

            return {
                "message": "Chambre ajouté",
                "id": chambre_id
            }

        finally:
            connection.close()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )


def update_chambre_proprete(chambre_id: int, propre: bool):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE chambre SET propre = %s
                    WHERE id = %s
                    """,
                    (propre, chambre_id)
                )

                updated = cursor.rowcount

            updated.commit()

            if updated == 0:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM chambre WHERE id = %s",
                        (chambre_id,)
                    )
                    if cursor.fetchone() is None:
                        raise HTTPException(
                            status_code=404,
                            detail="Chambre introuvable"
                        )

            return {"message": "Chambre mise à jour"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la modification de la chambre"
        )


def update_chambre_reserve(chambre_id: int, reserve: bool):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE chambre SET reserve = %s
                    WHERE id = %s
                    """,
                    (reserve, chambre_id)
                )

                updated = cursor.rowcount

            updated.commit()

            if updated == 0:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM chambre WHERE id = %s",
                        (chambre_id,)
                    )
                    if cursor.fetchone() is None:
                        raise HTTPException(
                            status_code=404,
                            detail="Chambre introuvable"
                        )

            return {"message": "Chambre mise à jour"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la modification de la chambre"
        )


def update_chambre(chambre_id: int, nb_lit: int):
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE chambre SET nb_lit = %s
                    WHERE id = %s
                    """,
                    (nb_lit, chambre_id)
                )

                updated = cursor.rowcount

            updated.commit()

            if updated == 0:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM chambre WHERE id = %s",
                        (chambre_id,)
                    )
                    if cursor.fetchone() is None:
                        raise HTTPException(
                            status_code=404,
                            detail="Chambre introuvable"
                        )

            return {"message": "Chambre mise à jour"}

        finally:
            connection.close()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la modification de la chambre"
        )