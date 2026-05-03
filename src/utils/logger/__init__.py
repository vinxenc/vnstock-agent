"""Logger package with swappable implementations.

Usage:
    from utils.logger import get_logger, ILogger

    logger = get_logger(__name__)
    logger.info("Hello, world!")
    logger.debug("Debug message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
"""

from .interface import ILogger
from .logger import get_logger
from .logxide_adapter import LogxideAdapter

__all__ = ["get_logger", "ILogger", "LogxideAdapter"]
