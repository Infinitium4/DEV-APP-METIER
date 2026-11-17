from fastapi import APIRouter, Depends, HTTPException
from API.dependances import ACCUEIL, MANAGERS, exiger_roles, utilisateur_courant
from API.services.personnel import *
from API.models.personnel import *
from API.securite import hacher_mot_de_passe


router = APIRouter(prefix="/personnels", tags=["Personnels"])

@router.get("/", response_model=list[PersonnelPublic], dependencies=[Depends(exiger_roles(*ACCUEIL))])
def get_personnels():
    return show_personnels()

@router.get("/{personnel_id}", response_model=PersonnelPublic)
def get_personnel(personnel_id: int, utilisateur: dict = Depends(utilisateur_courant)):
    if utilisateur["role"] not in ACCUEIL and not (
        utilisateur["type"] == "personnel" and utilisateur["id"] == personnel_id
    ):
        raise HTTPException(status_code=403, detail="Accès interdit")
    return show_personnel(personnel_id)

@router.get("/roles/{id_role}", response_model=list[PersonnelPublic], dependencies=[Depends(exiger_roles(*ACCUEIL))])
def get_role_personnel(id_role: int):
    return show_role_personnel(id_role)


@router.delete("/{id_personnel}", status_code=204, dependencies=[Depends(exiger_roles(*MANAGERS))])
def delete_personnel(id_personnel: int):
    return supprimer_personnel(id_personnel)

@router.post("/", status_code=201, dependencies=[Depends(exiger_roles(*MANAGERS))])
def create_personnel(personnel: PersonnelCreate):
    hash_mdp = hacher_mot_de_passe(personnel.mot_de_passe)
    return insert_personnel(
        personnel.nom,
        personnel.telephone,
        personnel.id_role,
        hash_mdp
    )

@router.put("/{personnel_id}", dependencies=[Depends(exiger_roles(*MANAGERS))])
def modifier_personnel(personnel_id: int, personnel: PersonnelUpdate):
    return update_personnel(
        personnel_id,
        personnel.nom,
        personnel.telephone,
        personnel.id_role
    )
