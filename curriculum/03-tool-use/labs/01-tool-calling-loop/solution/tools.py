"""Lab 03.01: calculator + weather tool-calling loop -- reference solution.
See ../README.md.
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

from shared.llm import LLMClient, Message, Role
from shared.llm.types import ToolCall, ToolDefinition, ToolResult

_BINOPS: dict[type, Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARYOPS: dict[type, Callable[[float], float]] = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
        return _BINOPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARYOPS:
        return _UNARYOPS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"Unsupported expression element: {ast.dump(node)}")


def calculate(expression: str) -> float:
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc}") from exc
    return _eval_node(tree.body)


_WEATHER_DATA = {
    "Paris": {"condition": "cloudy", "temp_c": 18},
    "Tokyo": {"condition": "sunny", "temp_c": 24},
}


def get_weather(city: str, unit: str = "celsius") -> dict:
    if city not in _WEATHER_DATA:
        raise ValueError(f"No weather data for city: {city!r}")
    data = _WEATHER_DATA[city]
    temp_c = data["temp_c"]
    temperature = temp_c if unit == "celsius" else temp_c * 9 / 5 + 32
    return {"city": city, "condition": data["condition"], "temperature": temperature, "unit": unit}


TOOL_DEFINITIONS: list[ToolDefinition] = [
    ToolDefinition(
        name="calculate",
        description="Evaluate a basic arithmetic expression and return the numeric result.",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "An arithmetic expression, e.g. '2 + 2 * 3'.",
                }
            },
            "required": ["expression"],
        },
    ),
    ToolDefinition(
        name="get_weather",
        description="Get the current weather for a city.",
        parameters={
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name, e.g. 'Paris'."},
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit. Defaults to celsius if omitted.",
                },
            },
            "required": ["city"],
        },
    ),
]

TOOL_REGISTRY: dict[str, Callable] = {
    "calculate": calculate,
    "get_weather": get_weather,
}


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


async def run_tool_loop(
    client: LLMClient,
    system_prompt: str,
    user_input: str,
    max_steps: int = 5,
) -> str:
    messages: list[Message] = [
        Message(role=Role.SYSTEM, content=system_prompt),
        Message(role=Role.USER, content=user_input),
    ]
    for _ in range(max_steps):
        response = await client.complete(messages, tools=TOOL_DEFINITIONS)
        if not response.message.tool_calls:
            return response.message.content or ""
        messages.append(response.message)
        for tool_call in response.message.tool_calls:
            result = dispatch(tool_call, TOOL_REGISTRY)
            messages.append(Message(role=Role.TOOL, tool_result=result))
    return f"Max steps ({max_steps}) reached without a final response."
