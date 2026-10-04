from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from app.core.vector.config import qdrant_settings
from app.core.vector.client import get_qdrant_client


class QdrantService:
    def __init__(self):
        self.client = QdrantClient = get_qdrant_client()
        self.collection_name = qdrant_settings.QDRANT_COLLECTION

    def upsert_embedding(
        self,
        point_id: int,
        embedding: list[float],
        payload: dict,
    ) -> None:
        self.client.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(id=point_id, vector=embedding, payload=payload)],
        )

    def search(self, embedding: list[float], limit: int = 5):
        result = self.client.query_points(
            collection_name=self.collection_name, query=embedding, limit=limit
        )

        return result.points

    def delete(self, point_id: int) -> None:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=[point_id],
        )
