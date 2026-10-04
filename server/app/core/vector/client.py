from qdrant_client import QdrantClient
from app.core.vector.config import qdrant_settings


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=qdrant_settings.QDRANT_URL)
