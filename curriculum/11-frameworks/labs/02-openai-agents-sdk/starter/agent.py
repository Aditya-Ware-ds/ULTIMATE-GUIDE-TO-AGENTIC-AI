"""Lab 11.02: reference agent in the OpenAI Agents SDK.
See ../README.md for the full spec.

Requires `openai-agents` installed (not in the default install -- see
../README.md). Fill in the pieces below.
"""

from __future__ import annotations

import ast  # noqa: F401 -- used once you implement calculate below

from agents import Agent, Runner, function_tool  # noqa: F401 -- Runner used in run_agent below


def _evaluate(expression: str) -> float:
    """The testable arithmetic logic (kept separate from the @function_tool
    wrapper below, since the SDK's tool-invocation path needs a real
    ToolContext and isn't meant to be called directly in tests).

    TODO: implement this using the ast-based safe evaluator from Module 03.
    """
    raise NotImplementedError


@function_tool
def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression.

    Args:
        expression: The arithmetic expression to evaluate.
    """
    return _evaluate(expression)


def build_agent(model) -> Agent:
    """TODO: implement this. Return an Agent with the calculate tool and this model."""
    raise NotImplementedError


async def run_agent(question: str, model) -> str:
    """TODO: implement this. await Runner.run(agent, question), return result.final_output."""
    raise NotImplementedError
