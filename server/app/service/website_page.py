from sqlalchemy.ext.asyncio import AsyncSession
from app.models.website_page import WebsitePage, PageStatus
from app.repositories.website_page_repository import WebsitePageRepository
from app.repositories.website_repository import WebsiteRepository
from app.schemas.website_pages import WebsitePageCreate, WebsitePageUpdate


class WebsitePageService:
    def __init__(self, db: AsyncSession):
        self.db = db

        self.page_repository = WebsitePageRepository(db)
        self.website_repository = WebsiteRepository(db)

    async def create_page(self, tenant_id: int, data: WebsitePageCreate) -> WebsitePage:
        website = await self.website_repository.get_by_tenant_id(tenant_id)

        if website is None:
            raise ValueError("Website not found")

        existing_page = await self.page_repository.get_by_website_and_slug(
            website_id=website.id, slug=data.slug
        )

        if existing_page is not None:
            raise ValueError(f'Page with slug "{data.slug}" already exists.')

        page = WebsitePage(
            website_id=website.id,
            title=data.title,
            slug=data.slug,
            status=PageStatus.DRAFT,
        )
        return await self.page_repository.create(page)

    async def get_pages(
        self,
        tenant_id: int,
    ) -> list[WebsitePage]:
        website = await self.website_repository.get_by_tenant_id(tenant_id)

        if website is None:
            raise ValueError("Website not found")

        return await self.page_repository.get_by_website_id(website.id)
