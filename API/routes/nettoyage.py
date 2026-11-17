from fastapi import APIRouter, Depends, HTTPException
from API.dependances import MANAGERS, NETTOYAGES, exiger_roles
from API.services.nettoyage import *
from API.models.nettoyage import *

router = APIRouter(
    prefix="/nettoyages", tags=["Nettoyages"],
    dependencies=[Depends(exiger_roles(*NETTOYAGES))],
)

@router.get("/")
def get_nettoyages():
    return show_nettoyages()

@router.get("/{nettoyage_id}")
def get_nettoyage(nettoyage_id: int):
    return show_nettoyage(nettoyage_id)

@router.get("/dates/{nettoyage_id}")
def get_nettoyage_dates(nettoyage_id: int):
    return show_nettoyage_dates(nettoyage_id)

@router.get("/personnel/{id_personnel}")
def get_nettoyage_client(id_personnel: int, utilisateur: dict = Depends(exiger_roles(*NETTOYAGES))):
    if utilisateur["role"] not in MANAGERS and utilisateur["id"] != id_personnel:
        raise HTTPException(status_code=403, detail="Accès interdit")
    return show_nettoyage_personnel(id_personnel)

@router.get("/chambre/{id_chambre}")
def get_nettoyage_chambre(id_chambre: int):
    return show_nettoyage_chambre(id_chambre)


@router.delete("/{nettoyage_id}", status_code=204)
def delete_nettoyage(nettoyage_id: int, utilisateur: dict = Depends(exiger_roles(*NETTOYAGES))):
    proprietaire = None if utilisateur["role"] in MANAGERS else utilisateur["id"]
    return supprimer_nettoyage(nettoyage_id, proprietaire)

@router.post("/", status_code=201)
def create_nettoyage(nettoyage: NettoyageCreate, utilisateur: dict = Depends(exiger_roles(*NETTOYAGES))):
    return insert_nettoyage(
        nettoyage.date_debut,
        nettoyage.id_chambre,
        utilisateur["id"]
    )

@router.put("/{nettoyage_id}")
def modifier_nettoyage(nettoyage_id: int, nettoyage: NettoyageUpdate, utilisateur: dict = Depends(exiger_roles(*NETTOYAGES))):
    proprietaire = None if utilisateur["role"] in MANAGERS else utilisateur["id"]
    return update_nettoyage(
        nettoyage_id,
        nettoyage.date_fin,
        proprietaire
    )
