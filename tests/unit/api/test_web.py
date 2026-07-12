"""Tests for the web API module."""

from fastapi.testclient import TestClient
from starlette.applications import Starlette

from api.web import app


def test_web_app_is_starlette_instance() -> None:
    """Verify that web.py exports a Starlette app (from to_web())."""
    assert isinstance(app, Starlette)


def test_web_app_has_routes() -> None:
    """Verify that the web app has registered routes."""
    client = TestClient(app)
    response = client.get("/")
    # to_web() serves HTML at root, should not 404
    assert response.status_code != 404
