"""Lab 05.01: agent loop with compaction. See ../README.md for the full spec.

Fill in the four functions below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/05-context-engineering/labs/01-compacting-agent/tests
"""

from __future__ import annotations

from collections.abc import Callable

import tiktoken  # noqa: F401 -- used once you implement count_tokens below

from shared.llm import LLMClient, Message, Role  # noqa: F401 -- Role used in compact_messages below
from shared.llm.types import ToolCall, ToolDefinition, ToolResult


def count_tokens(messages: list[Message]) -> int:
    """Sum the tiktoken (o200k_base) token count of every message's content.

    TODO: implement this.
    """
    raise NotImplementedError


def compact_messages(
    messages: list[Message], max_tokens: int, keep_recent: int = 4
) -> list[Message]:
    """Keep system messages + the most recent `keep_recent` messages; replace
    everything else with one summary placeholder, only if over `max_tokens`.

    TODO: implement this (see lessons/02-compaction-and-summarization.md).
    """
    raise NotImplementedError


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    """Execute a tool call against `registry`, never raising.

    TODO: implement this (same contract as Modules 03-04).
    """
    raise NotImplementedError


async def run_agent_with_compaction(
    client: LLMClient,
    system_prompt: str,
    user_input: str,
    tools: list[ToolDefinition],
    registry: dict[str, Callable],
    max_context_tokens: int,
    max_steps: int = 20,
) -> str:
    """Run the agent loop, compacting `messages` before every model call.

    TODO: implement this. Same loop shape as Module 04's run_react_agent, but
    call compact_messages(messages, max_context_tokens) before each
    client.complete(...) call.
    """
    raise NotImplementedError
