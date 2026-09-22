"""Lab 11.04: reference agent in Google ADK. See ../README.md for the full spec.

Requires `google-adk` installed (not in the default install -- see
../README.md). Fill in the pieces below.
"""

from __future__ import annotations

import ast  # noqa: F401 -- used once you implement calculate below

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner  # noqa: F401 -- used in run_agent below


def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression."""
    raise NotImplementedError


def build_agent(model) -> LlmAgent:
    """TODO: implement this. Return an LlmAgent with the calculate tool and this model."""
    raise NotImplementedError


async def run_agent(question: str, model) -> str:
    """TODO: implement this. Build the agent, run it via InMemoryRunner.run_debug,
    and return the last non-empty text part found across the returned events.
    """
    raise NotImplementedError
