"""Lab 17.01: a fully instrumented ReAct agent, plus trace replay and a
usage summary. See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/17-observability-and-debugging/labs/01-traced-react-agent/tests
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

from shared.llm import Message, Role  # noqa: F401 -- used once you implement run_traced_agent below
from shared.llm.types import ToolCall, ToolDefinition, ToolResult
from shared.tracing import chat_span, execute_tool_span, invoke_agent_span  # noqa: F401

_BINOPS: dict[type, Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
        return _BINOPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    raise ValueError(f"Unsupported expression element: {ast.dump(node)}")


def calculate(expression: str) -> float:
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc}") from exc
    return _eval_node(tree.body)


CALCULATE_TOOL = ToolDefinition(
    name="calculate",
    description="Evaluate a basic arithmetic expression.",
    parameters={
        "type": "object",
        "properties": {"expression": {"type": "string"}},
        "required": ["expression"],
    },
)

TOOL_REGISTRY: dict[str, Callable] = {"calculate": calculate}


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    if tool_call.name not in registry:
        return ToolResult(
            tool_call_id=tool_call.id, content=f"Unknown tool: {tool_call.name}", is_error=True
        )
    function = registry[tool_call.name]
    try:
        result = function(**tool_call.arguments)
        return ToolResult(tool_call_id=tool_call.id, content=str(result))
    except Exception as exc:
        return ToolResult(
            tool_call_id=tool_call.id, content=f"Tool execution failed: {exc}", is_error=True
        )


def _infer_provider_name(client) -> str:
    name = type(client.provider).__name__
    return name.removesuffix("LLMProvider").removesuffix("Provider").lower() or "mock"


_SYSTEM_PROMPT = (
    "You answer arithmetic questions using the calculate tool. "
    "When you have the answer, give a final response with no further tool calls."
)


async def run_traced_agent(client, user_input: str, max_steps: int = 6) -> str:
    """Run Module 04's ReAct loop shape (calculate tool only), wrapped in
    tracing spans:
      - the whole run in
        invoke_agent_span("react-agent", **{"gen_ai.request.max_steps": max_steps})
      - each model call in
        chat_span(model=client.default_model, provider=_infer_provider_name(client)),
        recording gen_ai.usage.input_tokens/output_tokens on the span via
        span.set_attribute(...) once the response is known
      - each tool call in execute_tool_span(tool_call.name)

    TODO: implement this.
    """
    raise NotImplementedError


def replay_trace(spans) -> str:
    """Reconstruct a chronological, indented timeline from exported spans
    (see lessons/02-replaying-failed-runs.md): sort by start_time, indent by
    walking each span's parent chain, and print each span's name, duration
    in milliseconds, and attributes.

    TODO: implement this.
    """
    raise NotImplementedError


def summarize_usage(spans) -> dict:
    """Return {"chat_calls": ..., "input_tokens": ..., "output_tokens": ...}
    by summing the gen_ai.usage.* attributes across every span whose name
    starts with "chat ".

    TODO: implement this.
    """
    raise NotImplementedError
