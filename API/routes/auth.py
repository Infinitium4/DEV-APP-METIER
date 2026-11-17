from fastapi import APIRouter
from API.services.auth import *
from API.models.auth import *

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/connexion")
def connexion(identifiants: Connexion):
    return authentifier(
        identifiants.telephone,
        identifiants.mot_de_passe,
        identifiants.type_utilisateur,
    )
