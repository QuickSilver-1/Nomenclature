from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Order API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/postgres"
    LOG_LEVEL: str = "info"
    RATE_LIMIT_PER_MINUTE: int = 60
    ALLOWED_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()