"""Lab 11.07: reference agent in Pydantic AI. See ../README.md for the full spec.

Requires `pydantic-ai` installed (not in the default install -- see
../README.md). Fill in the pieces below.
"""

from __future__ import annotations

import ast  # noqa: F401 -- used once you implement calculate below

from pydantic_ai import Agent


# TODO: define calculate(expression: str) -> float using the ast-based safe
# evaluator from Module 03 (no eval()).
def calculate(expression: str) -> float:
    raise NotImplementedError


# TODO: define AGENT: Agent with a system prompt, and register calculate via
# @AGENT.tool_plain.
AGENT: Agent | None = None


def run_agent(question: str, model) -> str:
    """TODO: implement this. Call AGENT.run_sync(question, model=model).output."""
    raise NotImplementedError
