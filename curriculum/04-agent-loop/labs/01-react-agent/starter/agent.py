"""Lab 04.01: ReAct agent for multi-hop questions. See ../README.md for the
full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/04-agent-loop/labs/01-react-agent/tests
"""

from __future__ import annotations

import ast  # noqa: F401 -- used once you implement calculate() below
from collections.abc import Callable

from shared.llm import LLMClient, Message, Role  # noqa: F401 -- used in run_react_agent below
from shared.llm.types import ToolCall, ToolDefinition, ToolResult

# TODO: at least 4 entries forming a genuine 2-hop chain (lowercase keys).
KNOWLEDGE_BASE: dict[str, str] = {}


def search(query: str) -> str:
    """Look up `query.lower()` in KNOWLEDGE_BASE. Raise ValueError if not found.

    TODO: implement this.
    """
    raise NotImplementedError


def calculate(expression: str) -> float:
    """Safely evaluate a basic arithmetic expression. Do NOT use eval().

    TODO: implement this (a smaller copy of Module 03's ast-based evaluator is fine).
    """
    raise NotImplementedError


# TODO: define SEARCH_TOOL and CALCULATE_TOOL (ToolDefinition instances).
SEARCH_TOOL: ToolDefinition | None = None
CALCULATE_TOOL: ToolDefinition | None = None

# TODO: define TOOL_REGISTRY mapping "search" -> search, "calculate" -> calculate.
TOOL_REGISTRY: dict[str, Callable] = {}


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    """Execute a tool call against `registry`, never raising.

    TODO: implement this (same contract as Module 03's dispatch()).
    """
    raise NotImplementedError


async def run_react_agent(client: LLMClient, user_input: str, max_steps: int = 6) -> str:
    """Run a ReAct-style agent loop with the search and calculate tools.

    TODO: implement this. Use a system prompt instructing the model to reason
    briefly before each tool call and to give a final answer with no further
    tool calls once it has enough information. Loop up to max_steps times,
    dispatching tool calls and feeding results back, same shape as Module 03's
    run_tool_loop. Return a clear "stopped after N steps" message if max_steps
    is exhausted without a final answer.
    """
    raise NotImplementedError
