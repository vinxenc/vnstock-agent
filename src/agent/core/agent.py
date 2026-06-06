"""Core agent implementation using PydanticAI with configurable provider."""

from typing import Any

from pydantic_ai import Agent

from llm.factory import LLMFactory

SYSTEM_PROMPT = "You are a helpful assistant for the Vietnamese stock market (VNX). Alway anwser by English"


def create_agent(model: Any | None = None) -> Agent:
    """Create the vnstock agent with an injectable model for tests."""
    return Agent(
        model=model if model is not None else LLMFactory.get_model(),
        system_prompt=SYSTEM_PROMPT,
    )


vnstock_agent = create_agent()
