"""Application settings loaded from environment variables and .env file."""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "vnstock-agent"
    debug: bool = False
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_model: str = "gpt-oss:120b-cloud"
    provider: str = "ollama"
    market_data_provider: Literal["vnstock"] = "vnstock"
    vnstock_source: str = "VCI"
    vnstock_history_window_days: int = 30
    log_level: str = "INFO"
    logger_type: str = "logxide"

    # Bounded thread pool for blocking sync tool I/O offloaded by Pydantic AI.
    # Caps the number of worker threads so the server does not grow unbounded.
    thread_pool_max_workers: int = 16

    # Per-run usage limits forwarded to AGUIAdapter at request time.
    # total_tokens_limit is a run-wide budget (cumulative input+output tokens
    # across all model calls in a single run). Size it relative to the Ollama
    # per-request context window (num_ctx) times the expected tool round-trips.
    usage_request_limit: int = 5
    usage_tool_calls_limit: int = 8
    usage_total_tokens_limit: int = 20000


settings = Settings()
