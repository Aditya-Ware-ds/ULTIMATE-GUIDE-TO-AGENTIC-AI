"""Run: uv run python curriculum/09-human-in-the-loop/examples/approval_gate_demo.py

Shows a gated tool call being intercepted before dispatch, then dispatched
only after simulated approval. See lessons/01-approval-gates.md. No API key
needed.
"""

from __future__ import annotations

import asyncio

from shared.llm import Message, Role, get_client
from shared.llm.types import ToolDefinition, ToolResult

REQUIRES_APPROVAL = {"send_email"}

SEND_EMAIL = ToolDefinition(
    name="send_email",
    description="Send an email to a recipient.",
    parameters={
        "type": "object",
        "properties": {
            "to": {"type": "string"},
            "subject": {"type": "string"},
        },
        "required": ["to", "subject"],
    },
)


def send_email(to: str, subject: str) -> str:
    return f"Email sent to {to} with subject {subject!r}"


def render_for_human(tool_call) -> str:
    args = tool_call.arguments
    return f"This agent wants to send an email to {args['to']} with subject {args['subject']!r}."


async def main() -> None:
    client = get_client("mock")
    client.provider.add_tool_call("send_email", {"to": "jane@example.com", "subject": "Update"})
    client.provider.add_text("The email has been sent.")

    messages = [Message(role=Role.USER, content="Email Jane an update.")]
    response = await client.complete(messages, tools=[SEND_EMAIL])
    tool_call = response.message.tool_calls[0]

    if tool_call.name in REQUIRES_APPROVAL:
        print(f"[GATED] {render_for_human(tool_call)}")
        print("Simulating human approval: yes")
        result_text = send_email(**tool_call.arguments)
        print(f"Dispatched after approval: {result_text}")
    else:
        print("Not gated -- would dispatch immediately.")

    messages.append(response.message)
    messages.append(
        Message(
            role=Role.TOOL, tool_result=ToolResult(tool_call_id=tool_call.id, content=result_text)
        )
    )
    final = await client.complete(messages, tools=[SEND_EMAIL])
    print(f"Final: {final.message.content}")


if __name__ == "__main__":
    asyncio.run(main())
