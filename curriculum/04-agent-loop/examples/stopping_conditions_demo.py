"""Run: uv run python curriculum/04-agent-loop/examples/stopping_conditions_demo.py

Shows an agent loop hitting a max-steps limit and returning a clear message
instead of raising or looping forever. See lessons/02-stopping-conditions.md.
"""

from __future__ import annotations

import asyncio

from shared.llm import Message, Role, get_client
from shared.llm.types import ToolDefinition, ToolResult

NOOP_TOOL = ToolDefinition(
    name="noop",
    description="Does nothing. Used to demonstrate a runaway tool-calling loop.",
    parameters={"type": "object", "properties": {}},
)


async def run_agent(client, user_input: str, max_steps: int) -> str:
    messages = [Message(role=Role.USER, content=user_input)]
    for _ in range(max_steps):
        response = await client.complete(messages, tools=[NOOP_TOOL])
        if not response.message.tool_calls:
            return response.message.content or ""
        messages.append(response.message)
        for call in response.message.tool_calls:
            messages.append(
                Message(role=Role.TOOL, tool_result=ToolResult(tool_call_id=call.id, content="ok"))
            )
    return f"Stopped after {max_steps} steps without reaching a final answer."


async def main() -> None:
    client = get_client("mock")
    for _ in range(10):  # a model that never stops calling the tool
        client.provider.add_tool_call("noop", {})

    result = await run_agent(client, "Do the thing forever.", max_steps=4)
    print(result)
    print(f"Model was called {client.provider.call_count} times (bounded by max_steps).")


if __name__ == "__main__":
    asyncio.run(main())
