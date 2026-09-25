from fastapi import FastAPI
from app.routes.api.v1 import router as ApiRoute

app = FastAPI(title="NovaCrux API", version="1.0.0")


app.include_router(ApiRoute, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Novacrux API is running"}
