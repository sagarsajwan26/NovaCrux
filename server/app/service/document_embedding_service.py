from app.core.ai.embedding import EmbeddingService
from app.core.vector.service import QdrantService
from app.models.document_chunk import DocumentChunk


class DocumentEmbeddingService:
    def __init__(
        self, embedding_service: EmbeddingService, qdrant_service: QdrantService
    ):
        self.embedding_service = embedding_service
        self.qdrant_service = qdrant_service

    async def index_chunk(self, chunk: DocumentChunk) -> None:

        embedding = await self.embedding_service.embed(chunk.content)

        payload = {
            "tenant_id": chunk.document_version_id,
            "document_version_id": chunk.document_version_id,
            "chunk_id": chunk.id,
            "chunk_index": chunk.chunk_index,
        }

        self.qdrant_service.upsert_embedding(
            point_id=chunk.id, embedding=embedding, payload=payload
        )
