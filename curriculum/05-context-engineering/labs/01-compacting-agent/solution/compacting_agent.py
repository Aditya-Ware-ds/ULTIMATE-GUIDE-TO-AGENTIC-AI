"""Lab 05.01: agent loop with compaction -- reference solution. See ../README.md."""

from __future__ import annotations

from collections.abc import Callable

import tiktoken

from shared.llm import LLMClient, Message, Role
from shared.llm.types import ToolCall, ToolDefinition, ToolResult

_ENCODING = tiktoken.get_encoding("o200k_base")


def count_tokens(messages: list[Message]) -> int:
    return sum(len(_ENCODING.encode(m.content or "")) for m in messages)


def compact_messages(
    messages: list[Message], max_tokens: int, keep_recent: int = 4
) -> list[Message]:
    if count_tokens(messages) <= max_tokens:
        return messages

    system_messages = [m for m in messages if m.role == Role.SYSTEM]
    rest = [m for m in messages if m.role != Role.SYSTEM]

    if len(rest) <= keep_recent:
        return messages

    recent = rest[-keep_recent:]
    older = rest[:-keep_recent]

    summary = Message(
        role=Role.USER,
        content=f"[{len(older)} earlier messages omitted to stay within the context budget.]",
    )
    return [*system_messages, summary, *recent]


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


async def run_agent_with_compaction(
    client: LLMClient,
    system_prompt: str,
    user_input: str,
    tools: list[ToolDefinition],
    registry: dict[str, Callable],
    max_context_tokens: int,
    max_steps: int = 20,
) -> str:
    messages: list[Message] = [
        Message(role=Role.SYSTEM, content=system_prompt),
        Message(role=Role.USER, content=user_input),
    ]
    for _ in range(max_steps):
        messages = compact_messages(messages, max_context_tokens)
        response = await client.complete(messages, tools=tools)
        if not response.message.tool_calls:
            return response.message.content or ""
        messages.append(response.message)
        for tool_call in response.message.tool_calls:
            result = dispatch(tool_call, registry)
            messages.append(Message(role=Role.TOOL, tool_result=result))
    return f"Stopped after {max_steps} steps without reaching a final answer."
