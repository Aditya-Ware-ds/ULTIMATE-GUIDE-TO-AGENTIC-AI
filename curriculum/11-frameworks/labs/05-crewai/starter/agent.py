"""Lab 11.05: reference agent in CrewAI. See ../README.md for the full spec.

Requires `crewai` installed (not in the default install -- see ../README.md).
Fill in the pieces below.
"""

from __future__ import annotations

import ast  # noqa: F401 -- used once you implement calculate below

from crewai import Agent, Crew, Task  # noqa: F401 -- Agent/Task used in build_crew below
from crewai.tools import tool


@tool("calculate")
def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression."""
    raise NotImplementedError


def build_crew(llm, question: str) -> Crew:
    """TODO: implement this (see ../README.md)."""
    raise NotImplementedError


def run_agent(question: str, llm) -> str:
    """TODO: implement this. Build the crew and call .kickoff(), return str(result)."""
    raise NotImplementedError
