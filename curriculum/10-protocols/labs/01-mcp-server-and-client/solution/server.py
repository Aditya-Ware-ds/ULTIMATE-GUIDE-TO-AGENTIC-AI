"""Lab 10.01: MCP server wrapping the calculator and weather tools.
Reference solution. See ../README.md.
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

from mcp.server import MCPServer

mcp = MCPServer("agentic-ai-mastery-tools")

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


@mcp.tool()
def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression and return the numeric result."""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc}") from exc
    return _eval_node(tree.body)


_WEATHER_DATA = {
    "Paris": "cloudy, 18C",
    "Tokyo": "sunny, 24C",
}


@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    if city not in _WEATHER_DATA:
        raise ValueError(f"No weather data for city: {city!r}")
    return _WEATHER_DATA[city]


if __name__ == "__main__":
    mcp.run()
