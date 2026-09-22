"""Lab 08.01: plan-and-execute vs. evaluator-optimizer. See ../README.md for
the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/08-planning-and-reasoning/labs/01-plan-vs-evaluate/tests
"""

from __future__ import annotations

import json  # noqa: F401 -- used once you implement plan/evaluate_draft below

from shared.llm import LLMClient, Message, Role  # noqa: F401 -- used below


async def plan(client: LLMClient, task: str) -> list[str]:
    """Request a structured {"steps": [...]} response. Raise ValueError if empty.

    TODO: implement this (see lessons/01-plan-and-execute.md).
    """
    raise NotImplementedError


async def execute_step(client: LLMClient, step: str) -> str:
    """TODO: implement this."""
    raise NotImplementedError


async def plan_and_execute(client: LLMClient, task: str) -> str:
    """Call plan(), then execute_step() for each step, return the last result.

    TODO: implement this.
    """
    raise NotImplementedError


async def generate_draft(client: LLMClient, task: str, feedback: str | None) -> str:
    """TODO: implement this (see lessons/02-reflection-and-evaluator-optimizer.md)."""
    raise NotImplementedError


async def evaluate_draft(client: LLMClient, task: str, draft: str) -> tuple[bool, str]:
    """Request a structured {"approved": bool, "feedback": str} response.

    TODO: implement this.
    """
    raise NotImplementedError


async def evaluator_optimizer(client: LLMClient, task: str, max_iterations: int = 3) -> str:
    """Loop generate -> evaluate -> (return if approved, else regenerate with
    feedback). Return the last draft if never approved.

    TODO: implement this.
    """
    raise NotImplementedError
