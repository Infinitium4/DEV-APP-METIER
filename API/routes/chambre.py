from fastapi import APIRouter
from API.services.chambre import *
from API.models.chambre import *

router = APIRouter(prefix="/chambres", tags=["Chambres"])

@router.get("/")
def get_chambres():
    return show_chambres()

@router.get("/sales")
def get_chambre_num():
    return show_chambres_sales()

@router.get("/propre/{chambre_id}")
def get_chambre_proprete(chambre_id: int):
    return show_chambre_proprete(chambre_id)

@router.get("/libres")
def get_chambre_libres():
    return show_chambres_libres()

@router.get("/libres/{chambre_id}")
def get_chambre_libre(chambre_id: int):
    return show_chambre_libre(chambre_id)

@router.get("/reservable")
def get_chambre_num():
    return show_chambre_reservable()



@router.get("/{chambre_id}")
def get_chambre(chambre_id: int):
    return show_chambre(chambre_id)

@router.delete("/{chambre_id}", status_code=204)
def delete_chambre(chambre_id: int):
    return supprimer_chambre(chambre_id)

@router.post("/", status_code=201)
def create_chambre(chambre: ChambreCreate):
    return insert_chambre(
        chambre.nb_lit
    )

@router.put("/proprete/{chambre_id}")
def modifier_chambre_proprete(chambre_id: int, chambre: ChambreUpdatePropre):
    return update_chambre_proprete(
        chambre_id,
        chambre.propre,
    )

@router.put("/reserve/{chambre_id}")
def modifier_chambre_reserve(chambre_id: int, chambre: ChambreUpdateReserve):
    return update_chambre_reserve(
        chambre_id,
        chambre.reserve,
    )

@router.put("/{chambre_id}")
def modifier_chambre(chambre_id: int, chambre: ChambreUpdate):
    return update_chambre(
        chambre_id,
        chambre.nb_lit,
    )