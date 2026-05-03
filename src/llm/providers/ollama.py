"""Ollama provider."""

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

logger.info(f"Ollama base URL: {settings.ollama_base_url}")
