"""Entry point for running the vnstock agent as an interactive CLI."""

from agent.core.agent import vnstock_agent


def main() -> None:
    """Launch PydanticAI's built-in interactive CLI (REPL) for the agent.

    Provides slash commands out of the box: /exit, /markdown, /multiline, /cp.
    """
    vnstock_agent.to_cli_sync(prog_name="vnstock-agent")


if __name__ == "__main__":
    main()
