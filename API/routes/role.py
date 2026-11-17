from fastapi import APIRouter, Depends, HTTPException
from API.dependances import ACCUEIL, MANAGERS, exiger_roles, utilisateur_courant
from API.services.role import *
from API.models.role import *

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", dependencies=[Depends(exiger_roles(*ACCUEIL))])
def get_roles():
    return show_roles()

@router.get("/{role_id}")
def get_role(role_id: int, utilisateur: dict = Depends(utilisateur_courant)):
    if utilisateur["role"] not in ACCUEIL and not (
        utilisateur["type"] == "personnel" and utilisateur["id_role"] == role_id
    ):
        raise HTTPException(status_code=403, detail="Accès interdit")
    return show_role(role_id)

@router.delete("/{role_id}", status_code=204, dependencies=[Depends(exiger_roles(*MANAGERS))])
def delete_role(role_id: int):
    return supprimer_role(role_id)

@router.post("/", status_code=201, dependencies=[Depends(exiger_roles(*MANAGERS))])
def create_role(role: RoleCreate):
    return insert_role(
        role.nom
    )

@router.put("/{role_id}", dependencies=[Depends(exiger_roles(*MANAGERS))])
def modifier_role(role_id: int, role: RoleUpdate):
    return update_role(
        role_id,
        role.nom
    )
