from pydantic import BaseModel

class NettoyageCreate(BaseModel):
    date_debut: str
    id_chambre: int
    # Conservé pour les anciens clients HTTP ; l'identité vient du JWT.
    id_personnel: int | None = None

class NettoyageUpdate(BaseModel):
    date_fin: str
    id_personnel: int | None = None
