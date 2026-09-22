"""Run: uv run python curriculum/09-human-in-the-loop/examples/rejection_demo.py

Shows a rejected action fed back to the model as a normal ToolResult(is_error=True),
letting the model react instead of crashing the loop. See
lessons/02-interrupt-and-resume.md. No API key needed.
"""

from __future__ import annotations

import asyncio

from shared.llm import Message, Role, get_client
from shared.llm.types import ToolDefinition, ToolResult

SEND_EMAIL = ToolDefinition(
    name="send_email",
    description="Send an email to a recipient.",
    parameters={
        "type": "object",
        "properties": {"to": {"type": "string"}, "subject": {"type": "string"}},
        "required": ["to", "subject"],
    },
)


async def main() -> None:
    client = get_client("mock")
    client.provider.add_tool_call("send_email", {"to": "jane@example.com", "subject": "Update"})
    client.provider.add_text(
        "Understood, I won't send that email. Let me know if you'd like changes."
    )

    messages = [Message(role=Role.USER, content="Email Jane an update.")]
    response = await client.complete(messages, tools=[SEND_EMAIL])
    tool_call = response.message.tool_calls[0]
    print(f"Model wants to call: {tool_call.name}({tool_call.arguments})")

    print("Simulating human rejection: no")
    rejection = ToolResult(
        tool_call_id=tool_call.id,
        content="The user did not approve this action.",
        is_error=True,
    )

    messages.append(response.message)
    messages.append(Message(role=Role.TOOL, tool_result=rejection))
    final = await client.complete(messages, tools=[SEND_EMAIL])
    print(f"Model's reaction to rejection: {final.message.content}")


if __name__ == "__main__":
    asyncio.run(main())
