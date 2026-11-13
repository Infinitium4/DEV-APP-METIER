from fastapi import APIRouter
from services.nettoyage import *
from models.nettoyage import *

router = APIRouter(prefix="/nettoyages", tags=["Nettoyages"])

@router.get("/")
def get_nettoyages():
    return show_nettoyages()

@router.get("/{nettoyage_id}")
def get_nettoyage(nettoyage_id: int):
    return show_nettoyage(nettoyage_id)

@router.get("/dates/{nettoyage_id}")
def get_nettoyage_num(nettoyage_id: int):
    return show_nettoyage_dates(nettoyage_id)

@router.get("/personnel/{personnel_id}")
def get_nettoyage_client(personnel_id: int):
    return show_nettoyage_personnel(personnel_id)

@router.get("/chambre/{chambre_id}")
def get_nettoyage_chambre(chambre_id: int):
    return show_nettoyage_chambre(chambre_id)


@router.delete("/{id_nettoyage}", status_code=204)
def delete_nettoyage(nettoyage_id: int):
    return supprimer_nettoyage(nettoyage_id)

@router.post("/", status_code=201)
def create_nettoyage(nettoyage: NettoyageCreate):
    return insert_nettoyage(
        nettoyage.date_debut,
        nettoyage.date_fin,
        nettoyage.id_chambre,
        nettoyage.id_personnel
    )

@router.put("/{nettoyage_id}")
def modifier_nettoyage(nettoyage_id: int, nettoyage: NettoyageUpdate):
    return update_nettoyage(
        nettoyage_id,
        nettoyage.date_debut,
        nettoyage.date_fin,
        nettoyage.id_chambre,
        nettoyage.id_personnel
    )