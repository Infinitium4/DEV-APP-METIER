from pydantic import BaseModel

class PersonnelCreate(BaseModel):
    nom: str
    prenom: str
    telephone: str
    id_role: int
    mot_de_passe: str

class PersonnelUpdate(BaseModel):
    nom: str
    prenom: str
    telephone: str
    id_role: int

class PersonnelPublic(BaseModel):
    id: int
    nom: str
    prenom: str
    telephone: str