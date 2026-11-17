from fastapi import APIRouter, Depends, HTTPException
from API.dependances import ACCUEIL, RESERVATIONS, exiger_roles
from API.services.reservation import *
from API.models.reservation import *

router = APIRouter(prefix="/reservations", tags=["Reservations"])


def reservation_accessible(reservation_id: int, utilisateur: dict = Depends(exiger_roles(*RESERVATIONS))):
    reservation = show_reservation(reservation_id)
    if utilisateur["role"] == "client" and reservation["id_client"] != utilisateur["id"]:
        raise HTTPException(status_code=403, detail="Accès interdit")
    return reservation


@router.get("/", dependencies=[Depends(exiger_roles(*ACCUEIL))])
def get_reservations():
    return show_reservations()

@router.get("/{reservation_id}")
def get_reservation(reservation: dict = Depends(reservation_accessible)):
    return reservation

@router.get("/dates/{reservation_id}")
def get_reservation_dates(reservation_id: int, reservation: dict = Depends(reservation_accessible)):
    return show_reservation_dates(reservation_id)

@router.get("/client/{id_client}")
def get_reservation_client(id_client: int, utilisateur: dict = Depends(exiger_roles(*RESERVATIONS))):
    if utilisateur["role"] == "client" and utilisateur["id"] != id_client:
        raise HTTPException(status_code=403, detail="Accès interdit")
    return show_reservation_client(id_client)

@router.get("/chambre/{id_chambre}")
def get_reservation_chambre(id_chambre: int, utilisateur: dict = Depends(exiger_roles(*RESERVATIONS))):
    reservations = show_reservation_chambre(id_chambre)
    if utilisateur["role"] == "client":
        # Les disponibilités ne doivent pas exposer les autres clients.
        return [{"date_debut": r["date_debut"], "date_fin": r["date_fin"]} for r in reservations]
    return reservations


@router.delete("/{reservation_id}", status_code=204)
def delete_reservation(reservation_id: int, reservation: dict = Depends(reservation_accessible)):
    return supprimer_reservation(reservation_id)

@router.post("/", status_code=201)
def create_reservation(reservation: ReservationCreate, utilisateur: dict = Depends(exiger_roles(*RESERVATIONS))):
    if utilisateur["role"] == "client" and reservation.id_client != utilisateur["id"]:
        raise HTTPException(status_code=403, detail="Vous ne pouvez réserver que pour vous-même")
    id_client = utilisateur["id"] if utilisateur["role"] == "client" else reservation.id_client
    return insert_reservation(
        reservation.date_debut,
        reservation.date_fin,
        reservation.nb_personnes,
        reservation.id_chambre,
        id_client
    )

@router.put("/{reservation_id}")
def modifier_reservation(
    reservation_id: int,
    reservation: ReservationUpdate,
    existante: dict = Depends(reservation_accessible),
):
    return update_reservation(
        reservation_id,
        reservation.date_debut,
        reservation.date_fin,
        reservation.nb_personnes,
        reservation.id_chambre
    )
