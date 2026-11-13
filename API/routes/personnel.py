from fastapi import APIRouter
from API.services.personnel import *
from API.models.personnel import *

router = APIRouter(prefix="/personnels", tags=["Personnels"])

@router.get("/")
def get_personnels():
    return show_personnels()

@router.get("/{personnel_id}")
def get_personnel(personnel_id: int):
    return show_personnel(personnel_id)

@router.get("roles/{id_role}")
def get_role_personnel(id_role: int):
    return show_role_personnel(id_role)


@router.delete("/{id_personnel}", status_code=204)
def delete_personnel(personnel_id: int):
    return supprimer_personnel(personnel_id)

@router.post("/", status_code=201)
def create_personnel(personnel: PersonnelCreate):
    return insert_personnel(
        personnel.nom,
        personnel.telephone,
        personnel.id_role,
        personnel.mot_de_passe_hash
    )

@router.put("/{personnel_id}")
def modifier_personnel(personnel_id: int, personnel: PersonnelUpdate):
    return update_personnel(
        personnel_id,
        personnel.nom,
        personnel.telephone,
        personnel.id_role
    )