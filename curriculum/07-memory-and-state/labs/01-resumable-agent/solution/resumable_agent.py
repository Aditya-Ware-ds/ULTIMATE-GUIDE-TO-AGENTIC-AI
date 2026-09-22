"""Lab 07.01: resumable agent (checkpoint & resume) -- reference solution.
See ../README.md.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict
from pathlib import Path

from shared.llm import LLMClient, Message, Role
from shared.llm.types import ToolCall, ToolDefinition, ToolResult


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


def save_checkpoint(path: Path, messages: list[Message], step: int) -> None:
    path.write_text(json.dumps({"step": step, "messages": [message_to_dict(m) for m in messages]}))


def load_checkpoint(path: Path) -> tuple[list[Message], int] | None:
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    return [message_from_dict(m) for m in data["messages"]], data["step"]


def build_initial_messages(system_prompt: str, user_input: str) -> list[Message]:
    return [
        Message(role=Role.SYSTEM, content=system_prompt),
        Message(role=Role.USER, content=user_input),
    ]


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


async def run_one_step(
    client: LLMClient,
    messages: list[Message],
    tools: list[ToolDefinition],
    registry: dict[str, Callable],
) -> tuple[list[Message], str | None]:
    response = await client.complete(messages, tools=tools)
    if not response.message.tool_calls:
        return messages, response.message.content or ""
    messages = [*messages, response.message]
    for tool_call in response.message.tool_calls:
        result = dispatch(tool_call, registry)
        messages.append(Message(role=Role.TOOL, tool_result=result))
    return messages, None


async def run_resumable_agent(
    client: LLMClient,
    tools: list[ToolDefinition],
    registry: dict[str, Callable],
    checkpoint_path: Path,
    system_prompt: str,
    user_input: str,
    max_steps: int = 10,
) -> str:
    checkpoint = load_checkpoint(checkpoint_path)
    if checkpoint is not None:
        messages, step = checkpoint
    else:
        messages = build_initial_messages(system_prompt, user_input)
        step = 0

    while step < max_steps:
        messages, answer = await run_one_step(client, messages, tools, registry)
        step += 1
        if answer is not None:
            if checkpoint_path.exists():
                checkpoint_path.unlink()
            return answer
        save_checkpoint(checkpoint_path, messages, step)

    return f"Stopped after {step} steps without reaching a final answer."
