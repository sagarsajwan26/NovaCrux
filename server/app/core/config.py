from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    app_env: str = "development"

    tenant_base_domain: str = "ienergizerinfo.com"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
