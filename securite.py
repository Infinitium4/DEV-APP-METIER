#Import des library qui permettent de hasher et de gérer les errors
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError

#Variable gestionnaire qui stock le password hasher
gestionnaire = PasswordHash.recommended()


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