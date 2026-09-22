"""Lab 03.01: calculator + weather tool-calling loop. See ../README.md for the
full spec.

Fill in the six pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/03-tool-use/labs/01-tool-calling-loop/tests
"""

from __future__ import annotations

import ast  # noqa: F401 -- used once you implement calculate() below
from collections.abc import Callable

from shared.llm import LLMClient, Message, Role  # noqa: F401 -- used in run_tool_loop below
from shared.llm.types import ToolCall, ToolDefinition, ToolResult


def calculate(expression: str) -> float:
    """Safely evaluate a basic arithmetic expression (+, -, *, /, parentheses).

    TODO: implement using ast.parse(expression, mode="eval") and a recursive
    walk that only allows BinOp (Add/Sub/Mult/Div), UnaryOp (USub/UAdd), and
    numeric Constant nodes. Do NOT use eval(). Raise ValueError for anything else.
    """
    raise NotImplementedError


def get_weather(city: str, unit: str = "celsius") -> dict:
    """Return canned weather data for a known city. Raise ValueError otherwise.

    TODO: implement using a small hardcoded lookup table with at least "Paris"
    and "Tokyo".
    """
    raise NotImplementedError


# TODO: define TOOL_DEFINITIONS, a list[ToolDefinition] with schemas for
# "calculate" and "get_weather" (see lessons/01-tool-schemas.md for the shape).
TOOL_DEFINITIONS: list[ToolDefinition] = []

# TODO: define TOOL_REGISTRY, mapping tool names to the functions above.
TOOL_REGISTRY: dict[str, Callable] = {}


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    """Execute a tool call against `registry`, never raising.

    TODO: implement this (see lessons/02-dispatch-and-execution.md).
    """
    raise NotImplementedError


async def run_tool_loop(
    client: LLMClient,
    system_prompt: str,
    user_input: str,
    max_steps: int = 5,
) -> str:
    """Run the model, dispatching tool calls, until it responds with plain text.

    TODO: implement this. Build the initial [system, user] messages, then loop
    up to max_steps times: call client.complete(messages, tools=TOOL_DEFINITIONS);
    if the response has no tool calls, return its text; otherwise append the
    assistant's tool-call message plus a Message(role=Role.TOOL, tool_result=...)
    per dispatched call, and continue. If max_steps is exhausted, return a clear
    message instead of raising.
    """
    raise NotImplementedError
