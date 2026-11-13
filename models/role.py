from pydantic import BaseModel

class RoleCreate(BaseModel):
    nom: str

class RoleUpdate(BaseModel):
    nom: str