#Import des library qui permettent de hasher et de gérer les errors
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError
from datetime import datetime,timedelta, timezone
import jwt
import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError

#Variable gestionnaire qui stock le password hasher
gestionnaire = PasswordHash.recommended()

#On hash le mot de passe
def hacher_mot_de_passe(mot_de_passe: str) -> str:
    return gestionnaire.hash(mot_de_passe)

#Vérifie si le mdp est valide à la connexion
def verifier_mot_de_passe(
    mot_de_passe: str,
    hash_stocke: str | None,
) -> bool:
    if not hash_stocke:
        return False

    try:
        return gestionnaire.verify(mot_de_passe, hash_stocke)
    except UnknownHashError:
        return False


#On créé le tocken pour l'utilisateur si il a bien le role valide 
def creer_token(
    id_utilisateur: int,
    type_utilisateur: str,
    cle_secrete: str,
) -> str:
    if type_utilisateur not in ("client", "personnel"):
        raise ValueError("Type utilisateur invalide")

    expiration = datetime.now(timezone.utc) + timedelta(minutes=30)

    return jwt.encode(
        {
            "sub": f"{type_utilisateur}:{id_utilisateur}",
            "exp": expiration,
        },
        cle_secrete,
        algorithm="HS256",
    )

#Vérifier si le tocken est valide 
def verifier_token(token: str, cle_secrete: str) -> dict:
    return jwt.decode(
        token,
        cle_secrete,
        algorithms=["HS256"],
        options={"require": ["sub", "exp"]},
    )

porteur_token = HTTPBearer(auto_error=False)

#On demande un tocken valide pour qu'il puisse rentrer sur la page
def exiger_token_valide(
    autorisation: HTTPAuthorizationCredentials | None = Depends(porteur_token),
) -> dict:
    if autorisation is None:
        raise HTTPException(
            status_code=401,
            detail="Token manquant",
            headers={"WWW-Authenticate": "Bearer"},
        )

    cle_secrete = os.getenv("JWT_SECRET_KEY")

    if not cle_secrete:
        raise HTTPException(
            status_code=503,
            detail="Clé JWT non configurée",
        )

    try:
        return verifier_token(autorisation.credentials, cle_secrete)
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None