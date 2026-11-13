from pydantic import BaseModel

class ClientCreate(BaseModel):
    nom: str
    prenom: str
    num_tel: str
    mot_de_passe: str

class ClientPublic(BaseModel):
    id: int
    nom: str
    prenom: str
    num_tel: str

class ClientUpdate(BaseModel):
    nom: str
    prenom: str
    num_tel: str
