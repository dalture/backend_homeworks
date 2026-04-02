from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "task-service"
    app_version: str = "0.1.0"
    app_env: str = "dev"

    db_host: str
    db_port: str
    db_user: str
    db_pass: str
    db_name: str

    secret_key: str

    s3_bucket_name: str
    s3_endpoint_url: str
    s3_access_key: str
    s3_region: str
    s3_secret_key: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

DB_URL = f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}"