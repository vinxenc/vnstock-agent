"""Tests for the vnstock agent configuration."""

from pydantic_ai import capture_run_messages
from pydantic_ai.models.test import TestModel

from agent.core.agent import SYSTEM_PROMPT, create_agent, vnstock_agent


async def test_create_agent_runs_with_injected_test_model() -> None:
    agent = create_agent(model=TestModel(custom_output_text="test answer"))

    result = await agent.run("What is VNM?")

    assert result.output == "test answer"


async def test_create_agent_includes_system_prompt() -> None:
    agent = create_agent(model=TestModel(custom_output_text="ok"))

    with capture_run_messages() as messages:
        await agent.run("Hello")

    assert any(getattr(part, "content", None) == SYSTEM_PROMPT for part in messages[0].parts)


def test_default_agent_is_created() -> None:
    assert vnstock_agent is not None
