"""Logger interface following the Interface Segregation Principle."""

from abc import ABC, abstractmethod


class ILogger(ABC):
    """Interface for logger implementations."""

    @abstractmethod
    def debug(self, msg: str, *args: object, **kwargs: object) -> None:
        """Log a debug message."""
        ...

    @abstractmethod
    def info(self, msg: str, *args: object, **kwargs: object) -> None:
        """Log an info message."""
        ...

    @abstractmethod
    def warning(self, msg: str, *args: object, **kwargs: object) -> None:
        """Log a warning message."""
        ...

    @abstractmethod
    def error(self, msg: str, *args: object, **kwargs: object) -> None:
        """Log an error message."""
        ...

    @abstractmethod
    def critical(self, msg: str, *args: object, **kwargs: object) -> None:
        """Log a critical message."""
        ...
