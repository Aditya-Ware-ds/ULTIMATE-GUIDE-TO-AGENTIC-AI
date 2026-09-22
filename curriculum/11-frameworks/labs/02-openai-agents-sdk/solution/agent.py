"""Lab 11.02: reference agent in the OpenAI Agents SDK -- reference solution.
See ../README.md.
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

from agents import Agent, Runner, function_tool

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


def _evaluate(expression: str) -> float:
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc}") from exc
    return _eval_node(tree.body)


@function_tool
def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression.

    Args:
        expression: The arithmetic expression to evaluate.
    """
    return _evaluate(expression)


def build_agent(model) -> Agent:
    return Agent(
        name="calc_agent",
        instructions="Use the calculate tool to answer math questions.",
        tools=[calculate],
        model=model,
    )


async def run_agent(question: str, model) -> str:
    agent = build_agent(model)
    result = await Runner.run(agent, question)
    return result.final_output
