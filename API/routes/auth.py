from fastapi import APIRouter, Depends
from securite import exiger_token_valide

#page d'authentification 
router = APIRouter(prefix="/auth", tags=["Authentification"])

#route de test pour les tockens
@router.get("/test")
def tester_token(donnees: dict = Depends(exiger_token_valide)):
    return {"identite": donnees["sub"]}
