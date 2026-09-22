"""Lab 12.01: supervisor-worker. See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/12-multi-agent-systems/labs/01-supervisor-worker/tests
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from shared.llm import Message, Role  # noqa: F401 -- used once you implement the functions below

WorkerFn = Callable[[str], Awaitable[dict]]


# The three specialized workers are given to you -- they're the "tools" this
# lab's supervisor dispatches to, not what you're implementing.
async def researcher(task: str) -> dict:
    if "unanswerable" in task.lower():
        return {"status": "error", "output": "No reliable source found for this claim."}
    return {"status": "success", "output": f"Researched 3 supporting facts for: {task}"}


async def writer(task: str) -> dict:
    return {"status": "success", "output": f"Drafted a short paragraph about: {task}"}


async def critic(task: str) -> dict:
    return {"status": "success", "output": f"Reviewed and found no issues with: {task}"}


async def route_to_worker(client, task: str, worker_names: list[str]) -> str:
    """Ask the model which worker should handle `task`.

    Send one user message asking the model to choose exactly one name from
    `worker_names` and reply with only that name. Raise ValueError if the
    model's reply isn't one of `worker_names` -- never silently fall back to
    a default worker (see lessons/02-failure-modes.md).

    TODO: implement this.
    """
    raise NotImplementedError


async def synthesize(client, task: str, worker_output: str) -> str:
    """Ask the model to turn a worker's raw output into a final, polished answer.

    TODO: implement this.
    """
    raise NotImplementedError


async def supervisor(client, task: str, workers: dict[str, WorkerFn]) -> dict:
    """Route `task` to a worker, then synthesize -- unless the worker failed.

    1. Call route_to_worker to pick a worker name.
    2. Call that worker with `task`.
    3. If the worker's result status is not "success", do NOT call synthesize
       -- return {"status": "escalated", "worker": <name>, "reason": <worker's output>}
       instead (see lessons/02-failure-modes.md on trusting explicit status,
       not inferring success from mere output).
    4. If the worker succeeded, call synthesize on its output and return
       {"status": "success", "worker": <name>, "output": <synthesized text>}.

    TODO: implement this.
    """
    raise NotImplementedError
