"""Agent tools for fetching Vietnamese stock market data.

These functions are registered as PydanticAI agent tools; their docstrings are
surfaced to the model as the tool descriptions, so keep them clear and concrete.
They are synchronous on purpose: PydanticAI runs sync tools in a thread pool, so
the underlying provider's blocking network I/O does not stall the event loop.
"""

from market_data.factory import MarketDataFactory
from market_data.models import StockPrice, StockPriceHistory


def get_stock_price(symbol: str) -> StockPrice:
    """Get the latest market price for a Vietnamese stock symbol (e.g. 'ACB')."""
    provider = MarketDataFactory.create_provider()
    return provider.get_latest_price(symbol)


def get_stock_history(symbol: str, start: str, end: str, interval: str = "1D") -> list[StockPriceHistory]:
    """Get historical OHLCV bars for a Vietnamese stock symbol over a date range.

    Dates use ISO format 'YYYY-MM-DD'. ``interval`` defaults to daily ('1D').
    """
    provider = MarketDataFactory.create_provider()
    return provider.get_history(symbol, start, end, interval)
