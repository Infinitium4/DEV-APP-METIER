from typing import Literal

from pydantic import BaseModel, Field


class Connexion(BaseModel):
    telephone: str = Field(min_length=1)
    mot_de_passe: str = Field(min_length=1)
    type_utilisateur: Literal["client", "personnel"]
