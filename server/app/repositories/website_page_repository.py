from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.website_page import WebsitePage, PageStatus
from app.models.website_page import PageStatus


class WebsitePageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, page: WebsitePage) -> WebsitePage:
        self.db.add(page)
        await self.db.flush()
        await self.db.refresh(page)
        return page

    async def get_by_website_and_slug(
        self,
        website_id: int,
        slug: str,
    ) -> WebsitePage | None:
        result = await self.db.execute(
            select(WebsitePage).where(
                WebsitePage.website_id == website_id, WebsitePage.slug == slug
            )
        )

        return result.scalar_one_or_none()

    async def get_published_by_website_and_slug(
        self, website_id: int, slug: str
    ) -> WebsitePage | None:
        result = await self.db.execute(
            select(WebsitePage).where(
                WebsitePage.website_id == website_id,
                WebsitePage.slug == slug,
                WebsitePage.status == PageStatus.PUBLISHED,
            )
        )
        return result.scalar_one_or_none()

    async def get_published_by_website_and_slug(
        self, website_id: int, slug: str
    ) -> WebsitePage | None:

        result = await self.db.execute(
            select(WebsitePage).where(
                WebsitePage.website_id == website_id,
                WebsitePage.slug == slug,
                WebsitePage.status == PageStatus.PUBLISHED,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_website_id(
        self,
        website_id: int,
    ) -> list[WebsitePage]:
        result = await self.db.execute(
            select(WebsitePage)
            .where(WebsitePage.website_id == website_id)
            .order_by(WebsitePage.id)
        )
        return list(result.scalars().all())
