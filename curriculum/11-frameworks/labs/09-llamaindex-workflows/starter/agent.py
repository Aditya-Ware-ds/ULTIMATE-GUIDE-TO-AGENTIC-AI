"""Lab 11.09: reference agent in LlamaIndex Workflows.
See ../README.md for the full spec.

Requires `llama-index-core` installed (not in the default install -- see
../README.md). Fill in the pieces below.
"""

from __future__ import annotations

import ast  # noqa: F401 -- used once you implement calculate below

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool


def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression.

    TODO: implement this (ast-based safe evaluator from Module 03).
    """
    raise NotImplementedError


# TODO: define CALCULATE_TOOL via FunctionTool.from_defaults(...).
CALCULATE_TOOL: FunctionTool | None = None


def build_agent(llm) -> FunctionAgent:
    """TODO: implement this. Return FunctionAgent(tools=[CALCULATE_TOOL], llm=llm)."""
    raise NotImplementedError


async def run_agent(question: str, llm) -> str:
    """TODO: implement this. Build the agent and await agent.run(question)."""
    raise NotImplementedError
