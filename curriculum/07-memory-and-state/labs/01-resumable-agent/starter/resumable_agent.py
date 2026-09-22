"""Lab 07.01: resumable agent (checkpoint & resume). See ../README.md for the
full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/07-memory-and-state/labs/01-resumable-agent/tests
"""

from __future__ import annotations

import json  # noqa: F401 -- used once you implement save/load_checkpoint below
from collections.abc import Callable
from dataclasses import asdict  # noqa: F401 -- used once you implement message_to_dict below
from pathlib import Path

from shared.llm import LLMClient, Message, Role  # noqa: F401 -- used below
from shared.llm.types import ToolCall, ToolDefinition, ToolResult


def message_to_dict(message: Message) -> dict:
    """TODO: implement this (see lessons/03-checkpointing-and-resumption.md)."""
    raise NotImplementedError


def message_from_dict(data: dict) -> Message:
    """TODO: implement this (inverse of message_to_dict)."""
    raise NotImplementedError


def save_checkpoint(path: Path, messages: list[Message], step: int) -> None:
    """TODO: implement this."""
    raise NotImplementedError


def load_checkpoint(path: Path) -> tuple[list[Message], int] | None:
    """Return None if `path` doesn't exist.

    TODO: implement this.
    """
    raise NotImplementedError


def build_initial_messages(system_prompt: str, user_input: str) -> list[Message]:
    """TODO: implement this."""
    raise NotImplementedError


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    """TODO: implement this (same contract as prior modules)."""
    raise NotImplementedError


async def run_one_step(
    client: LLMClient,
    messages: list[Message],
    tools: list[ToolDefinition],
    registry: dict[str, Callable],
) -> tuple[list[Message], str | None]:
    """Run exactly one loop iteration.

    TODO: implement this. Call the model. If the response has no tool calls,
    return (messages, answer_text). Otherwise, dispatch every tool call,
    append the assistant message and tool results to `messages`, and return
    (messages, None).
    """
    raise NotImplementedError


async def run_resumable_agent(
    client: LLMClient,
    tools: list[ToolDefinition],
    registry: dict[str, Callable],
    checkpoint_path: Path,
    system_prompt: str,
    user_input: str,
    max_steps: int = 10,
) -> str:
    """Resume from checkpoint_path if it exists, else start fresh. Checkpoint
    after every step. Delete the checkpoint on success; leave it in place if
    max_steps is exhausted.

    TODO: implement this.
    """
    raise NotImplementedError
