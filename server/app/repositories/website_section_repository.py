from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.website_section import WebsiteSection


class WebsiteSectionRepository:
    def __init__(self, db: AsyncSession):

        self.db = db

    async def create(
        self,
        section: WebsiteSection,
    ) -> WebsiteSection:
        self.db.add(section)
        await self.db.add(section)
        await self.db.flush()
        await self.db.refresh(section)
        return section

    async def get_by_page_id(
        self,
        page_id: int,
    ) -> list[WebsiteSection]:
        result = await self.db.execute(
            select(WebsiteSection)
            .where(WebsiteSection.page_id == page_id)
            .order_by(WebsiteSection.position)
        )

        return list(result.scalars().all())
