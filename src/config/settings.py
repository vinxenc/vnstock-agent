"""Application settings loaded from environment variables and .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "vnstock-agent"
    debug: bool = False
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_model: str = "gpt-oss:120b-cloud"
    provider: str = "ollama"
    market_data_provider: str = "vnstock"
    vnstock_source: str = "VCI"
    log_level: str = "INFO"
    logger_type: str = "logxide"


settings = Settings()
