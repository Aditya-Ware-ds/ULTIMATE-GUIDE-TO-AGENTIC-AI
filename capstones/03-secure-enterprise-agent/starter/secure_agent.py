"""Capstone 3: secure enterprise agent -- MCP tools, a human approval gate,
and checkpointed resume. See ../README.md, ../ARCHITECTURE.md, and
../THREAT_MODEL.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest capstones/03-secure-enterprise-agent/tests
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
    """Call mcp_client.call_tool(tool_call.name, tool_call.arguments) and
    wrap the result as a ToolResult:
      - if the call itself raises, return an is_error=True ToolResult with
        the exception text.
      - if result.is_error, return an is_error=True ToolResult using
        result.content[0].text as the message (this is what carries the
        MCP server's ToolError message -- see mcp_server.py).
      - otherwise, return a ToolResult whose content is
        result.structured_content["result"] if structured_content is
        truthy, else result.content[0].text.

    TODO: implement this.
    """
    raise NotImplementedError


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
    """Same loop shape as Module 09's approval-gate lab: call the model; if
    it gives a final answer (no tool calls), delete the checkpoint and
    return status="done". Otherwise take the first tool call: if its name
    is in REQUIRES_APPROVAL, save a checkpoint with pending_tool_call set
    and return status="paused" (do NOT call dispatch). Otherwise, call
    dispatch, append the ToolResult, advance step, save a checkpoint (no
    pending_tool_call), and loop. If max_steps is exhausted, return
    status="stopped".

    TODO: implement this.
    """
    raise NotImplementedError


async def run_agent_with_approval(
    client: LLMClient,
    mcp_client,
    checkpoint_path: Path,
    user_input: str,
    max_steps: int = 10,
) -> AgentResult:
    """Build the initial [system, user] messages and call _continue_loop.

    TODO: implement this.
    """
    raise NotImplementedError


async def resume_after_approval(
    client: LLMClient,
    mcp_client,
    checkpoint_path: Path,
    approved: bool,
    max_steps: int = 10,
) -> AgentResult:
    """Load the checkpoint (raise FileNotFoundError if none exists, raise
    ValueError if it has no pending_tool_call). If approved, dispatch the
    pending tool call for real; otherwise construct an is_error=True
    ToolResult saying the user did not approve. Append it, advance step,
    and continue via _continue_loop.

    TODO: implement this.
    """
    raise NotImplementedError
