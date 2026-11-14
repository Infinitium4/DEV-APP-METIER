from fastapi import APIRouter
from API.services.reservation import *
from API.models.reservation import *

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.get("/")
def get_reservations():
    return show_reservations()

@router.get("/{reservation_id}")
def get_reservation(reservation_id: int):
    return show_reservation(reservation_id)

@router.get("/dates/{reservation_id}")
def get_reservation_dates(reservation_id: int):
    return show_reservation_dates(reservation_id)

@router.get("/client/{id_client}")
def get_reservation_client(id_client: int):
    return show_reservation_client(id_client)

@router.get("/chambre/{id_chambre}")
def get_reservation_chambre(id_chambre: int):
    return show_reservation_chambre(id_chambre)


@router.delete("/{reservation_id}", status_code=204)
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