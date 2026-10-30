from fastapi import APIRouter
from services.client import show_clients

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/")
def get_clients():
    return show_clients()