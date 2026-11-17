from pydantic import BaseModel

class PersonnelCreate(BaseModel):
    nom: str
    prenom: str
    telephone: str
    id_role: int
    mot_de_passe: str

class PersonnelPublic(BaseModel):
    id: int
    nom: str
    telephone: str | None
    id_role: int

class PersonnelUpdate(BaseModel):
    nom: str
    prenom: str
    telephone: str
    id_role: int
