"""Lab 11.06: reference agent in Microsoft Agent Framework.
See ../README.md for the full spec.

Requires `agent-framework` installed (not in the default install -- see
../README.md). Fill in the pieces below.
"""

from __future__ import annotations

import ast  # noqa: F401 -- used once you implement calculate below

from agent_framework import Agent


def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression."""
    raise NotImplementedError


def build_agent(client) -> Agent:
    """TODO: implement this. Return an Agent with the calculate tool and this client."""
    raise NotImplementedError


async def run_agent(question: str, client) -> str:
    """TODO: implement this. Build the agent, await agent.run(question), return result.text."""
    raise NotImplementedError
