from pydantic import BaseModel

class ClientCreate(BaseModel):
    nom: str
    email: str
    telephone: str
    mot_de_passe_hash: str

class ClientUpdate(BaseModel):
    nom: str
    prenom: str
    telephone: str

class ClientPublic(BaseModel):
    id: int
    nom: str
    prenom: str
    telephone: str
