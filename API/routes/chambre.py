from fastapi import APIRouter, Depends, HTTPException
from API.services.chambre import *
from API.models.chambre import *
from API.dependances import ACCUEIL, CHAMBRES_SALES, MANAGERS, RESERVATIONS, exiger_roles

router = APIRouter(prefix="/chambres", tags=["Chambres"])

@router.get("/")
def get_chambres(utilisateur: dict = Depends(exiger_roles(*RESERVATIONS))):
    chambres = show_chambres()
    if utilisateur["role"] == "client":
        return [c for c in chambres if c["propre"] and not c["reserve"]]
    return chambres

@router.get(
    "/sales",
    dependencies=[Depends(exiger_roles(*CHAMBRES_SALES))],
)
def get_chambre_sales():
    return show_chambres_sales()

@router.get("/propre/{chambre_id}", dependencies=[Depends(exiger_roles(*CHAMBRES_SALES))])
def get_chambre_proprete(chambre_id: int):
    return show_chambre_proprete(chambre_id)

@router.get("/libres", dependencies=[Depends(exiger_roles(*RESERVATIONS))])
def get_chambre_libres():
    return show_chambres_libres()

@router.get("/libres/{chambre_id}", dependencies=[Depends(exiger_roles(*RESERVATIONS))])
def get_chambre_libre(chambre_id: int):
    return show_chambre_libre(chambre_id)

@router.get("/reservable", dependencies=[Depends(exiger_roles(*RESERVATIONS))])
def get_chambre_reservable():
    return show_chambre_reservable()



@router.get("/{chambre_id}")
def get_chambre(chambre_id: int, utilisateur: dict = Depends(exiger_roles(*RESERVATIONS))):
    chambre = show_chambre(chambre_id)
    if utilisateur["role"] == "client" and (not chambre["propre"] or chambre["reserve"]):
        raise HTTPException(status_code=403, detail="Chambre indisponible")
    return chambre

@router.delete("/{chambre_id}", status_code=204, dependencies=[Depends(exiger_roles(*ACCUEIL))])
def delete_chambre(chambre_id: int):
    return supprimer_chambre(chambre_id)

@router.post("/", status_code=201, dependencies=[Depends(exiger_roles(*ACCUEIL))])
def create_chambre(chambre: ChambreCreate):
    return insert_chambre(
        chambre.nb_lit
    )

@router.put("/proprete/{chambre_id}")
def modifier_chambre_proprete(chambre_id: int, chambre: ChambreUpdatePropre, utilisateur: dict = Depends(exiger_roles(*CHAMBRES_SALES))):
    if chambre.propre and utilisateur["role"] not in ("entretien", *MANAGERS):
        raise HTTPException(status_code=403, detail="Vous ne pouvez pas terminer un nettoyage")
    proprietaire = utilisateur["id"] if utilisateur["role"] == "entretien" else None
    return update_chambre_proprete(
        chambre_id,
        chambre.propre,
        proprietaire,
    )

@router.put("/reserve/{chambre_id}", dependencies=[Depends(exiger_roles(*ACCUEIL))])
def modifier_chambre_reserve(chambre_id: int, chambre: ChambreUpdateReserve):
    return update_chambre_reserve(
        chambre_id,
        chambre.reserve,
    )

@router.put("/{chambre_id}", dependencies=[Depends(exiger_roles(*ACCUEIL))])
def modifier_chambre(chambre_id: int, chambre: ChambreUpdate):
    return update_chambre(
        chambre_id,
        chambre.nb_lit,
    )
