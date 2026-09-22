"""Run: uv run python curriculum/12-multi-agent-systems/examples/supervisor_worker_demo.py

A supervisor routes a task to one of three specialized workers, then
synthesizes the worker's raw output into a final answer. See
lessons/01-topologies.md. No API key needed.
"""

from __future__ import annotations

import asyncio

from shared.llm import Message, Role, get_client


async def route_to_worker(client, task: str, worker_names: list[str]) -> str:
    response = await client.complete(
        [
            Message(
                role=Role.USER,
                content=f"Which worker should handle this task: {task!r}? "
                f"Choose exactly one of: {', '.join(worker_names)}. Reply with only the name.",
            )
        ]
    )
    return (response.message.content or "").strip()


async def synthesize(client, task: str, worker_result: str) -> str:
    response = await client.complete(
        [
            Message(
                role=Role.USER,
                content=f"Task: {task}\nWorker output: {worker_result}\n"
                "Write a final, polished answer for the user.",
            )
        ]
    )
    return response.message.content or ""


async def researcher(task: str) -> str:
    return f"[researcher] found 3 relevant facts about: {task}"


async def writer(task: str) -> str:
    return f"[writer] drafted a paragraph about: {task}"


async def critic(task: str) -> str:
    return f"[critic] reviewed and found no issues with: {task}"


async def supervisor(client, task: str, workers: dict[str, callable]) -> str:
    worker_name = await route_to_worker(client, task, list(workers.keys()))
    if worker_name not in workers:
        worker_name = next(iter(workers))  # fall back to the first worker
    worker_result = await workers[worker_name](task)
    return await synthesize(client, task, worker_result)


async def main() -> None:
    client = get_client("mock")
    workers = {"researcher": researcher, "writer": writer, "critic": critic}

    tasks = [
        "Find out how many moons Jupiter has.",
        "Write a tagline for a coffee shop.",
        "Check this sentence for grammar errors.",
    ]
    routes = ["researcher", "writer", "critic"]
    for route in routes:
        client.provider.add_text(route)
        client.provider.add_text(f"Final answer synthesized for: {route}")

    for task in tasks:
        result = await supervisor(client, task, workers)
        print(f"Task: {task}\n  -> {result}\n")


if __name__ == "__main__":
    asyncio.run(main())
