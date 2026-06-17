"""Tests for the vnstock market data provider."""

from datetime import date, datetime, timedelta

import pytest

from market_data.models import StockPrice, StockPriceHistory
from market_data.providers.vnstock import VnstockProvider, _to_date


class _FakeFrame:
    """Stand-in for a pandas DataFrame exposing only the seam the provider uses."""

    def __init__(self, records: list[dict]) -> None:
        self._records = records

    def to_dict(self, orient: str) -> list[dict]:
        assert orient == "records"
        return self._records


class _FakeQuote:
    last_init: dict = {}
    last_history: dict = {}

    def __init__(self, symbol: str, source: str) -> None:
        type(self).last_init = {"symbol": symbol, "source": source}

    def history(self, start: str, end: str, interval: str) -> _FakeFrame:
        type(self).last_history = {"start": start, "end": end, "interval": interval}
        return _FakeFrame(
            [
                {"time": datetime(2024, 1, 2), "open": 10.0, "high": 11.0, "low": 9.5, "close": 10.5, "volume": 1000},
                {"time": datetime(2024, 1, 3), "open": 10.5, "high": 12.0, "low": 10.0, "close": 11.5, "volume": 2000},
            ]
        )


def test_get_history_maps_frame_to_models(monkeypatch, mocker) -> None:
    monkeypatch.setattr("market_data.providers.vnstock.settings.vnstock_source", "VCI")
    mocker.patch("market_data.providers.vnstock.Quote", _FakeQuote)
    mocker.patch("market_data.providers.vnstock.logger.info")

    bars = VnstockProvider().get_history("ACB", "2024-01-01", "2024-01-31", interval="1D")

    assert _FakeQuote.last_init == {"symbol": "ACB", "source": "VCI"}
    assert _FakeQuote.last_history == {"start": "2024-01-01", "end": "2024-01-31", "interval": "1D"}
    assert bars == [
        StockPriceHistory(time=date(2024, 1, 2), open=10.0, high=11.0, low=9.5, close=10.5, volume=1000),
        StockPriceHistory(time=date(2024, 1, 3), open=10.5, high=12.0, low=10.0, close=11.5, volume=2000),
    ]


def test_get_latest_price_returns_most_recent_bar(monkeypatch, mocker) -> None:
    class _FrozenDate(date):
        @classmethod
        def today(cls) -> date:
            return cls(2024, 1, 3)

    monkeypatch.setattr("market_data.providers.vnstock.settings.vnstock_source", "VCI")
    monkeypatch.setattr("market_data.providers.vnstock.settings.vnstock_history_window_days", 30)
    monkeypatch.setattr("market_data.providers.vnstock.date", _FrozenDate)
    mocker.patch("market_data.providers.vnstock.Quote", _FakeQuote)
    mocker.patch("market_data.providers.vnstock.logger.info")

    price = VnstockProvider().get_latest_price("ACB")

    assert isinstance(price, StockPrice)
    assert price.symbol == "ACB"
    assert price.price == pytest.approx(11.5)
    assert price.source == "VCI"
    assert price.time == datetime(2024, 1, 3)
    assert _FakeQuote.last_history == {
        "start": (date(2024, 1, 3) - timedelta(days=30)).isoformat(),
        "end": "2024-01-03",
        "interval": "1D",
    }


def test_get_latest_price_raises_without_data(mocker) -> None:
    class _EmptyQuote:
        def __init__(self, symbol: str, source: str) -> None: ...

        def history(self, start: str, end: str, interval: str) -> _FakeFrame:
            return _FakeFrame([])

    mocker.patch("market_data.providers.vnstock.Quote", _EmptyQuote)
    mocker.patch("market_data.providers.vnstock.logger.info")

    with pytest.raises(ValueError, match="No price data"):
        VnstockProvider().get_latest_price("ZZZ")


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (datetime(2024, 5, 1, 9, 30), date(2024, 5, 1)),
        (date(2024, 5, 1), date(2024, 5, 1)),
        ("2024-05-01", date(2024, 5, 1)),
    ],
)
def test_to_date_normalises_inputs(value: object, expected: date) -> None:
    assert _to_date(value) == expected


def test_to_date_rejects_unparseable_value() -> None:
    with pytest.raises(ValueError):
        _to_date("not-a-date")
