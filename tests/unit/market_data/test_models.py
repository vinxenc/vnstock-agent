"""Tests for market data models."""

from datetime import date, datetime

import pytest

from market_data.models import StockPrice, StockPriceHistory


def test_stock_price_fields() -> None:
    price = StockPrice(symbol="ACB", price=10.5, time=datetime(2024, 1, 3), source="VCI")

    assert price.symbol == "ACB"
    assert price.price == pytest.approx(10.5)
    assert price.source == "VCI"


def test_stock_price_history_fields() -> None:
    bar = StockPriceHistory(time=date(2024, 1, 2), open=10.0, high=11.0, low=9.5, close=10.5, volume=1000)

    assert bar.close == pytest.approx(10.5)
    assert bar.volume == 1000
