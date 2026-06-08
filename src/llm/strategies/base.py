"""Base strategy interface for LLM providers."""

from abc import ABC, abstractmethod

from pydantic_ai.models import Model


class BaseLLMStrategy(ABC):
    """Abstract base class for LLM provider strategies."""

    @abstractmethod
    def get_model(self) -> Model:
        """Return a PydanticAI model instance for this provider."""
        ...
