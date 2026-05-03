"""Logger interface following the Interface Segregation Principle."""

from abc import ABC, abstractmethod
from typing import Any


class ILogger(ABC):
    """Interface for logger implementations."""

    @abstractmethod
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        ...

    @abstractmethod
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message."""
        ...

    @abstractmethod
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message."""
        ...

    @abstractmethod
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message."""
        ...

    @abstractmethod
    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message."""
        ...
