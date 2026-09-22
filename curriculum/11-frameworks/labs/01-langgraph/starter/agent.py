"""Lab 11.01: reference agent in LangGraph (via langchain.agents.create_agent).
See ../README.md for the full spec.

Requires `langgraph` and `langchain` installed (not in the default install --
see ../README.md). Fill in the pieces below.
"""

from __future__ import annotations

import ast  # noqa: F401 -- used once you implement calculate below

from langchain.agents import create_agent  # noqa: F401 -- used in build_agent below
from langchain_core.tools import tool


@tool
def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression."""
    raise NotImplementedError


def build_agent(model):
    """TODO: implement this. Return create_agent(model, tools=[calculate], system_prompt=...)."""
    raise NotImplementedError


def run_agent(question: str, model) -> str:
    """TODO: implement this. Build the agent, invoke it, return the last message's content."""
    raise NotImplementedError
