"""Lab 09.01: agent with an approval gate. See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/09-human-in-the-loop/labs/01-approval-gate/tests
"""

from __future__ import annotations

import json  # noqa: F401 -- used once you implement save/load_checkpoint below
from collections.abc import Callable
from dataclasses import asdict, dataclass  # noqa: F401 -- used below
from pathlib import Path

from shared.llm import LLMClient, Message, Role  # noqa: F401 -- used below
from shared.llm.types import ToolCall, ToolDefinition, ToolResult


def get_weather(city: str) -> str:
    """A non-gated tool. TODO: implement (canned data is fine)."""
    raise NotImplementedError


_SENT_EMAILS: list[dict] = []


def send_email(to: str, subject: str) -> str:
    """A gated (risky) tool.

    TODO: implement this. Append {"to": to, "subject": subject} to
    _SENT_EMAILS (so tests can verify this real side effect happened, or
    didn't), then return a confirmation string.
    """
    raise NotImplementedError


# TODO: define TOOLS (list[ToolDefinition]) and TOOL_REGISTRY (dict[str, Callable])
# for both tools above.
TOOLS: list[ToolDefinition] = []
TOOL_REGISTRY: dict[str, Callable] = {}

# TODO: define REQUIRES_APPROVAL, a set of tool names requiring approval.
REQUIRES_APPROVAL: set[str] = set()


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    """TODO: implement this (same contract as prior modules)."""
    raise NotImplementedError


def message_to_dict(message: Message) -> dict:
    """TODO: implement this (see Module 07's lab)."""
    raise NotImplementedError


def message_from_dict(data: dict) -> Message:
    """TODO: implement this (inverse of message_to_dict)."""
    raise NotImplementedError


def save_checkpoint(
    path: Path,
    messages: list[Message],
    step: int,
    pending_tool_call: ToolCall | None = None,
) -> None:
    """TODO: implement this (extends Module 07's shape with pending_tool_call)."""
    raise NotImplementedError


def load_checkpoint(path: Path) -> tuple[list[Message], int, ToolCall | None] | None:
    """Return None if `path` doesn't exist.

    TODO: implement this.
    """
    raise NotImplementedError


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
    """Shared loop body used by both entry points below.

    TODO: implement this. While step < max_steps: call the model; if no tool
    calls, clean up the checkpoint and return AgentResult(status="done", ...);
    otherwise take the single tool call (per this lab's one-tool-call-per-turn
    simplification), append the assistant message, and either (a) if it
    requires approval, save a checkpoint with it as pending_tool_call and
    return AgentResult(status="paused", pending_tool_call=...) without
    dispatching, or (b) dispatch it immediately, append the result, increment
    step, checkpoint, and continue. If the loop exhausts max_steps, return
    AgentResult(status="stopped", text=...) leaving the checkpoint in place.
    """
    raise NotImplementedError


async def run_agent_with_approval(
    client: LLMClient,
    checkpoint_path: Path,
    system_prompt: str,
    user_input: str,
    max_steps: int = 10,
) -> AgentResult:
    """TODO: implement this. Build initial messages, step=0, call _continue_loop."""
    raise NotImplementedError


async def resume_after_approval(
    client: LLMClient,
    checkpoint_path: Path,
    approved: bool,
    max_steps: int = 10,
) -> AgentResult:
    """TODO: implement this. Load the checkpoint's pending_tool_call, dispatch
    it (if approved) or build a rejection ToolResult (if not), append it,
    increment step, then call _continue_loop.
    """
    raise NotImplementedError
