"""Lab 11.09: reference agent in LlamaIndex Workflows -- reference solution.
See ../README.md.
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool

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


CALCULATE_TOOL = FunctionTool.from_defaults(
    fn=calculate,
    name="calculate",
    description="Evaluate a basic arithmetic expression and return the numeric result.",
)


def build_agent(llm) -> FunctionAgent:
    return FunctionAgent(tools=[CALCULATE_TOOL], llm=llm)


async def run_agent(question: str, llm) -> str:
    agent = build_agent(llm)
    result = await agent.run(question)
    return str(result)
