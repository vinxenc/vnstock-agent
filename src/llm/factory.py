"""LLM provider factory implementing Factory pattern."""

from pydantic_ai.models import Model

from config.settings import settings
from llm.strategies.base import BaseLLMStrategy
from llm.strategies.ollama import OllamaStrategy
from utils.logger import get_logger

logger = get_logger(__name__)


class LLMFactory:
    """Factory class to create LLM provider strategies."""

    @classmethod
    def create_strategy(cls) -> BaseLLMStrategy:
        """Create and return an LLM strategy based on the configured provider.

        Returns:
            An instance of BaseLLMStrategy for the configured provider.

        Raises:
            ValueError: If the provider is not supported.
        """
        provider = settings.provider.lower()

        match provider:
            case "ollama":
                strategy = OllamaStrategy()
            case _:
                raise ValueError(f"Unknown provider: {settings.provider!r}. Supported providers: ['ollama']")

        logger.info(f"Creating strategy for provider: {provider}")
        return strategy

    @classmethod
    def get_model(cls) -> Model:
        """Convenience method to get a model from the configured provider.

        Returns:
            A PydanticAI model instance.
        """
        strategy = cls.create_strategy()
        return strategy.get_model()
