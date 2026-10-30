from fastapi import APIRouter
from services.client import *
from models.client import *

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/")
def get_clients():
    return show_clients()

@router.get("/{client_id}")
def get_client(client_id: int):
    return show_client(client_id)

@router.get("/num/{client_id}")
def get_client_num(client_id: int):
    return show_client_num(client_id)

@router.delete("/{id_client}")
def delete_client(client_id: int):
    return supprimer_client(client_id)

@router.post("/")
def create_client(client: ClientCreate):
    return insert_client(
        client.nom,
        client.email,
        client.telephone
    )

@router.put("/{client_id}")
def modifier_client(client_id: int, client: ClientUpdate):
    return update_client(
        client_id,
        client.nom,
        client.email,
        client.telephone
    )