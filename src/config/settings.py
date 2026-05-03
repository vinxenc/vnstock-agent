"""Application settings loaded from environment variables and .env file."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "vnstock-agent"
    debug: bool = False
    ollama_base_url: str = "http://localhost:11434"
    log_level: str = "INFO"
    logger_type: str = "logxide"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
