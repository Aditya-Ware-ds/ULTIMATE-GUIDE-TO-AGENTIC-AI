"""Lab 11.04: reference agent in Google ADK -- reference solution. See ../README.md."""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner

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
    """Evaluate a basic arithmetic expression."""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc}") from exc
    return _eval_node(tree.body)


def build_agent(model) -> LlmAgent:
    return LlmAgent(
        name="calc_agent",
        model=model,
        instruction="Use the calculate tool to answer math questions.",
        tools=[calculate],
    )


async def run_agent(question: str, model) -> str:
    agent = build_agent(model)
    runner = InMemoryRunner(agent=agent)
    events = await runner.run_debug(question, quiet=True)

    final_text = ""
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_text = part.text
    return final_text
