"""Lab 11.01: reference agent in LangGraph -- reference solution. See ../README.md."""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

from langchain.agents import create_agent
from langchain_core.tools import tool

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


@tool
def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression."""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc}") from exc
    return _eval_node(tree.body)


def build_agent(model):
    return create_agent(
        model, tools=[calculate], system_prompt="Use the calculate tool to answer math questions."
    )


def run_agent(question: str, model) -> str:
    agent = build_agent(model)
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content
