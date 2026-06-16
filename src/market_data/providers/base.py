"""Base interface for market data providers."""

from abc import ABC, abstractmethod

from market_data.models import StockPrice, StockPriceHistory


class BaseMarketDataProvider(ABC):
    """Abstract base class for market data providers."""

    @abstractmethod
    def get_latest_price(self, symbol: str) -> StockPrice:
        """Return the latest market price for a stock symbol."""
        ...

    @abstractmethod
    def get_history(self, symbol: str, start: str, end: str, interval: str = "1D") -> list[StockPriceHistory]:
        """Return historical OHLCV bars for a symbol over a date range (ISO 'YYYY-MM-DD')."""
        ...
