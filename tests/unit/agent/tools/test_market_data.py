"""Tests for the agent market data tools."""

from agent.tools.market_data import get_stock_history, get_stock_price
from market_data.factory import MarketDataFactory


def test_get_stock_price_delegates_to_provider(monkeypatch) -> None:
    expected = object()

    class DummyProvider:
        def get_latest_price(self, symbol: str) -> object:
            assert symbol == "ACB"
            return expected

    monkeypatch.setattr(MarketDataFactory, "create_provider", classmethod(lambda cls: DummyProvider()))

    assert get_stock_price("ACB") is expected


def test_get_stock_history_delegates_to_provider(monkeypatch) -> None:
    expected = [object()]

    class DummyProvider:
        def get_history(self, symbol: str, start: str, end: str, interval: str) -> object:
            assert (symbol, start, end, interval) == ("ACB", "2024-01-01", "2024-01-31", "1D")
            return expected

    monkeypatch.setattr(MarketDataFactory, "create_provider", classmethod(lambda cls: DummyProvider()))

    assert get_stock_history("ACB", "2024-01-01", "2024-01-31") is expected
