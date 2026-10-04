from app.core.documents.chunker import DocumentChunker
from app.core.documents.extractor import PDFTextExtractor
from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import DocumentChunkRepository


class DocumentProcessingService:
    def __init__(
        self,
        chunk_repository: DocumentChunkRepository,
        extractor: PDFTextExtractor,
        chunker: DocumentChunker,
    ):
        self.chunk_repository = chunk_repository
        self.extractor = extractor
        self.chunker = chunker

    async def process_pdf(
        self,
        file_path: str,
        document_version_id: int,
    ) -> list[DocumentChunk]:
        text = self.extractor.extract(file_path)

        chunks = self.chunker.chunk_text(text)

        document_chunks: list[DocumentChunk] = []
        for index, content in enumerate(chunks):
            document_chunks.append(
                DocumentChunk(
                    document_version_id=document_version_id,
                    chunk_index=index,
                    content=content,
                )
            )

        return await self.chunk_repository.create(document_chunks)
