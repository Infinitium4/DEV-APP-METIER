from pydantic import BaseModel

class ClientCreate(BaseModel):
    nom: str
    prenom: str
    telephone: str
    mot_de_passe: str

class ClientPublic(BaseModel):
    id: int
    nom: str
    prenom: str
    telephone: str | None

class ClientUpdate(BaseModel):
    nom: str
    prenom: str
    telephone: str
