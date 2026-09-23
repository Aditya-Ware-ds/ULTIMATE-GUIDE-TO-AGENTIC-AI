"""Capstone 3: secure enterprise agent -- MCP tools, a human approval gate,
and checkpointed resume. Reference solution. See ../README.md,
../ARCHITECTURE.md, and ../THREAT_MODEL.md.

Extends Module 09's approval-gate pattern (message_to_dict/from_dict,
save/load_checkpoint, AgentResult, run_agent_with_approval/
resume_after_approval, all unchanged in shape) with a real MCP client as
the tool-execution transport (Module 10), instead of a local Python
function registry.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from shared.llm import LLMClient, Message, Role
from shared.llm.types import ToolCall, ToolDefinition, ToolResult

TOOLS: list[ToolDefinition] = [
    ToolDefinition(
        name="lookup_record",
        description="Look up an internal employee record by id.",
        parameters={
            "type": "object",
            "properties": {"record_id": {"type": "string"}},
            "required": ["record_id"],
        },
    ),
    ToolDefinition(
        name="send_announcement",
        description="Send an internal announcement to a channel.",
        parameters={
            "type": "object",
            "properties": {
                "channel": {"type": "string"},
                "message": {"type": "string"},
            },
            "required": ["channel", "message"],
        },
    ),
]

REQUIRES_APPROVAL: set[str] = {"send_announcement"}


async def dispatch(mcp_client, tool_call: ToolCall) -> ToolResult:
    try:
        result = await mcp_client.call_tool(tool_call.name, tool_call.arguments)
    except Exception as exc:
        return ToolResult(
            tool_call_id=tool_call.id, content=f"Tool execution failed: {exc}", is_error=True
        )
    if result.is_error:
        error_text = result.content[0].text if result.content else "unknown error"
        return ToolResult(tool_call_id=tool_call.id, content=error_text, is_error=True)
    content = (
        result.structured_content["result"]
        if result.structured_content
        else (result.content[0].text if result.content else "")
    )
    return ToolResult(tool_call_id=tool_call.id, content=str(content))


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


_SYSTEM_PROMPT = (
    "You are an internal enterprise assistant. You have lookup_record and "
    "send_announcement tools. When you have the answer, give a final "
    "response with no further tool calls."
)


async def _continue_loop(
    client: LLMClient,
    mcp_client,
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

        result = await dispatch(mcp_client, tool_call)
        messages.append(Message(role=Role.TOOL, tool_result=result))
        step += 1
        save_checkpoint(checkpoint_path, messages, step)

    return AgentResult(status="stopped", text=f"Stopped after {step} steps without a final answer.")


async def run_agent_with_approval(
    client: LLMClient,
    mcp_client,
    checkpoint_path: Path,
    user_input: str,
    max_steps: int = 10,
) -> AgentResult:
    messages: list[Message] = [
        Message(role=Role.SYSTEM, content=_SYSTEM_PROMPT),
        Message(role=Role.USER, content=user_input),
    ]
    return await _continue_loop(
        client, mcp_client, checkpoint_path, messages, step=0, max_steps=max_steps
    )


async def resume_after_approval(
    client: LLMClient,
    mcp_client,
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
        result = await dispatch(mcp_client, pending_tool_call)
    else:
        result = ToolResult(
            tool_call_id=pending_tool_call.id,
            content="The user did not approve this action.",
            is_error=True,
        )
    messages.append(Message(role=Role.TOOL, tool_result=result))
    step += 1
    return await _continue_loop(client, mcp_client, checkpoint_path, messages, step, max_steps)
