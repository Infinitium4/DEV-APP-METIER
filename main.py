from fastapi import FastAPI
from routes.client import router as client_router

app = FastAPI()

app.include_router(client_router)

@app.get("/")
def accueil():
    return {"message": "API connectée à MariaDB"}