from pydantic import BaseModel

class ReservationCreate(BaseModel):
    date_debut: str
    date_fin: str
    nb_personnes: int
    id_chambre: int
    id_client: int

class ReservationUpdate(BaseModel):
    date_debut: str
    date_fin: str
    nb_personnes: int
    id_chambre: int