from fastapi import APIRouter
from API.services.nettoyage import *
from API.models.nettoyage import *

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

@router.get("/personnel/{id_personnel}")
def get_nettoyage_client(id_personnel: int):
    return show_nettoyage_personnel(id_personnel)

@router.get("/chambre/{id_chambre}")
def get_nettoyage_chambre(id_chambre: int):
    return show_nettoyage_chambre(id_chambre)


@router.delete("/{nettoyage_id}", status_code=204)
def delete_nettoyage(nettoyage_id: int):
    return supprimer_nettoyage(nettoyage_id)

@router.post("/", status_code=201)
def create_nettoyage(nettoyage: NettoyageCreate):
    return insert_nettoyage(
        nettoyage.date_debut,
        nettoyage.id_chambre,
        nettoyage.id_personnel
    )

@router.put("/{nettoyage_id}")
def modifier_nettoyage(nettoyage_id: int, nettoyage: NettoyageUpdate):
    return update_nettoyage(
        nettoyage_id,
        nettoyage.date_fin,
        nettoyage.id_personnel
    )