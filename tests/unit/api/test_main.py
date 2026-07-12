"""Tests for the main API module with AG-UI protocol."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.main import app


def test_main_app_is_fastapi_instance() -> None:
    """Verify that main.py exports a FastAPI app."""
    assert isinstance(app, FastAPI)


def test_main_app_has_post_route() -> None:
    """Verify that the main app has a POST route at '/'."""
    routes = [route.path for route in app.routes]
    assert "/" in routes


def test_main_app_accepts_ag_ui_request() -> None:
    """Verify that the main app can handle AG-UI protocol requests."""
    client = TestClient(app)

    ag_ui_request = {
        "threadId": "test-1",
        "runId": "run-1",
        "state": {},
        "messages": [{"role": "user", "content": "Hello", "id": "msg-1"}],
        "tools": [],
        "context": [],
        "forwardedProps": {},
    }

    response = client.post("/", json=ag_ui_request)
    # Should not return 405 Method Not Allowed or 404
    assert response.status_code not in [404, 405]
