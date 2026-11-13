from pydantic import BaseModel

class PersonnelCreate(BaseModel):
    nom: str
    telephone: str
    id_role: int
    mot_de_passe_hash: str

class PersonnelUpdate(BaseModel):
    nom: str
    telephone: str
    id_role: int