from fastapi import APIRouter
from app.routes.api.v1 import auth

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["authentication"])
