"""Project 02: customer-support agent with escalation. See ../README.md for
the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest projects/02-customer-support-agent/tests
"""

from __future__ import annotations

import json  # noqa: F401 -- used once you implement save/load_checkpoint below
from collections.abc import Callable
from dataclasses import asdict, dataclass  # noqa: F401 -- used below
from pathlib import Path

from shared.llm import LLMClient, Message, Role  # noqa: F401 -- used below
from shared.llm.types import ToolCall, ToolDefinition, ToolResult

# TODO: at least 3 entries, e.g. "shipping", "returns", "account".
FAQ: dict[str, str] = {}


def search_faq(query: str) -> str:
    """Keyword-overlap match against FAQ values. Raise ValueError if no overlap.

    TODO: implement this.
    """
    raise NotImplementedError


_ISSUED_REFUNDS: list[dict] = []


def issue_refund(order_id: str, amount: float) -> str:
    """A gated (risky) tool.

    TODO: implement this. Append {"order_id": order_id, "amount": amount} to
    _ISSUED_REFUNDS, then return a confirmation string.
    """
    raise NotImplementedError


# TODO: define SEARCH_FAQ_TOOL, ISSUE_REFUND_TOOL, TOOL_REGISTRY, REQUIRES_APPROVAL.
SEARCH_FAQ_TOOL: ToolDefinition | None = None
ISSUE_REFUND_TOOL: ToolDefinition | None = None
TOOL_REGISTRY: dict[str, Callable] = {}
REQUIRES_APPROVAL: set[str] = set()


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    """TODO: implement this (same contract as prior modules)."""
    raise NotImplementedError


def message_to_dict(message: Message) -> dict:
    """TODO: implement this (see Modules 07/09)."""
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
    """TODO: implement this (see Module 09)."""
    raise NotImplementedError


def load_checkpoint(path: Path) -> tuple[list[Message], int, ToolCall | None] | None:
    """Return None if `path` doesn't exist.

    TODO: implement this.
    """
    raise NotImplementedError


def build_escalation_summary(messages: list[Message], reason: str) -> str:
    """Render every tool call + result in `messages` as a numbered list of
    attempted steps, followed by `reason`.

    TODO: implement this (see lessons/03-escalation-and-ux.md in Module 09).
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
    """TODO: implement this. Same shape as Module 09's _continue_loop, except
    on exhausting max_steps, return AgentResult(status="escalated",
    text=build_escalation_summary(messages, "hit the step limit without
    resolving the request")) instead of a generic stopped message, leaving
    the checkpoint in place.
    """
    raise NotImplementedError


async def run_support_agent(
    client: LLMClient,
    checkpoint_path: Path,
    user_input: str,
    max_steps: int = 5,
) -> AgentResult:
    """TODO: implement this. Build initial messages, step=0, call _continue_loop."""
    raise NotImplementedError


async def resume_after_approval(
    client: LLMClient,
    checkpoint_path: Path,
    approved: bool,
    max_steps: int = 5,
) -> AgentResult:
    """TODO: implement this (same contract as Module 09's lab)."""
    raise NotImplementedError
