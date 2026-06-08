"""Entry point for running the vnstock agent interactively."""

import asyncio

from agent.core.agent import vnstock_agent
from utils.logger import get_logger

logger = get_logger(__name__)


async def main() -> None:
    """Run the agent interactively via stdin."""
    print("vnstock-agent (type 'exit' to quit)")
    print("-" * 40)

    while True:
        user_input = (await asyncio.to_thread(input, "\nYou: ")).strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        result = await vnstock_agent.run(user_input)
        print(f"\nAgent: {result.output}")


if __name__ == "__main__":
    asyncio.run(main())
