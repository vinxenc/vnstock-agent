"""AG-UI integration example - FastAPI server with AG-UI protocol."""

from collections.abc import AsyncIterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic_ai import Agent, UsageLimitExceeded, UsageLimits
from pydantic_ai.ui.ag_ui import AGUIAdapter

from agent.core.agent import vnstock_agent
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

# Per-run usage limits. These are read from settings/env so they can be tuned
# (e.g. total_tokens_limit against the deployed Ollama num_ctx) without code
# changes. They are passed to AGUIAdapter at run time, NOT the Agent constructor.
RUN_LIMITS = UsageLimits(
    request_limit=settings.usage_request_limit,
    tool_calls_limit=settings.usage_tool_calls_limit,
    total_tokens_limit=settings.usage_total_tokens_limit,
)

# Module-level agent handle so tests can swap in a fake agent without touching
# the production wiring (create_agent remains injectable by design).
AGENT = vnstock_agent


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Create a single bounded thread pool for the whole process lifetime.

    Pydantic AI offloads synchronous tools to anyio threads; binding a fixed
    pool prevents unbounded thread growth under sustained traffic. The pool is
    created exactly once here and torn down on shutdown with wait=True.
    """
    max_workers = settings.thread_pool_max_workers
    if max_workers < 1:
        msg = f"Invalid thread_pool_max_workers configuration: {max_workers!r}. Expected a positive integer (>= 1)."
        logger.error(msg)
        raise ValueError(msg)

    executor = ThreadPoolExecutor(max_workers=max_workers)
    logger.info(
        "Bounded thread executor created",
        extra={"max_workers": max_workers},
    )
    with Agent.using_thread_executor(executor):
        yield
    executor.shutdown(wait=True)
    logger.info("Bounded thread executor shut down")


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe: asserts the process is up and serving. Cheap and
    dependency-free by design — it does not check Ollama/vnstock, so a
    downstream outage never flaps the container unhealthy."""
    return {"status": "ok"}


@app.post("/")
async def run_agent(request: Request) -> Response:
    """Handle AG-UI protocol request and stream response."""
    try:
        return await AGUIAdapter.dispatch_request(request, agent=AGENT, usage_limits=RUN_LIMITS)
    except UsageLimitExceeded as exc:
        # The adapter normally surfaces this as a RUN_ERROR event in the stream;
        # this guard keeps a non-streaming edge case a clean 429, never a crash.
        logger.warning("Usage limit exceeded for run", extra={"detail": str(exc)})
        return JSONResponse(
            status_code=429,
            content={"error": "usage_limit_exceeded", "detail": str(exc)},
        )
