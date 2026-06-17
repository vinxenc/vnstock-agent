"""Market data provider factory implementing the Factory pattern."""

from config.settings import settings
from market_data.providers.base import BaseMarketDataProvider
from market_data.providers.vnstock import VnstockProvider
from utils.logger import get_logger

logger = get_logger(__name__)


class MarketDataFactory:
    """Factory class to create market data providers."""

    @classmethod
    def create_provider(cls) -> BaseMarketDataProvider:
        """Create and return a market data provider based on the configured provider.

        Returns:
            An instance of BaseMarketDataProvider for the configured provider.

        Raises:
            ValueError: If the provider is not supported.
        """
        provider = settings.market_data_provider.lower()

        match provider:
            case "vnstock":
                instance = VnstockProvider()
            case _:
                raise ValueError(
                    f"Unknown market data provider: {settings.market_data_provider!r}. Supported providers: ['vnstock']"
                )

        logger.info("Created market data provider: %s", provider)
        return instance
