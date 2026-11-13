from fastapi import APIRouter
from API.services.client import *
from API.models.client import *

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/", response_model=list[ClientPublic])
def get_clients():
    return show_clients()

@router.get("/{client_id}", response_model=ClientPublic)
def get_client(client_id: int):
    return show_client(client_id)

@router.delete("/{id_client}", status_code=204)
def delete_client(client_id: int):
    return supprimer_client(client_id)

@router.post("/", status_code=201)
def create_client(client: ClientCreate):
    return insert_client(
        client.nom,
        client.email,
        client.telephone,
        client.mot_de_passe_hash
    )

@router.put("/{client_id}")
def modifier_client(client_id: int, client: ClientUpdate):
    return update_client(
        client_id,
        client.nom,
        client.prenom,
        client.num_tel
    )
