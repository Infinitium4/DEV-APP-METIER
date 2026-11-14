from fastapi import APIRouter
from API.services.role import *
from API.models.role import *

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/")
def get_roles():
    return show_roles()

@router.get("/{role_id}")
def get_role(role_id: int):
    return show_role(role_id)

@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: int):
    return supprimer_role(role_id)

@router.post("/", status_code=201)
def create_role(role: RoleCreate):
    return insert_role(
        role.nom
    )

@router.put("/{role_id}")
def modifier_role(role_id: int, role: RoleUpdate):
    return update_role(
        role_id,
        role.nom
    )