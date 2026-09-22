"""Lab 16.01: a golden-dataset eval harness with an LLM-as-judge.
See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/16-evaluation/labs/01-eval-harness-and-judge/tests
"""

from __future__ import annotations

import json  # noqa: F401 -- used once you implement judge below
from collections.abc import Awaitable, Callable

from shared.llm import Message, Role  # noqa: F401 -- used below

GOLDEN_DATASET = [
    {"question": "What is the capital of France?", "reference_answer": "Paris"},
    {"question": "What is 12 * 8?", "reference_answer": "96"},
    {"question": "What color do you get mixing blue and yellow?", "reference_answer": "Green"},
]


async def simple_agent(client, question: str) -> str:
    """Send `question` as a single user message and return the model's text
    response. This stands in for "the agent under test" -- any of this
    curriculum's earlier agents could be swapped in here.

    TODO: implement this.
    """
    raise NotImplementedError


async def judge(client, question: str, reference_answer: str, candidate_answer: str) -> dict:
    """Request a structured {"correct": bool, "reasoning": str} verdict on
    whether `candidate_answer` matches `reference_answer`'s meaning for
    `question` (see lessons/02-llm-as-judge.md).

    TODO: implement this.
    """
    raise NotImplementedError


async def evaluate_dataset(
    client,
    agent_fn: Callable[..., Awaitable[str]],
    dataset: list[dict],
) -> dict:
    """For each item in `dataset`: call agent_fn(client, item["question"]) to
    get an answer, then judge() it against item["reference_answer"]. Return
    {"total": ..., "correct": ..., "accuracy": ..., "results": [...]}
    where each result dict is {"question": ..., "answer": ..., "correct": ..., "reasoning": ...}.

    TODO: implement this.
    """
    raise NotImplementedError
