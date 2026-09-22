"""Lab 09.01: agent with an approval gate -- reference solution. See ../README.md."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path

from shared.llm import LLMClient, Message, Role
from shared.llm.types import ToolCall, ToolDefinition, ToolResult

_SENT_EMAILS: list[dict] = []  # module-level, used by tests to check the real side effect


def get_weather(city: str) -> str:
    return "sunny"


def send_email(to: str, subject: str) -> str:
    _SENT_EMAILS.append({"to": to, "subject": subject})
    return f"Email sent to {to} with subject {subject!r}"


TOOLS: list[ToolDefinition] = [
    ToolDefinition(
        name="get_weather",
        description="Get the current weather for a city.",
        parameters={
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    ),
    ToolDefinition(
        name="send_email",
        description="Send an email to a recipient.",
        parameters={
            "type": "object",
            "properties": {"to": {"type": "string"}, "subject": {"type": "string"}},
            "required": ["to", "subject"],
        },
    ),
]

TOOL_REGISTRY: dict[str, Callable] = {"get_weather": get_weather, "send_email": send_email}

REQUIRES_APPROVAL: set[str] = {"send_email"}


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    if tool_call.name not in registry:
        return ToolResult(
            tool_call_id=tool_call.id,
            content=f"Unknown tool: {tool_call.name}",
            is_error=True,
        )
    function = registry[tool_call.name]
    try:
        result = function(**tool_call.arguments)
        return ToolResult(tool_call_id=tool_call.id, content=str(result))
    except Exception as exc:
        return ToolResult(
            tool_call_id=tool_call.id, content=f"Tool execution failed: {exc}", is_error=True
        )


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


def save_checkpoint(
    path: Path,
    messages: list[Message],
    step: int,
    pending_tool_call: ToolCall | None = None,
) -> None:
    data = {
        "step": step,
        "messages": [message_to_dict(m) for m in messages],
        "pending_tool_call": asdict(pending_tool_call) if pending_tool_call else None,
    }
    path.write_text(json.dumps(data))


def load_checkpoint(path: Path) -> tuple[list[Message], int, ToolCall | None] | None:
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    messages = [message_from_dict(m) for m in data["messages"]]
    pending_tool_call = ToolCall(**data["pending_tool_call"]) if data["pending_tool_call"] else None
    return messages, data["step"], pending_tool_call


@dataclass
class AgentResult:
    status: str
    text: str | None = None
    pending_tool_call: ToolCall | None = None


async def _continue_loop(
    client: LLMClient,
    checkpoint_path: Path,
    messages: list[Message],
    step: int,
    max_steps: int,
) -> AgentResult:
    while step < max_steps:
        response = await client.complete(messages, tools=TOOLS)
        if not response.message.tool_calls:
            if checkpoint_path.exists():
                checkpoint_path.unlink()
            return AgentResult(status="done", text=response.message.content or "")

        tool_call = response.message.tool_calls[0]
        messages.append(response.message)

        if tool_call.name in REQUIRES_APPROVAL:
            save_checkpoint(checkpoint_path, messages, step, pending_tool_call=tool_call)
            return AgentResult(status="paused", pending_tool_call=tool_call)

        result = dispatch(tool_call, TOOL_REGISTRY)
        messages.append(Message(role=Role.TOOL, tool_result=result))
        step += 1
        save_checkpoint(checkpoint_path, messages, step)

    return AgentResult(status="stopped", text=f"Stopped after {step} steps without a final answer.")


async def run_agent_with_approval(
    client: LLMClient,
    checkpoint_path: Path,
    system_prompt: str,
    user_input: str,
    max_steps: int = 10,
) -> AgentResult:
    messages: list[Message] = [
        Message(role=Role.SYSTEM, content=system_prompt),
        Message(role=Role.USER, content=user_input),
    ]
    return await _continue_loop(client, checkpoint_path, messages, step=0, max_steps=max_steps)


async def resume_after_approval(
    client: LLMClient,
    checkpoint_path: Path,
    approved: bool,
    max_steps: int = 10,
) -> AgentResult:
    checkpoint = load_checkpoint(checkpoint_path)
    if checkpoint is None:
        raise FileNotFoundError(f"No checkpoint found at {checkpoint_path}")
    messages, step, pending_tool_call = checkpoint
    if pending_tool_call is None:
        raise ValueError("Checkpoint has no pending tool call to resume")

    if approved:
        result = dispatch(pending_tool_call, TOOL_REGISTRY)
    else:
        result = ToolResult(
            tool_call_id=pending_tool_call.id,
            content="The user did not approve this action.",
            is_error=True,
        )
    messages.append(Message(role=Role.TOOL, tool_result=result))
    step += 1
    return await _continue_loop(client, checkpoint_path, messages, step, max_steps)
