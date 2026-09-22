"""Run: uv run python curriculum/04-agent-loop/examples/agent_loop_demo.py

A minimal observe-think-act loop over one tool, tracing each step. See
lessons/01-the-agent-loop.md. No API key needed.
"""

from __future__ import annotations

import asyncio

from shared.llm import Message, Role, get_client
from shared.llm.types import ToolDefinition

DOUBLE = ToolDefinition(
    name="double",
    description="Double a number.",
    parameters={
        "type": "object",
        "properties": {"n": {"type": "number"}},
        "required": ["n"],
    },
)


async def main() -> None:
    client = get_client("mock")
    client.provider.add_tool_call("double", {"n": 3})
    client.provider.add_tool_call("double", {"n": 6})
    client.provider.add_text("The final result is 12.")

    messages = [Message(role=Role.USER, content="Double 3, then double the result.")]

    for step in range(5):
        print(f"--- step {step + 1} ---")
        response = await client.complete(messages, tools=[DOUBLE])
        if not response.message.tool_calls:
            print(f"OBSERVE+THINK -> final answer: {response.message.content}")
            break
        messages.append(response.message)
        for call in response.message.tool_calls:
            print(f"THINK -> ACT: call {call.name}({call.arguments})")
            result = str(call.arguments["n"] * 2)
            print(f"OBSERVE: result = {result}")
            from shared.llm.types import ToolResult

            messages.append(
                Message(
                    role=Role.TOOL, tool_result=ToolResult(tool_call_id=call.id, content=result)
                )
            )


if __name__ == "__main__":
    asyncio.run(main())
