from pydantic import BaseModel

class ClientCreate(BaseModel):
    nom: str
    email: str
    telephone: str
    mot_de_passe_hash: str

class ClientUpdate(BaseModel):
    nom: str
    email: str
    telephone: str