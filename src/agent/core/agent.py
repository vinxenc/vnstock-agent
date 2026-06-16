"""Core agent implementation using PydanticAI with configurable provider."""

from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName, Model

from agent.tools.market_data import get_stock_history, get_stock_price
from llm.factory import LLMFactory

SYSTEM_PROMPT = "You are a helpful assistant for the Vietnamese stock market (VNX). Always answer in English"


def create_agent(model: Model | KnownModelName | str) -> Agent:
    """Create the vnstock agent with an injectable model for tests."""
    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[get_stock_price, get_stock_history],
    )


vnstock_agent = create_agent(LLMFactory.get_model())
