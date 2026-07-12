"""AG-UI integration example - FastAPI server with AG-UI protocol."""

from fastapi import FastAPI, Request, Response
from pydantic_ai.ui.ag_ui import AGUIAdapter

from agent.core.agent import vnstock_agent

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe: asserts the process is up and serving. Cheap and
    dependency-free by design — it does not check Ollama/vnstock, so a
    downstream outage never flaps the container unhealthy."""
    return {"status": "ok"}


@app.post("/")
async def run_agent(request: Request) -> Response:
    """Handle AG-UI protocol request and stream response."""
    return await AGUIAdapter.dispatch_request(request, agent=vnstock_agent)
