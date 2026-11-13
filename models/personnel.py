from pydantic import BaseModel

class PersonnelCreate(BaseModel):
    nom: str
    telephone: str
    id_role: int

class PersonnelUpdate(BaseModel):
    nom: str
    telephone: str
    id_role: int