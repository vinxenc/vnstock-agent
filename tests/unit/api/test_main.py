"""Tests for the main API module with AG-UI protocol."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic_ai import Agent, UsageLimits
from pydantic_ai.models.test import TestModel

from api.main import app


def _fake_agent() -> Agent:
    """An agent backed by TestModel (runs locally, counts usage, supports streaming).

    Safe under the unit-test fixture that blocks real model requests.
    """
    return Agent(model=TestModel())


def _ag_ui_request() -> dict:
    return {
        "threadId": "test-1",
        "runId": "run-1",
        "state": {},
        "messages": [{"role": "user", "content": "Hello", "id": "msg-1"}],
        "tools": [],
        "context": [],
        "forwardedProps": {},
    }


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

    response = client.post("/", json=_ag_ui_request())
    # Should not return 405 Method Not Allowed or 404
    assert response.status_code not in [404, 405]


def test_low_request_limit_surfaces_usage_limit_exceeded(monkeypatch) -> None:
    """A very low request_limit must surface UsageLimitExceeded cleanly."""
    monkeypatch.setattr("api.main.AGENT", _fake_agent())
    monkeypatch.setattr("api.main.RUN_LIMITS", UsageLimits(request_limit=0))

    client = TestClient(app)
    response = client.post("/", json=_ag_ui_request())

    # Either the adapter's RUN_ERROR stream (200) or the handler's 429 guard.
    assert response.status_code in (200, 429)
    assert "request_limit" in response.text


def test_low_total_tokens_limit_surfaces_usage_limit_exceeded(monkeypatch) -> None:
    """A very low total_tokens_limit must surface UsageLimitExceeded cleanly."""
    monkeypatch.setattr("api.main.AGENT", _fake_agent())
    monkeypatch.setattr("api.main.RUN_LIMITS", UsageLimits(total_tokens_limit=1))

    client = TestClient(app)
    response = client.post("/", json=_ag_ui_request())

    assert response.status_code in (200, 429)
    assert "total_tokens_limit" in response.text
