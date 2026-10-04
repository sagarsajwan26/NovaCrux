from pydantic_settings import BaseSettings, SettingsConfigDict


class QdrantSettings(BaseSettings):
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "novacrux_documents"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


qdrant_settings = QdrantSettings()
