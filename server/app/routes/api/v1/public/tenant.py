from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.service.website import WebsiteService
from app.core.dependencies.tenant_domain import get_tenant_from_domain

router = APIRouter()


@router.get("/")
async def get_public_tenant(
    tenant=Depends(get_tenant_from_domain), db: AsyncSession = Depends(get_db)
):
    website_service = WebsiteService(db)

    website = await website_service.get_public_website(tenant_id=tenant.id)

    if website is None:
        raise HTTPException(status_code=404, detail="Website not found")
    return {
        "tenant": {"id": tenant.id, "name": tenant.name, "slug": tenant.slug},
        "website": {
            "id": website.id,
            "name": website.name,
            "is_active": website.is_active,
        },
    }
