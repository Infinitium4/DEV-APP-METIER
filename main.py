from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes.client import router as client_router


app = FastAPI()

app.include_router(client_router)

@app.get("/")
def accueil():
    return {"message": "API connectée à MariaDB"}

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