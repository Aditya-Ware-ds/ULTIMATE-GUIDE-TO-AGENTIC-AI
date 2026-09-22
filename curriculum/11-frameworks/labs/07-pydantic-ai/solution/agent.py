"""Lab 11.07: reference agent in Pydantic AI -- reference solution.
See ../README.md.
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

from pydantic_ai import Agent

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


AGENT = Agent(system_prompt="Use the calculate tool to answer math questions.")
AGENT.tool_plain(calculate)


def run_agent(question: str, model) -> str:
    result = AGENT.run_sync(question, model=model)
    return result.output
