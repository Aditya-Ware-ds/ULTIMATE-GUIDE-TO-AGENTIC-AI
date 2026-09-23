"""Lab 22.01: a multi-task agent that survives being killed and restarted
mid-plan via a durable progress file. See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/22-long-horizon-and-autonomous-agents/labs/01-progress-file-agent/tests
"""

from __future__ import annotations

import json  # noqa: F401 -- used once you implement load_progress/save_progress below
from pathlib import Path

from shared.llm import Message, Role  # noqa: F401 -- used once you implement run_task below


def load_progress(path: Path) -> list[dict] | None:
    """Return the "tasks" list from `path` (parsed as JSON), or None if
    `path` doesn't exist yet.

    TODO: implement this.
    """
    raise NotImplementedError


def save_progress(path: Path, tasks: list[dict]) -> None:
    """Write {"tasks": tasks} to `path` as JSON.

    TODO: implement this.
    """
    raise NotImplementedError


async def run_task(client, task_name: str) -> str:
    """Send `task_name` as a single user message and return the model's
    text response.

    TODO: implement this.
    """
    raise NotImplementedError


async def run_one_task_and_persist(
    client, progress_path: Path, tasks: list[dict], task_index: int
) -> list[dict]:
    """Run tasks[task_index] via run_task, set its "result" and mark its
    "status" as "done", call save_progress, and return tasks.

    TODO: implement this.
    """
    raise NotImplementedError


async def run_long_horizon_agent(client, progress_path: Path, task_names: list[str]) -> dict:
    """Load existing progress from progress_path, or initialize a fresh
    tasks list (every task "pending", result None) and save it if none
    exists yet. Then, for each task still "pending" (in order), call
    run_one_task_and_persist -- skip any task already "done" (from a
    previous run). Return {"tasks": tasks}.

    TODO: implement this.
    """
    raise NotImplementedError
