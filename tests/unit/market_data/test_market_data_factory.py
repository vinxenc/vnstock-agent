"""Tests for the market data provider factory."""

import pytest

from market_data.factory import MarketDataFactory
from market_data.providers.vnstock import VnstockProvider


def test_create_provider_returns_vnstock_provider(monkeypatch, mocker) -> None:
    monkeypatch.setattr("market_data.factory.settings.market_data_provider", "VNSTOCK")
    mocker.patch("market_data.factory.logger.info")

    provider = MarketDataFactory.create_provider()

    assert isinstance(provider, VnstockProvider)


def test_create_provider_rejects_unknown_provider(monkeypatch) -> None:
    monkeypatch.setattr("market_data.factory.settings.market_data_provider", "missing")

    with pytest.raises(ValueError, match="Unknown market data provider"):
        MarketDataFactory.create_provider()
