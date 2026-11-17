from fastapi import Depends, HTTPException
from unicodedata import combining, normalize

from API.securite import exiger_token_valide
from API.services.client import show_client
from API.services.personnel import show_personnel
from API.services.role import show_role


# Groupes utilisés dans les routes, d'après les droits de notes.md.
MANAGERS = ("manager_hotel", "manager_general")
ACCUEIL = ("receptionniste", *MANAGERS)
RESERVATIONS = ("client", *ACCUEIL)
NETTOYAGES = ("entretien", *MANAGERS)
CHAMBRES_SALES = ("entretien", *ACCUEIL)


def normaliser_role(nom: str) -> str:
    nom = "".join(c for c in normalize("NFKD", nom.casefold()) if not combining(c))
    nom = " ".join(nom.replace("’", "'").replace("_", " ").split())
    return {
        "accueil": "receptionniste",
        "personnel d'accueil": "receptionniste",
        "personnel d'entretien": "entretien",
        "personnel de securite": "securite",
        "manager de garde": "manager_garde",
        "manager garde": "manager_garde",
        "manager hotel": "manager_hotel",
        "manager general": "manager_general",
    }.get(nom, nom)


def utilisateur_courant(donnees: dict = Depends(exiger_token_valide)) -> dict:
    
    try:
        # On extrait le type de compte et l'identifiant du JWT vérifié.
        type_compte, identifiant = donnees["sub"].split(":")
        identifiant = int(identifiant)
        #Si l'identifiant n'est pas valide on renvoie une Error
        if type_compte not in ("client", "personnel") or identifiant <= 0:
            raise ValueError()

    except (KeyError, ValueError, TypeError, AttributeError):
        raise HTTPException(
            status_code=401,
            detail="Identité invalide",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    try:
        id_role = None
        # On vérifie que le compte existe toujours.
        if type_compte == "client":
            show_client(identifiant)
            role = "client"
        else:
            # Le rôle du personnel est relu en BDD à chaque requête.
            personnel = show_personnel(identifiant)
            id_role = personnel["id_role"]
            role = normaliser_role(show_role(id_role)["nom"])
            if role == "client":
                raise HTTPException(status_code=403, detail="Rôle personnel invalide")
    #on renvoie une error si le compte ou le role est introuvable
    except HTTPException as erreur:
        if erreur.status_code == 404:
            raise HTTPException(
                status_code=401,
                detail="Compte ou rôle introuvable",
                headers={"WWW-Authenticate": "Bearer"},
            ) from None
        raise

    return {"id": identifiant, "type": type_compte, "role": role, "id_role": id_role}


def exiger_roles(*roles_autorises: str):
    # On prépare les rôles autorisés en ignorant la casse et les espaces autour.
    roles = {normaliser_role(role) for role in roles_autorises}

    def verifier(utilisateur: dict = Depends(utilisateur_courant)) -> dict: 
        #Récupération du role du user actif 
        role = normaliser_role(utilisateur["role"])


        if role not in roles:
            raise HTTPException(status_code=403, detail="Accès interdit")

        return utilisateur

    return verifier
