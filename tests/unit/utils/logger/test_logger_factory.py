"""Tests for the logger factory."""

from utils.logger import logger as logger_module


def test_get_logger_returns_logxide_adapter(monkeypatch, mocker) -> None:
    monkeypatch.setattr(logger_module.settings, "logger_type", "logxide")
    adapter = object()
    adapter_cls = mocker.patch("utils.logger.logger.LogxideAdapter", return_value=adapter)

    result = logger_module.get_logger("test")

    assert result is adapter
    adapter_cls.assert_called_once_with("test")


def test_get_logger_falls_back_to_logxide_adapter(monkeypatch, mocker) -> None:
    monkeypatch.setattr(logger_module.settings, "logger_type", "unknown")
    adapter = object()
    adapter_cls = mocker.patch("utils.logger.logger.LogxideAdapter", return_value=adapter)

    result = logger_module.get_logger("test")

    assert result is adapter
    adapter_cls.assert_called_once_with("test")
