from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document_version import DocumentVersion


class DocumentVersionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, version: DocumentVersion) -> DocumentVersion:
        self.db.add(version)
        await self.db.flush()
        await self.db.refresh(version)

        return version

    async def get_by_id(self, version_id: int) -> DocumentVersion | None:
        result = await self.db.execute(
            select(DocumentVersion).where(
                DocumentVersion.id == version_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_latest(
        self,
        document_id: int,
    ) -> DocumentVersion | None:
        result = await self.db.execute(
            select(DocumentVersion)
            .where(
                DocumentVersion.document_id == document_id,
            )
            .order_by(DocumentVersion.version_number.desc())
            .limit(1)
        )

        return result.scalar_one_or_none()

    async def list_by_document(
        self,
        document_id: int,
    ) -> list[DocumentVersion]:
        result = await self.db.execute(
            select(DocumentVersion)
            .where(
                DocumentVersion.document_id == document_id,
            )
            .order_by(DocumentVersion.version_number.asc())
        )

        return list(result.scalars().all())
