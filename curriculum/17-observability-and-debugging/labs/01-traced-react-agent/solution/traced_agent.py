"""Lab 17.01: a fully instrumented ReAct agent, plus trace replay and a
usage summary. Reference solution. See ../README.md.
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

from shared.llm import Message, Role
from shared.llm.types import ToolCall, ToolDefinition, ToolResult
from shared.tracing import chat_span, execute_tool_span, invoke_agent_span

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
    messages: list[Message] = [
        Message(role=Role.SYSTEM, content=_SYSTEM_PROMPT),
        Message(role=Role.USER, content=user_input),
    ]
    provider_name = _infer_provider_name(client)
    with invoke_agent_span("react-agent", **{"gen_ai.request.max_steps": max_steps}):
        for _ in range(max_steps):
            with chat_span(model=client.default_model, provider=provider_name) as span:
                response = await client.complete(messages, tools=[CALCULATE_TOOL])
                span.set_attribute("gen_ai.usage.input_tokens", response.usage.input_tokens)
                span.set_attribute("gen_ai.usage.output_tokens", response.usage.output_tokens)
            if not response.message.tool_calls:
                return response.message.content or ""
            messages.append(response.message)
            for tool_call in response.message.tool_calls:
                with execute_tool_span(tool_call.name):
                    result = dispatch(tool_call, TOOL_REGISTRY)
                messages.append(Message(role=Role.TOOL, tool_result=result))
    return f"Stopped after {max_steps} steps without reaching a final answer."


def replay_trace(spans) -> str:
    spans_by_id = {s.context.span_id: s for s in spans}
    lines = []
    for span in sorted(spans, key=lambda s: s.start_time):
        depth = 0
        parent = span.parent
        while parent is not None:
            depth += 1
            parent_span = spans_by_id.get(parent.span_id)
            parent = parent_span.parent if parent_span else None
        duration_ms = (span.end_time - span.start_time) / 1_000_000
        attrs = ", ".join(f"{k}={v}" for k, v in span.attributes.items())
        lines.append(f"{'  ' * depth}{span.name} ({duration_ms:.1f}ms) [{attrs}]")
    return "\n".join(lines)


def summarize_usage(spans) -> dict:
    chat_spans = [s for s in spans if s.name.startswith("chat ")]
    return {
        "chat_calls": len(chat_spans),
        "input_tokens": sum(s.attributes.get("gen_ai.usage.input_tokens", 0) for s in chat_spans),
        "output_tokens": sum(s.attributes.get("gen_ai.usage.output_tokens", 0) for s in chat_spans),
    }
