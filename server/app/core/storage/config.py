from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageSettings(BaseSettings):
    S3_ENDPOINT_URL: str = "http://localhost:4566"
    S3_REGION: str = "us-east-1"

    AWS_ACCESS_KEY_ID: str = "test"
    AWS_SECRET_ACCESS_KEY: str = "test"

    S3_BUCKET_NAME: str = "novacrux-dev"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


storage_settings = StorageSettings()
