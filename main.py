from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from routes.chambre import router as chambre_router
from routes.client import router as client_router
from routes.nettoyage import router as nettoyage_router
from routes.personnel import router as personnel_router
from routes.reservation import router as reservation_router
from routes.role import router as role_router
from database import get_connection


app = FastAPI()


app.include_router(chambre_router)
app.include_router(client_router)
app.include_router(nettoyage_router)
app.include_router(personnel_router)
app.include_router(reservation_router)
app.include_router(role_router)


@app.get("/api")
def accueil():
    connection = None
    try:
        connection = get_connection()
        return {"message": "API connectée à MariaDB"}

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur de connexion à la BDD"
        )
    finally:
        if connection is not None:
            connection.close()

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "404 - Not Found",
            "message": "La route demandée n'existe pas",
            "path": request.url.path
        }
    )

app.mount("/", StaticFiles(directory=Path(__file__).resolve().parent / "frontend", html=True), name="frontend")
