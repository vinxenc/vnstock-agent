"""AG-UI integration example - FastAPI server with AG-UI protocol."""

from fastapi import FastAPI, Request, Response
from pydantic_ai.ui.ag_ui import AGUIAdapter

from agent.core.agent import vnstock_agent

app = FastAPI()


@app.post("/")
async def run_agent(request: Request) -> Response:
    """Handle AG-UI protocol request and stream response."""
    return await AGUIAdapter.dispatch_request(request, agent=vnstock_agent)
