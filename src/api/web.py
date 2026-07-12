"""Basic web usage example - FastAPI server with Pydantic AI agent."""

from agent.core.agent import vnstock_agent

app = vnstock_agent.to_web()
