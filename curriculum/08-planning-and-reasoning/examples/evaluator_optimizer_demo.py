"""Run: uv run python curriculum/08-planning-and-reasoning/examples/evaluator_optimizer_demo.py

Generates a draft, evaluates it, revises once, then gets approved. See
lessons/02-reflection-and-evaluator-optimizer.md. No API key needed.
"""

from __future__ import annotations

import asyncio
import json

from shared.llm import Message, Role, get_client


async def generate_draft(client, task: str, feedback: str | None) -> str:
    prompt = task if feedback is None else f"{task}\n\nPrevious feedback: {feedback}"
    response = await client.complete([Message(role=Role.USER, content=prompt)])
    return response.message.content or ""


async def evaluate_draft(client, task: str, draft: str) -> tuple[bool, str]:
    schema = {
        "type": "object",
        "properties": {"approved": {"type": "boolean"}, "feedback": {"type": "string"}},
        "required": ["approved", "feedback"],
    }
    response = await client.complete(
        [Message(role=Role.USER, content=f"Task: {task}\nDraft: {draft}")],
        response_schema=schema,
    )
    result = json.loads(response.message.content)
    return result["approved"], result["feedback"]


async def main() -> None:
    client = get_client("mock")
    client.provider.add_text("Our product is good.")
    client.provider.add_text(
        json.dumps({"approved": False, "feedback": "Too vague -- mention a specific benefit."})
    )
    client.provider.add_text("Our product saves you two hours a week on scheduling.")
    client.provider.add_text(json.dumps({"approved": True, "feedback": "Specific and concise."}))

    task = "Write a one-sentence product description."
    feedback = None
    for iteration in range(1, 4):
        draft = await generate_draft(client, task, feedback)
        approved, feedback = await evaluate_draft(client, task, draft)
        print(f"Iteration {iteration}: draft={draft!r} approved={approved} feedback={feedback!r}")
        if approved:
            print(f"\nFinal approved draft: {draft}")
            break


if __name__ == "__main__":
    asyncio.run(main())
