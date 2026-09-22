"""Reference solution -- see ../README.md for the task description."""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from shared.llm import Message, Role

WorkerFn = Callable[[str], Awaitable[dict]]


async def researcher(task: str) -> dict:
    if "unanswerable" in task.lower():
        return {"status": "error", "output": "No reliable source found for this claim."}
    return {"status": "success", "output": f"Researched 3 supporting facts for: {task}"}


async def writer(task: str) -> dict:
    return {"status": "success", "output": f"Drafted a short paragraph about: {task}"}


async def critic(task: str) -> dict:
    return {"status": "success", "output": f"Reviewed and found no issues with: {task}"}


async def route_to_worker(client, task: str, worker_names: list[str]) -> str:
    response = await client.complete(
        [
            Message(
                role=Role.USER,
                content=(
                    f"Which worker should handle this task: {task!r}? "
                    f"Choose exactly one of: {', '.join(worker_names)}. "
                    "Reply with only the worker's name, nothing else."
                ),
            )
        ]
    )
    choice = (response.message.content or "").strip()
    if choice not in worker_names:
        raise ValueError(
            f"Model chose an unknown worker {choice!r}; expected one of {worker_names}"
        )
    return choice


async def synthesize(client, task: str, worker_output: str) -> str:
    response = await client.complete(
        [
            Message(
                role=Role.USER,
                content=(
                    f"Task: {task}\nWorker output: {worker_output}\n"
                    "Write a final, polished answer for the user."
                ),
            )
        ]
    )
    return response.message.content or ""


async def supervisor(client, task: str, workers: dict[str, WorkerFn]) -> dict:
    worker_name = await route_to_worker(client, task, list(workers.keys()))
    worker_result = await workers[worker_name](task)

    if worker_result["status"] != "success":
        # Explicit status check (lesson 02): never treat a failed worker as
        # done just because it produced *some* output. Escalate instead of
        # spending a synthesis call polishing a failure.
        return {
            "status": "escalated",
            "worker": worker_name,
            "reason": worker_result["output"],
        }

    final_answer = await synthesize(client, task, worker_result["output"])
    return {"status": "success", "worker": worker_name, "output": final_answer}
