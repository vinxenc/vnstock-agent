"""Tests for the vnstock agent configuration."""

from datetime import datetime

from pydantic_ai import capture_run_messages
from pydantic_ai.models.test import TestModel

from agent.core.agent import SYSTEM_PROMPT, create_agent, vnstock_agent
from market_data.factory import MarketDataFactory
from market_data.models import StockPrice


async def test_create_agent_runs_with_injected_test_model() -> None:
    agent = create_agent(model=TestModel(custom_output_text="test answer", call_tools=[]))

    result = await agent.run("What is VNM?")

    assert result.output == "test answer"


async def test_create_agent_includes_system_prompt() -> None:
    agent = create_agent(model=TestModel(custom_output_text="ok", call_tools=[]))

    with capture_run_messages() as messages:
        await agent.run("Hello")

    assert any(getattr(part, "content", None) == SYSTEM_PROMPT for part in messages[0].parts)


async def test_agent_registers_market_data_tools(monkeypatch) -> None:
    called: list[str] = []

    class DummyProvider:
        def get_latest_price(self, symbol: str) -> StockPrice:
            called.append("get_latest_price")
            return StockPrice(symbol=symbol, price=1.0, time=datetime(2024, 1, 1), source="VCI")

        def get_history(self, symbol: str, start: str, end: str, interval: str) -> list:
            called.append("get_history")
            return []

    monkeypatch.setattr(MarketDataFactory, "create_provider", classmethod(lambda cls: DummyProvider()))

    agent = create_agent(model=TestModel())
    result = await agent.run("price of ACB?")

    assert result.output is not None
    assert set(called) == {"get_latest_price", "get_history"}


def test_default_agent_is_created() -> None:
    assert vnstock_agent is not None
