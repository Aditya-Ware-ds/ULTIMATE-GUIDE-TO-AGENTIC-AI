"""Lab 11.08: reference agent in smolagents. See ../README.md for the full spec.

Requires `smolagents` installed (not in the default install -- see
../README.md). Fill in the pieces below.
"""

from __future__ import annotations

import ast  # noqa: F401 -- used once you implement calculate below

from smolagents import ToolCallingAgent, tool


@tool
def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression.

    Args:
        expression: The arithmetic expression to evaluate.
    """
    raise NotImplementedError


def build_agent(model) -> ToolCallingAgent:
    """TODO: implement this. Return ToolCallingAgent(tools=[calculate], model=model)."""
    raise NotImplementedError


def run_agent(question: str, model) -> str:
    """TODO: implement this. Build the agent and call .run(question)."""
    raise NotImplementedError
