# Market Data Package

Swappable stock market data layer using the **Strategy pattern** and **Factory pattern**, so the
underlying data source (currently [vnstock](https://github.com/thinh-vu/vnstock)) can be replaced
without touching the agent or its tools.

## Design Pattern

- **`models.py`**: Provider-agnostic domain models (`StockPrice`, `StockPriceHistory`) — the contract every provider returns.
- **`providers/base.py`**: `BaseMarketDataProvider` abstract base class defining the provider interface.
- **`providers/vnstock.py`**: `VnstockProvider` implementing the interface on top of the `vnstock` library.
- **`factory.py`**: `MarketDataFactory.create_provider()` with `match-case` to select a provider from config.
- **`__init__.py`**: Exposes the clean public API (`MarketDataFactory`).

## Architecture

```
agent tools (get_stock_price / get_stock_history)   # src/agent/tools/market_data.py
        │
        ▼
MarketDataFactory.create_provider()                 # match-case on settings.market_data_provider
        │
        ▼
BaseMarketDataProvider (ABC)                         # get_latest_price / get_history
        │
        ▼
VnstockProvider  ──►  StockPrice / StockPriceHistory # provider-agnostic models (never DataFrames)
```

The golden rule: **providers return domain models, never vendor types** (e.g. a pandas `DataFrame`).
Callers depend only on `StockPrice` / `StockPriceHistory`, so swapping providers cannot ripple outward.

## Models

Clean, provider-agnostic Pydantic models (`models.py`):

```python
class StockPrice(BaseModel):
    symbol: str       # e.g. "ACB"
    price: float      # latest close price
    time: datetime    # timestamp of the price
    source: str       # provider/source name, e.g. "VCI"


class StockPriceHistory(BaseModel):
    time: date        # bar date
    open: float
    high: float
    low: float
    close: float
    volume: int
```

## Usage

### Via the factory (provider-agnostic)

```python
from market_data import MarketDataFactory

provider = MarketDataFactory.create_provider()                  # picks provider from settings
price = provider.get_latest_price("ACB")                        # -> StockPrice
bars = provider.get_history("ACB", "2024-01-01", "2024-03-01")  # -> list[StockPriceHistory]
```

### Via the agent tools

The agent (`src/agent/core/agent.py`) registers two tools the LLM can call:

- `get_stock_price(symbol)` → latest `StockPrice`
- `get_stock_history(symbol, start, end, interval="1D")` → `list[StockPriceHistory]`

## Configuration

Controlled by environment variables in `.env`:

- `MARKET_DATA_PROVIDER`: active provider (default: `vnstock`)
  - Supported: `"vnstock"` (add more by extending `factory.py`)
- `VNSTOCK_SOURCE`: data source passed to vnstock (default: `VCI`, e.g. `VCI`, `TCBS`)
- `VNSTOCK_HISTORY_WINDOW_DAYS`: lookback window (in days) used by `get_latest_price` to find the most recent bar (default: `30`)

## Adding a New Provider

To replace or add to `vnstock` (e.g. a broker REST API):

1. **Create a provider** implementing `BaseMarketDataProvider`, mapping the source response into the shared models:

```python
# src/market_data/providers/ssi.py
from market_data.models import StockPrice, StockPriceHistory
from market_data.providers.base import BaseMarketDataProvider


class SSIProvider(BaseMarketDataProvider):
    def get_latest_price(self, symbol: str) -> StockPrice:
        ...  # call your source, map the response into a StockPrice

    def get_history(self, symbol: str, start: str, end: str, interval: str = "1D") -> list[StockPriceHistory]:
        ...  # map each bar into a StockPriceHistory
```

2. **Add a case to the factory** in `factory.py`:

```python
from market_data.providers.ssi import SSIProvider

match provider:
    case "vnstock":
        instance = VnstockProvider()
    case "ssi":
        instance = SSIProvider()
    case _:
        raise ValueError(...)
```

3. **Select it** in `.env`:

```
MARKET_DATA_PROVIDER=ssi
```

No changes are needed in the agent or its tools — they depend only on `BaseMarketDataProvider` and
the domain models.

## vnstock Dependency

`vnstock` is a regular dependency. The project targets stable **Python 3.14**, where vnstock and its
scientific stack (pandas/NumPy/Pillow) install cleanly, so `VnstockProvider` imports `Quote` from
vnstock at module level and `uv sync` installs it automatically. Because the import lives only in
`providers/vnstock.py` behind `BaseMarketDataProvider`, swapping providers keeps it fully isolated.

## File Structure

```
src/market_data/
├── README.md            # This file
├── __init__.py          # Public API: MarketDataFactory
├── factory.py           # Factory with match-case
├── models.py            # StockPrice, StockPriceHistory (provider-agnostic)
└── providers/
    ├── __init__.py
    ├── base.py          # BaseMarketDataProvider abstract base class
    └── vnstock.py       # VnstockProvider (vnstock-backed)
```

## Benefits

- **Swappable**: Replace the data source by implementing `BaseMarketDataProvider` and adding one factory case.
- **Isolated**: Vendor types never leak past the provider boundary.
- **Configurable**: Switch providers via `MARKET_DATA_PROVIDER`, no code change.
- **Testable**: Mock the provider or its `Quote` client in unit tests.
- **Consistent**: Mirrors the `llm/` strategy/factory layer.
```
