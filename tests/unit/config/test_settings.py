"""Tests for application settings."""

import pytest
from pydantic import ValidationError

from config.settings import Settings


def test_settings_defaults_without_env_file(monkeypatch) -> None:
    for key in (
        "APP_NAME",
        "DEBUG",
        "OLLAMA_BASE_URL",
        "OLLAMA_MODEL",
        "PROVIDER",
        "MARKET_DATA_PROVIDER",
        "VNSTOCK_SOURCE",
        "VNSTOCK_HISTORY_WINDOW_DAYS",
        "LOG_LEVEL",
        "LOGGER_TYPE",
    ):
        monkeypatch.delenv(key, raising=False)

    settings = Settings(_env_file=None)

    assert settings.app_name == "vnstock-agent"
    assert settings.debug is False
    assert settings.ollama_base_url == "http://localhost:11434/v1"
    assert settings.ollama_model == "gpt-oss:120b-cloud"
    assert settings.provider == "ollama"
    assert settings.market_data_provider == "vnstock"
    assert settings.vnstock_source == "VCI"
    assert settings.vnstock_history_window_days == 30
    assert settings.log_level == "INFO"
    assert settings.logger_type == "logxide"


def test_settings_read_environment_overrides(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "test-agent")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://ollama.test/v1")
    monkeypatch.setenv("OLLAMA_MODEL", "llama-test")
    monkeypatch.setenv("PROVIDER", "custom")
    monkeypatch.setenv("VNSTOCK_SOURCE", "TCBS")
    monkeypatch.setenv("VNSTOCK_HISTORY_WINDOW_DAYS", "45")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("LOGGER_TYPE", "custom-logger")

    settings = Settings(_env_file=None)

    assert settings.app_name == "test-agent"
    assert settings.debug is True
    assert settings.ollama_base_url == "http://ollama.test/v1"
    assert settings.ollama_model == "llama-test"
    assert settings.provider == "custom"
    assert settings.vnstock_source == "TCBS"
    assert settings.vnstock_history_window_days == 45
    assert settings.log_level == "DEBUG"
    assert settings.logger_type == "custom-logger"


def test_settings_rejects_unknown_market_data_provider(monkeypatch) -> None:
    monkeypatch.setenv("MARKET_DATA_PROVIDER", "bogus")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
