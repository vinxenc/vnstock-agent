"""Ollama provider strategy."""

from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from config.settings import settings
from llm.strategies.base import BaseLLMStrategy
from utils.logger import get_logger

logger = get_logger(__name__)


class OllamaStrategy(BaseLLMStrategy):
    """Strategy for Ollama provider."""

    def get_model(self) -> OllamaModel:
        """Return an OllamaModel instance."""
        provider = OllamaProvider(base_url=settings.ollama_base_url)
        logger.info(f"Using Ollama model: {settings.ollama_model}")

        return OllamaModel(settings.ollama_model, provider=provider)
