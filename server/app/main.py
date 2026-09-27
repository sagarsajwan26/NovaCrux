from fastapi import FastAPI
from app.routes.api.v1 import router as ApiRoute
from app.core.exceptions.base import AppException
from app.core.exceptions.handler import app_exception_handler

app = FastAPI(title="NovaCrux API", version="1.0.0")


app.add_exception_handler(AppException, app_exception_handler)
app.include_router(ApiRoute, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Novacrux API is running"}
