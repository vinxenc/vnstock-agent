"""Core agent implementation using PydanticAI with configurable provider."""

from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName, Model

from llm.factory import LLMFactory

SYSTEM_PROMPT = "You are a helpful assistant for the Vietnamese stock market (VNX). Always answer in English"


def create_agent(model: Model | KnownModelName | str) -> Agent:
    """Create the vnstock agent with an injectable model for tests."""
    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
    )


vnstock_agent = create_agent(LLMFactory.get_model())
