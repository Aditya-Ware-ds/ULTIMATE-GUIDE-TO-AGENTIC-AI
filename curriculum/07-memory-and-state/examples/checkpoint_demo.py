"""Run: uv run python curriculum/07-memory-and-state/examples/checkpoint_demo.py

Serializes a Message list (including a tool call) to JSON and back, proving
round-trip fidelity. See lessons/03-checkpointing-and-resumption.md.
"""

from __future__ import annotations

import json
import tempfile
from dataclasses import asdict
from pathlib import Path

from shared.llm.types import Message, Role, ToolCall, ToolResult


def message_to_dict(message: Message) -> dict:
    return {
        "role": message.role.value,
        "content": message.content,
        "tool_calls": [asdict(tc) for tc in message.tool_calls],
        "tool_result": asdict(message.tool_result) if message.tool_result else None,
    }


def message_from_dict(data: dict) -> Message:
    return Message(
        role=Role(data["role"]),
        content=data["content"],
        tool_calls=[ToolCall(**tc) for tc in data["tool_calls"]],
        tool_result=ToolResult(**data["tool_result"]) if data["tool_result"] else None,
    )


def main() -> None:
    messages = [
        Message(role=Role.SYSTEM, content="Be concise."),
        Message(role=Role.USER, content="What's the weather in Paris?"),
        Message(
            role=Role.ASSISTANT,
            tool_calls=[ToolCall(id="1", name="get_weather", arguments={"city": "Paris"})],
        ),
        Message(
            role=Role.TOOL,
            tool_result=ToolResult(tool_call_id="1", content="cloudy, 18C"),
        ),
    ]

    with tempfile.TemporaryDirectory() as tmp:
        checkpoint_path = Path(tmp) / "checkpoint.json"
        checkpoint_path.write_text(
            json.dumps({"step": 1, "messages": [message_to_dict(m) for m in messages]})
        )

        data = json.loads(checkpoint_path.read_text())
        restored = [message_from_dict(m) for m in data["messages"]]

        print(f"Saved and restored {len(restored)} messages, step={data['step']}")
        assert restored == messages
        print("Round-trip fidelity confirmed: restored messages == original messages")


if __name__ == "__main__":
    main()
