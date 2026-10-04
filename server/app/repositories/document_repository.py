from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document


class DocumenetRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, document: Document) -> Document:
        self.db.add(document)
        await self.db.flush()
        await self.db.refresh(document)
        return document

    async def get_by_id(self, document_id: int, tenant_id: int) -> Document | None:

        result = await self.db.execute(
            select(Document).where(
                Document.id == document_id, Document.tenant_id == tenant_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        slug: str,
        tenant_id: int,
    ) -> Document | None:
        result = await self.db.execute(
            select(Document).where(
                Document.slug == slug, Document.tenant_id == tenant_id
            )
        )

        return result.scalar_one_or_none()

    async def list_by_tenant(
        self,
        tenant_id: int,
    ) -> list[Document]:
        result = await self.db.execute(
            select(Document)
            .where(Document.tenant_id == tenant_id)
            .order_by(Document.created_at.desc())
        )

        return list(result.scalars().all())

    async def update(self, document: Document) -> Document:
        await self.db.flush()
        await self.db.refresh(document)

        return document
