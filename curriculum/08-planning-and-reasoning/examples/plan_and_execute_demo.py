"""Run: uv run python curriculum/08-planning-and-reasoning/examples/plan_and_execute_demo.py

Generates a structured plan, then executes each step and synthesizes a final
answer. See lessons/01-plan-and-execute.md. No API key needed.
"""

from __future__ import annotations

import asyncio
import json

from shared.llm import Message, Role, get_client


async def plan(client, task: str) -> list[str]:
    schema = {
        "type": "object",
        "properties": {"steps": {"type": "array", "items": {"type": "string"}}},
        "required": ["steps"],
    }
    response = await client.complete(
        [Message(role=Role.USER, content=f"Break this task into steps: {task}")],
        response_schema=schema,
    )
    return json.loads(response.message.content)["steps"]


async def execute_step(client, step: str) -> str:
    response = await client.complete([Message(role=Role.USER, content=step)])
    return response.message.content or ""


async def main() -> None:
    client = get_client("mock")
    client.provider.add_text(
        json.dumps({"steps": ["Calculate 2 + 2", "Calculate 3 + 3", "State both results"]})
    )
    client.provider.add_text("4")
    client.provider.add_text("6")
    client.provider.add_text("2+2 is 4, and 3+3 is 6.")

    task = "Calculate 2+2 and 3+3, then state both results."
    steps = await plan(client, task)
    print(f"Plan: {steps}")

    results = []
    for step in steps:
        result = await execute_step(client, step)
        print(f"  executed {step!r} -> {result!r}")
        results.append(result)

    print(f"\nFinal (from the plan's own last step): {results[-1]}")


if __name__ == "__main__":
    asyncio.run(main())
