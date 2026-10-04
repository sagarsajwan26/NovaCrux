import asyncio

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.core.documents.chunker import DocumentChunker
from app.core.documents.extractor import PDFTextExtractor
from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository,
)
from app.service.document_processing_service import (
    DocumentProcessingService,
)


async def main():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(DocumentChunk.document_version_id).limit(1))

        document_version_id = result.scalar_one_or_none()

        if document_version_id is None:
            print("No DocumentVersion found in PostgreSQL.")
            return

        service = DocumentProcessingService(
            chunk_repository=DocumentChunkRepository(db),
            extractor=PDFTextExtractor(),
            chunker=DocumentChunker(
                chunk_size=1000,
                chunk_overlap=200,
            ),
        )

        chunks = await service.process_pdf(
            file_path="test.pdf",
            document_version_id=document_version_id,
        )

        await db.commit()

        print(f"Successfully created {len(chunks)} chunks.")

        for chunk in chunks[:5]:
            print()
            print(f"Chunk {chunk.chunk_index} " f"(id={chunk.id})")
            print(chunk.content[:300])


if __name__ == "__main__":
    asyncio.run(main())
