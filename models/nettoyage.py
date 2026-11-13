from pydantic import BaseModel

class NettoyageCreate(BaseModel):
    date_debut: str
    date_fin: str
    id_chambre: int
    id_personnel: int

class NettoyageUpdate(BaseModel):
    date_fin: str