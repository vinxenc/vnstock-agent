# Logger Package

Simple swappable logging system using the **Adapter pattern** and **Factory pattern** for easy library replacement.

## Design Pattern

- **`interface.py`**: Defines `ILogger` abstract base class with standard logging methods
- **`logxide_adapter.py`**: Implements `ILogger` by wrapping the `logxide` library
- **`logger.py`**: Factory function `get_logger()` with `match-case` to switch adapters based on env var
- **`__init__.py`**: Exposes clean public API

## Usage

### Basic Usage
```python
from utils.logger import get_logger, ILogger

logger: ILogger = get_logger(__name__)
logger.info("Hello, world!")
logger.debug("Debug message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### Configuration
Logger settings are controlled via environment variables in `.env`:
- `LOGGER_TYPE`: Logger adapter type (default: `logxide`)
  - Supported: `"logxide"` (add more by extending `logger.py`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## Factory Pattern (match-case)

The `get_logger()` function uses Python's `match-case` to select the adapter:

```python
# In logger.py
match logger_type:
    case "logxide":
        return LogxideAdapter(name)
    case _:
        return LogxideAdapter(name)  # default fallback
```

## Swapping Logger Implementation

To replace `logxide` with another logging library:

1. **Create a new adapter** implementing `ILogger`:
```python
# src/utils/logger/my_adapter.py
from typing import Any
from .interface import ILogger

class MyLoggerAdapter(ILogger):
    def __init__(self, name: str) -> None:
        import my_log_lib
        self._logger = my_log_lib.getLogger(name)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.info(msg, *args, **kwargs)

    # ... implement other ILogger methods
```

2. **Add case to factory** in `logger.py`:
```python
from .my_adapter import MyLoggerAdapter

match logger_type:
    case "logxide":
        return LogxideAdapter(name)
    case "mylib":
        return MyLoggerAdapter(name)
    case _:
        return LogxideAdapter(name)
```

3. **Set env var** in `.env`:
```
LOGGER_TYPE=mylib
```

## LogxideAdapter Details

The `LogxideAdapter`:
- Calls `logxide.basicConfig()` once (via `_configured` flag)
- Configures default format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Wraps `logxide.getLogger()` to conform to `ILogger` interface

## File Structure

```
src/utils/logger/
├── README.md            # This file
├── __init__.py          # Public API: get_logger, ILogger, LogxideAdapter
├── interface.py         # ILogger abstract base class
├── logxide_adapter.py  # LogxideAdapter implementing ILogger
└── logger.py           # Factory with match-case
```

## Benefits

- **Simple**: Minimal code, no complex options
- **Swappable**: Replace logxide by implementing `ILogger` and updating the factory
- **SOLID compliant**: Adheres to Dependency Inversion Principle
- **Testable**: Mock `ILogger` interface in unit tests
- **Consistent**: Standard logging interface across the project
- **Pythonic**: Uses modern `match-case` syntax
