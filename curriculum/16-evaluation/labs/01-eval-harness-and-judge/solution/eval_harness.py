"""Lab 16.01: a golden-dataset eval harness with an LLM-as-judge.
Reference solution. See ../README.md.
"""

from __future__ import annotations

import json
from collections.abc import Awaitable, Callable

from shared.llm import Message, Role

GOLDEN_DATASET = [
    {"question": "What is the capital of France?", "reference_answer": "Paris"},
    {"question": "What is 12 * 8?", "reference_answer": "96"},
    {"question": "What color do you get mixing blue and yellow?", "reference_answer": "Green"},
]


async def simple_agent(client, question: str) -> str:
    response = await client.complete([Message(role=Role.USER, content=question)])
    return response.message.content or ""


async def judge(client, question: str, reference_answer: str, candidate_answer: str) -> dict:
    schema = {
        "type": "object",
        "properties": {"correct": {"type": "boolean"}, "reasoning": {"type": "string"}},
        "required": ["correct", "reasoning"],
    }
    response = await client.complete(
        [
            Message(
                role=Role.USER,
                content=(
                    f"Question: {question}\nReference answer: {reference_answer}\n"
                    f"Candidate answer: {candidate_answer}\n"
                    "Does the candidate answer correctly address the question, "
                    "matching the reference answer's meaning (not necessarily its "
                    "exact wording)?"
                ),
            )
        ],
        response_schema=schema,
    )
    return json.loads(response.message.content)


async def evaluate_dataset(
    client,
    agent_fn: Callable[..., Awaitable[str]],
    dataset: list[dict],
) -> dict:
    results = []
    for item in dataset:
        answer = await agent_fn(client, item["question"])
        verdict = await judge(client, item["question"], item["reference_answer"], answer)
        results.append({"question": item["question"], "answer": answer, **verdict})

    correct = sum(1 for r in results if r["correct"])
    total = len(dataset)
    return {
        "total": total,
        "correct": correct,
        "accuracy": correct / total if total else 0.0,
        "results": results,
    }
