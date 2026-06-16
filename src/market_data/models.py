"""Provider-agnostic market data models.

These domain models are the contract the agent and tools depend on, so swapping
the underlying data provider never leaks vendor-specific types (e.g. DataFrames).
"""

from datetime import date, datetime

from pydantic import BaseModel


class StockPrice(BaseModel):
    """Latest market price snapshot for a stock symbol."""

    symbol: str
    price: float
    time: datetime
    source: str


class StockPriceHistory(BaseModel):
    """A single historical open/high/low/close/volume bar."""

    time: date
    open: float
    high: float
    low: float
    close: float
    volume: int
