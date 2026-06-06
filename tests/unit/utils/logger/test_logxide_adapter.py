"""Tests for the Logxide logger adapter."""

import pytest

from utils.logger import logxide_adapter
from utils.logger.logxide_adapter import LogxideAdapter


@pytest.fixture(autouse=True)
def reset_logxide_adapter() -> None:
    previous_value = LogxideAdapter._configured
    LogxideAdapter._configured = False
    yield
    LogxideAdapter._configured = previous_value


def test_logxide_adapter_configures_level_from_settings(monkeypatch, mocker) -> None:
    monkeypatch.setattr(logxide_adapter.settings, "log_level", "DEBUG")
    monkeypatch.setattr(logxide_adapter.logxide, "DEBUG", 10, raising=False)
    basic_config = mocker.patch.object(logxide_adapter.logxide, "basicConfig")
    wrapped_logger = mocker.Mock()
    get_logger = mocker.patch("utils.logger.logxide_adapter.getLogger", return_value=wrapped_logger)

    logger = LogxideAdapter("test.logger")

    basic_config.assert_called_once()
    assert basic_config.call_args.kwargs["level"] == 10
    assert "timestamp" in basic_config.call_args.kwargs["format"]
    get_logger.assert_called_once_with("test.logger")

    logger.info("hello")

    wrapped_logger.info.assert_called_once_with("hello")


def test_logxide_adapter_configures_basic_config_once(monkeypatch, mocker) -> None:
    monkeypatch.setattr(logxide_adapter.settings, "log_level", "INFO")
    basic_config = mocker.patch.object(logxide_adapter.logxide, "basicConfig")
    mocker.patch("utils.logger.logxide_adapter.getLogger")

    LogxideAdapter("first")
    LogxideAdapter("second")

    basic_config.assert_called_once()
