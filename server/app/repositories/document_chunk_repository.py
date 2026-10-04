from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, chunk: DocumentChunk) -> DocumentChunk:
        self.db.add(chunk)
        await self.db.flush()
        await self.db.refresh(chunk)
        return chunk

    async def get_by_id(
        self,
        chunk_id: int,
    ) -> DocumentChunk | None:
        result = await self.db.execute(
            select(DocumentChunk).where(DocumentChunk.id == chunk_id)
        )

        return result.scalar_one_or_none()

    async def list_by_version(
        self,
        document_version_id: int,
    ) -> list[DocumentChunk]:
        result = await self.db.execute(
            select(DocumentChunk)
            .where(DocumentChunk.document_version_id == document_version_id)
            .order_by(DocumentChunk.chunk_index.asc())
        )

        return list(result.scalars().all())

    async def create_many(
        self,
        chunks: list[DocumentChunk],
    ) -> list[DocumentChunk]:
        self.db.add_all(chunks)

        await self.db.flush()

        for chunk in chunks:
            await self.db.refresh(chunk)

        return chunks
