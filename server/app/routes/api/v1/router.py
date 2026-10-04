from fastapi import APIRouter
from app.routes.api.v1 import auth
from app.routes.api.v1.public import tenant

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["authentication"])
router.include_router(tenant.router, prefix="/public/tenant", tags=["public-tenant"])
