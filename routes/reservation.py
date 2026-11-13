from fastapi import APIRouter
from services.reservation import *
from models.reservation import *

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.get("/")
def get_reservations():
    return show_reservations()

@router.get("/{reservation_id}")
def get_reservation(reservation_id: int):
    return show_reservation(reservation_id)

@router.get("/dates/{reservation_id}")
def get_reservation_num(reservation_id: int):
    return show_reservation_dates(reservation_id)

@router.get("/client/{client_id}")
def get_reservation_client(client_id: int):
    return show_reservation_client(client_id)

@router.get("/chambre/{chambre_id}")
def get_reservation_chambre(chambre_id: int):
    return show_reservation_chambre(chambre_id)


@router.delete("/{id_reservation}", status_code=204)
def delete_reservation(reservation_id: int):
    return supprimer_reservation(reservation_id)

@router.post("/", status_code=201)
def create_reservation(reservation: ReservationCreate):
    return insert_reservation(
        reservation.date_debut,
        reservation.date_fin,
        reservation.nb_personnes,
        reservation.id_chambre,
        reservation.id_client
    )

@router.put("/{reservation_id}")
def modifier_reservation(reservation_id: int, reservation: ReservationUpdate):
    return update_reservation(
        reservation_id,
        reservation.date_debut,
        reservation.date_fin,
        reservation.nb_personnes,
        reservation.id_chambre
    )