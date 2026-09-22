"""Lab 08.01: plan-and-execute vs. evaluator-optimizer -- reference solution.
See ../README.md.

Comparison notes (see README.md's "Comparing the two patterns"):

For "solve this arithmetic word problem," plan-and-execute is usually
preferable: it costs 1 + len(steps) calls (predictable, and the individual
steps -- "calculate 2+2" -- can run on a cheap model per Module 19's routing),
and the plan itself is an inspectable artifact for debugging ("here's exactly
what the model thought needed to happen"). Neither pattern inherently catches
wrong arithmetic on its own -- plan-and-execute's steps are executed by a
model call with no verification, and evaluator-optimizer's evaluator is just
another model call that could approve wrong arithmetic. Fixing that for
either pattern means the same thing: replace the arithmetic step/draft
generation with a real calculator tool call (Module 03) instead of trusting
the model to compute correctly, since arithmetic is exactly the kind of thing
that should never be delegated to free-text generation when a deterministic
tool is available. Evaluator-optimizer's advantage is its feedback history,
useful when the "quality" being checked is genuinely subjective (tone,
completeness) rather than mechanically verifiable -- which arithmetic isn't.
"""

from __future__ import annotations

import json

from shared.llm import LLMClient, Message, Role


async def plan(client: LLMClient, task: str) -> list[str]:
    schema = {
        "type": "object",
        "properties": {"steps": {"type": "array", "items": {"type": "string"}}},
        "required": ["steps"],
    }
    response = await client.complete(
        [Message(role=Role.USER, content=f"Break this task into steps: {task}")],
        response_schema=schema,
    )
    steps = json.loads(response.message.content or "{}")["steps"]
    if not steps:
        raise ValueError("Plan produced an empty steps list")
    return steps


async def execute_step(client: LLMClient, step: str) -> str:
    response = await client.complete([Message(role=Role.USER, content=step)])
    return response.message.content or ""


async def plan_and_execute(client: LLMClient, task: str) -> str:
    steps = await plan(client, task)
    result = ""
    for step in steps:
        result = await execute_step(client, step)
    return result


async def generate_draft(client: LLMClient, task: str, feedback: str | None) -> str:
    prompt = task if feedback is None else f"{task}\n\nPrevious feedback: {feedback}"
    response = await client.complete([Message(role=Role.USER, content=prompt)])
    return response.message.content or ""


async def evaluate_draft(client: LLMClient, task: str, draft: str) -> tuple[bool, str]:
    schema = {
        "type": "object",
        "properties": {"approved": {"type": "boolean"}, "feedback": {"type": "string"}},
        "required": ["approved", "feedback"],
    }
    response = await client.complete(
        [Message(role=Role.USER, content=f"Task: {task}\nDraft: {draft}")],
        response_schema=schema,
    )
    result = json.loads(response.message.content or "{}")
    return result["approved"], result["feedback"]


async def evaluator_optimizer(client: LLMClient, task: str, max_iterations: int = 3) -> str:
    feedback: str | None = None
    draft = ""
    for _ in range(max_iterations):
        draft = await generate_draft(client, task, feedback)
        approved, feedback = await evaluate_draft(client, task, draft)
        if approved:
            return draft
    return draft
