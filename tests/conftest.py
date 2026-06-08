"""Shared pytest fixtures."""

from collections.abc import Generator

import pytest
from pydantic_ai import models


@pytest.fixture(autouse=True)
def block_real_model_requests() -> Generator[None]:
    """Prevent unit tests from accidentally calling configured model providers."""
    previous_value = models.ALLOW_MODEL_REQUESTS
    models.ALLOW_MODEL_REQUESTS = False
    yield
    models.ALLOW_MODEL_REQUESTS = previous_value
