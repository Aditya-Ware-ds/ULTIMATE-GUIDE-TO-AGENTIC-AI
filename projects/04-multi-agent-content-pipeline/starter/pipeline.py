"""Project 04: multi-agent content pipeline. See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        projects/04-multi-agent-content-pipeline/tests
"""

from __future__ import annotations

import json  # noqa: F401 -- used once you implement research/critique below

from shared.llm import Message, Role  # noqa: F401 -- used below


async def research(client, topic: str) -> dict:
    """Ask the model for 3 short factual bullet points about `topic`.

    Request a structured response shaped either
    {"status": "success", "facts": [...]} or
    {"status": "error", "reason": "..."} (see lessons/02-failure-modes.md on
    workers reporting explicit status rather than the caller inferring it).

    TODO: implement this.
    """
    raise NotImplementedError


async def draft(client, topic: str, facts: list[str], feedback: str | None) -> str:
    """Write a short article about `topic` using `facts`. If `feedback` is not
    None, revise based on it (same shape as Module 08's evaluator-optimizer
    generate_draft).

    TODO: implement this.
    """
    raise NotImplementedError


async def critique(client, topic: str, article: str) -> tuple[bool, str]:
    """Request a structured {"approved": bool, "feedback": str} review of
    `article` (same shape as Module 08's evaluator-optimizer evaluate_draft).

    TODO: implement this.
    """
    raise NotImplementedError


async def run_pipeline(client, topic: str, max_revisions: int = 2) -> dict:
    """Run the full research -> draft -> critique(-> revise) pipeline.

    1. Call research(). If its status isn't "success", return
       {"status": "escalated", "reason": <research's reason>} immediately --
       do NOT call draft() or critique() (lessons/02-failure-modes.md).
    2. Call draft() with the research facts.
    3. Loop up to `max_revisions + 1` times: critique() the current draft;
       if approved, return {"status": "success", "article": ..., "revisions": <count>}.
       Otherwise, if revisions remain, call draft() again with the feedback.
    4. If never approved, return {"status": "escalated", "article": <last draft>,
       "reason": <a message mentioning the last feedback>}.

    TODO: implement this.
    """
    raise NotImplementedError
