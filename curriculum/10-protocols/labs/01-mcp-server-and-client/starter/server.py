"""Lab 10.01: MCP server wrapping the calculator and weather tools.
See ../README.md for the full spec.
"""

from __future__ import annotations

import ast  # noqa: F401 -- used once you implement calculate below

from mcp.server import MCPServer

mcp = MCPServer("agentic-ai-mastery-tools")


@mcp.tool()
def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression and return the numeric result.

    TODO: implement this using the ast-based safe evaluator from Module 03
    (no eval()). Raise ValueError for anything that isn't valid arithmetic.
    """
    raise NotImplementedError


@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current weather for a city.

    TODO: implement this with a small hardcoded lookup table (at least
    "Paris" and "Tokyo"). Raise ValueError for an unknown city.
    """
    raise NotImplementedError


if __name__ == "__main__":
    mcp.run()
