"""LLM provider factory implementing Factory pattern."""

from config.settings import settings
from llm.strategies.base import BaseLLMStrategy
from utils.logger import get_logger

logger = get_logger(__name__)


class LLMFactory:
    """Factory class to create LLM provider strategies."""

    _strategies = {
        "ollama": "llm.strategies.ollama.OllamaStrategy",
    }

    @classmethod
    def create_strategy(cls) -> BaseLLMStrategy:
        """Create and return an LLM strategy based on the configured provider.

        Returns:
            An instance of BaseLLMStrategy for the configured provider.

        Raises:
            ValueError: If the provider is not supported.
        """
        provider = settings.provider.lower()

        if provider not in cls._strategies:
            raise ValueError(
                f"Unknown provider: {settings.provider!r}. Supported providers: {list(cls._strategies.keys())}"
            )

        module_path, class_name = cls._strategies[provider].rsplit(".", 1)
        module = __import__(module_path, fromlist=[class_name])
        strategy_class = getattr(module, class_name)

        logger.info(f"Creating strategy for provider: {provider}")
        return strategy_class()

    @classmethod
    def get_model(cls):
        """Convenience method to get a model from the configured provider.

        Returns:
            A PydanticAI model instance.
        """
        strategy = cls.create_strategy()
        return strategy.get_model()
