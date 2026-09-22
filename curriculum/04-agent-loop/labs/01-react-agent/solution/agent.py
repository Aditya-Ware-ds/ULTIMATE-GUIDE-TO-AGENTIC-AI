"""Lab 04.01: ReAct agent for multi-hop questions -- reference solution.
See ../README.md.
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

from shared.llm import LLMClient, Message, Role
from shared.llm.types import ToolCall, ToolDefinition, ToolResult

KNOWLEDGE_BASE: dict[str, str] = {
    "capital of france": "Paris",
    "population of paris": "2.1 million",
    "capital of japan": "Tokyo",
    "population of tokyo": "14 million",
}


def search(query: str) -> str:
    key = query.lower()
    if key not in KNOWLEDGE_BASE:
        raise ValueError(f"No information found for {query!r}")
    return KNOWLEDGE_BASE[key]


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


SEARCH_TOOL = ToolDefinition(
    name="search",
    description="Look up a fact, such as a capital city or a population.",
    parameters={
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
)

CALCULATE_TOOL = ToolDefinition(
    name="calculate",
    description="Evaluate a basic arithmetic expression.",
    parameters={
        "type": "object",
        "properties": {"expression": {"type": "string"}},
        "required": ["expression"],
    },
)

TOOL_REGISTRY: dict[str, Callable] = {"search": search, "calculate": calculate}


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    if tool_call.name not in registry:
        return ToolResult(
            tool_call_id=tool_call.id,
            content=f"Unknown tool: {tool_call.name}",
            is_error=True,
        )
    function = registry[tool_call.name]
    try:
        result = function(**tool_call.arguments)
        return ToolResult(tool_call_id=tool_call.id, content=str(result))
    except Exception as exc:
        return ToolResult(
            tool_call_id=tool_call.id, content=f"Tool execution failed: {exc}", is_error=True
        )


_SYSTEM_PROMPT = (
    "You answer multi-hop questions using the search and calculate tools. "
    "Before each tool call, briefly explain your reasoning in one sentence. "
    "When you have enough information, give a final answer with no further tool calls."
)


async def run_react_agent(client: LLMClient, user_input: str, max_steps: int = 6) -> str:
    messages: list[Message] = [
        Message(role=Role.SYSTEM, content=_SYSTEM_PROMPT),
        Message(role=Role.USER, content=user_input),
    ]
    for _ in range(max_steps):
        response = await client.complete(messages, tools=[SEARCH_TOOL, CALCULATE_TOOL])
        if not response.message.tool_calls:
            return response.message.content or ""
        messages.append(response.message)
        for tool_call in response.message.tool_calls:
            result = dispatch(tool_call, TOOL_REGISTRY)
            messages.append(Message(role=Role.TOOL, tool_result=result))
    return f"Stopped after {max_steps} steps without reaching a final answer."
