from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.website_repository import WebsiteRepository


class WebsiteService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.website_repository = WebsiteRepository(db)

    async def get_public_website(
        self,
        tenant_id: int,
    ):
        website = await self.website_repository.get_by_tenant_id(tenant_id)
        if website is None:
            return None

        if not website.is_active:
            return None

        return website
