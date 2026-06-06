"""Logxide adapter implementing the logger interface."""

from typing import Any

import logxide
from logxide import getLogger

from config.settings import settings

from .interface import ILogger


class LogxideAdapter(ILogger):
    """Adapter wrapping logxide to conform to ILogger interface."""

    _configured = False

    def __init__(self, name: str) -> None:
        if not LogxideAdapter._configured:
            json_format = (
                '{"timestamp":"%(asctime)s",'
                '"level":"%(levelname)s",'
                '"logger":"%(name)s",'
                '"thread":%(thread)d,'
                '"process":%(process)d,'
                '"message":"%(message)s"}'
            )
            level = getattr(logxide, settings.log_level.upper(), logxide.INFO)
            logxide.basicConfig(
                level=level,
                format=json_format,
                datefmt="%Y-%m-%d %H:%M:%S.%f",
            )
            LogxideAdapter._configured = True
        self._logger = getLogger(name)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.critical(msg, *args, **kwargs)
