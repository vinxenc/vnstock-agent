"""Tests for the Ollama LLM strategy."""

from llm.strategies.ollama import OllamaStrategy


def test_get_model_uses_ollama_settings(monkeypatch, mocker) -> None:
    monkeypatch.setattr("llm.strategies.ollama.settings.ollama_base_url", "http://ollama.test/v1")
    monkeypatch.setattr("llm.strategies.ollama.settings.ollama_model", "llama-test")

    provider = object()
    model = object()
    provider_cls = mocker.patch("llm.strategies.ollama.OllamaProvider", return_value=provider)
    model_cls = mocker.patch("llm.strategies.ollama.OllamaModel", return_value=model)
    mocker.patch("llm.strategies.ollama.logger.info")

    result = OllamaStrategy().get_model()

    assert result is model
    provider_cls.assert_called_once_with(base_url="http://ollama.test/v1")
    model_cls.assert_called_once_with("llama-test", provider=provider)
