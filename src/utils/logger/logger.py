"""Logger factory module implementing factory pattern with match-case."""

from config.settings import settings

from .interface import ILogger
from .logxide_adapter import LogxideAdapter


def get_logger(name: str) -> ILogger:
    """Return a logger instance based on LOGGER_TYPE env var.

    Args:
        name: Logger name (typically __name__ of the module).

    Returns:
        An ILogger instance.

    Factory logic (match-case style):
        - "logxide" (default): Returns LogxideAdapter
        - Future types can be added here (e.g., "logging", "loguru")
    """
    logger_type = settings.logger_type.lower()

    match logger_type:
        case "logxide":
            return LogxideAdapter(name)
        # Example for future extension:
        # case "logging":
        #     from .standard_logging_adapter import StandardLoggingAdapter
        #     return StandardLoggingAdapter(name)
        case _:
            # Default fallback to logxide
            return LogxideAdapter(name)
