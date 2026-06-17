"""vnstock market data provider."""

from datetime import date, datetime, timedelta

from vnstock import Quote

from config.settings import settings
from market_data.models import StockPrice, StockPriceHistory
from market_data.providers.base import BaseMarketDataProvider
from utils.logger import get_logger

logger = get_logger(__name__)


def _to_date(value: object) -> date:
    """Normalise a vnstock time value (Timestamp/datetime/date/str) to a date."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


class VnstockProvider(BaseMarketDataProvider):
    """Market data provider backed by the vnstock library."""

    def get_history(self, symbol: str, start: str, end: str, interval: str = "1D") -> list[StockPriceHistory]:
        """Return historical OHLCV bars from vnstock for a symbol."""
        source = settings.vnstock_source
        logger.info("Fetching vnstock history for %s (%s) from %s to %s", symbol, source, start, end)

        frame = Quote(symbol=symbol, source=source).history(start=start, end=end, interval=interval)

        return [
            StockPriceHistory(
                time=_to_date(row["time"]),
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=int(row["volume"]),
            )
            for row in frame.to_dict(orient="records")
        ]

    def get_latest_price(self, symbol: str) -> StockPrice:
        """Return the latest close price by reading a short recent history window."""
        end = date.today()
        start = end - timedelta(days=settings.vnstock_history_window_days)
        bars = self.get_history(symbol, start.isoformat(), end.isoformat())

        if not bars:
            raise ValueError(f"No price data available for symbol {symbol!r}.")

        latest = max(bars, key=lambda bar: bar.time)
        logger.info("Latest vnstock price for %s: %s", symbol, latest.close)

        return StockPrice(
            symbol=symbol,
            price=latest.close,
            time=datetime.combine(latest.time, datetime.min.time()),
            source=settings.vnstock_source,
        )
