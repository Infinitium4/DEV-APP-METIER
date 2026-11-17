from fastapi import APIRouter, Depends, HTTPException
from API.dependances import ACCUEIL, RESERVATIONS, exiger_roles
from API.services.client import *
from API.models.client import *
from API.securite import hacher_mot_de_passe


router = APIRouter(prefix="/clients", tags=["Clients"])
router_public = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/", response_model=list[ClientPublic], dependencies=[Depends(exiger_roles(*ACCUEIL))])
def get_clients():
    return show_clients()

@router.get("/{client_id}", response_model=ClientPublic)
def get_client(client_id: int, utilisateur: dict = Depends(exiger_roles(*RESERVATIONS))):
    if utilisateur["role"] == "client" and utilisateur["id"] != client_id:
        raise HTTPException(status_code=403, detail="Accès interdit")
    return show_client(client_id)



@router.delete("/{client_id}", status_code=204, dependencies=[Depends(exiger_roles(*ACCUEIL))])
def delete_client(client_id: int):
    return supprimer_client(client_id)

@router_public.post("/", status_code=201)
def create_client(client: ClientCreate):
    hash_mdp = hacher_mot_de_passe(client.mot_de_passe)
    return insert_client(
        client.nom,
        client.prenom,
        client.telephone,
        hash_mdp
    )

@router.put("/{client_id}")
def modifier_client(client_id: int, client: ClientUpdate, utilisateur: dict = Depends(exiger_roles(*RESERVATIONS))):
    if utilisateur["role"] == "client" and utilisateur["id"] != client_id:
        raise HTTPException(status_code=403, detail="Accès interdit")
    return update_client(
        client_id,
        client.nom,
        client.prenom,
        client.telephone
    )
