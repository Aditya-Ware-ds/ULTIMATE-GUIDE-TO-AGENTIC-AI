"""Lab 11.05: reference agent in CrewAI -- reference solution. See ../README.md."""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable

from crewai import Agent, Crew, Task
from crewai.tools import tool

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


@tool("calculate")
def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression."""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc}") from exc
    return _eval_node(tree.body)


def build_crew(llm, question: str) -> Crew:
    agent = Agent(
        role="Calculator",
        goal="Answer math questions",
        backstory="You use the calculate tool.",
        tools=[calculate],
        llm=llm,
    )
    task = Task(
        description=question,
        expected_output="The numeric answer to the question.",
        agent=agent,
    )
    return Crew(agents=[agent], tasks=[task])


def run_agent(question: str, llm) -> str:
    crew = build_crew(llm, question)
    result = crew.kickoff()
    return str(result)
