"""Tests for the LLM strategy factory."""

import pytest

from llm.factory import LLMFactory
from llm.strategies.ollama import OllamaStrategy


def test_create_strategy_returns_ollama_strategy(monkeypatch, mocker) -> None:
    monkeypatch.setattr("llm.factory.settings.provider", "OLLAMA")
    mocker.patch("llm.factory.logger.info")

    strategy = LLMFactory.create_strategy()

    assert isinstance(strategy, OllamaStrategy)


def test_create_strategy_rejects_unknown_provider(monkeypatch) -> None:
    monkeypatch.setattr("llm.factory.settings.provider", "missing")

    with pytest.raises(ValueError, match="Unknown provider"):
        LLMFactory.create_strategy()


def test_get_model_delegates_to_created_strategy(monkeypatch) -> None:
    expected_model = object()

    class DummyStrategy:
        def get_model(self):
            return expected_model

    monkeypatch.setattr(LLMFactory, "create_strategy", classmethod(lambda cls: DummyStrategy()))

    assert LLMFactory.get_model() is expected_model
