from pydantic import BaseModel

class ClientCreate(BaseModel):
    nom: str
    email: str
    telephone: str

class ClientUpdate(BaseModel):
    nom: str
    email: str
    telephone: str