from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.website import Website


class WebsiteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, website: Website) -> Website:
        self.db.add(website)
        await self.db.flush()
        await self.db.refresh(website)

        return website

    async def get_by_id(
        self,
        website_id: int,
    ) -> Website | None:
        result = await self.db.execute(select(Website).where(Website.id == website_id))

        return result.scalar_one_or_none()

    async def get_by_tenant_id(
        self,
        tenant_id: int,
    ) -> Website | None:
        result = await self.db.execute(
            select(Website).where(Website.tenant_id == tenant_id)
        )
        return result.scalar_one_or_none()
