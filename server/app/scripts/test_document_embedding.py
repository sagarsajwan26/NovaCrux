import asyncio

from sqlalchemy import select

from app.core.ai.embedding import EmbeddingService
from app.core.vector.service import QdrantService
from app.db.session import AsyncSessionLocal
from app.models.document_chunk import DocumentChunk
from app.service.document_embedding_service import DocumentEmbeddingService


async def main():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(DocumentChunk).order_by(DocumentChunk.id.asc()).limit(1)
        )

        chunk = result.scalar_one_or_none()

        if chunk is None:
            print("No DocumentChunk found in PostgreSQL. Creating a mock chunk for testing...")
            chunk = DocumentChunk(
                id=1,
                document_version_id=1,
                chunk_index=0,
                content="This is a mock document chunk to test the embedding service."
            )
        else:
            print("Found DocumentChunk:")
            print("ID:", chunk.id)
            print("Version ID:", chunk.document_version_id)
            print("Chunk index:", chunk.chunk_index)
            print("Content:", chunk.content[:200])

        embedding_service = EmbeddingService()
        qdrant_service = QdrantService()

        service = DocumentEmbeddingService(
            embedding_service=embedding_service,
            qdrant_service=qdrant_service,
        )

        await service.index_chunk(
            chunk=chunk
        )

        print("Chunk successfully indexed into Qdrant.")


if __name__ == "__main__":
    asyncio.run(main())
