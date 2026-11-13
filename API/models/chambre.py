from pydantic import BaseModel

class ChambreCreate(BaseModel):
    nb_lit: int

class ChambreUpdateReserve(BaseModel):
    reserve: bool

class ChambreUpdatePropre(BaseModel):
    propre: bool

class ChambreUpdate(BaseModel):
    nb_lit: int