"""Lab 11.03: reference agent in the Claude Agent SDK.
See ../README.md for the full spec, including why this framework can't be
fully tested offline.

Requires `claude-agent-sdk` installed (not in the default install -- see
../README.md). Fill in the pieces below.
"""

from __future__ import annotations

import ast  # noqa: F401 -- used once you implement _evaluate below

from claude_agent_sdk import (  # noqa: F401 -- create_sdk_mcp_server/query used below
    ClaudeAgentOptions,
    create_sdk_mcp_server,
    query,
    tool,
)


def _evaluate(expression: str) -> float:
    """The testable arithmetic logic.

    TODO: implement this using the ast-based safe evaluator from Module 03.
    """
    raise NotImplementedError


@tool("calculate", "Evaluate a basic arithmetic expression.", {"expression": str})
async def calculate(args: dict) -> dict:
    """TODO: implement this. Return
    {"content": [{"type": "text", "text": str(_evaluate(args["expression"]))}]}.
    """
    raise NotImplementedError


def build_options() -> ClaudeAgentOptions:
    """TODO: implement this (see ../README.md)."""
    raise NotImplementedError


async def run_agent(question: str) -> str:
    """TODO: implement this. Call query(prompt=question, options=build_options()),
    iterate the async generator, and return the final AssistantMessage's text
    (concatenate its TextBlock parts). Requires a real API key to actually run
    -- see the live-marked test.
    """
    raise NotImplementedError
