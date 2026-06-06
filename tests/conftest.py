"""Shared pytest fixtures."""

import pytest
from pydantic_ai import models


@pytest.fixture(autouse=True)
def block_real_model_requests() -> None:
    """Prevent unit tests from accidentally calling configured model providers."""
    previous_value = models.ALLOW_MODEL_REQUESTS
    models.ALLOW_MODEL_REQUESTS = False
    yield
    models.ALLOW_MODEL_REQUESTS = previous_value
