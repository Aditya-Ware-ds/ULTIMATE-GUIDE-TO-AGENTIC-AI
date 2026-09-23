"""Lab 22.01: a multi-task agent that survives being killed and restarted
mid-plan via a durable progress file. Reference solution. See ../README.md.
"""

from __future__ import annotations

import json
from pathlib import Path

from shared.llm import Message, Role


def load_progress(path: Path) -> list[dict] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text())["tasks"]


def save_progress(path: Path, tasks: list[dict]) -> None:
    path.write_text(json.dumps({"tasks": tasks}))


async def run_task(client, task_name: str) -> str:
    response = await client.complete([Message(role=Role.USER, content=task_name)])
    return response.message.content or ""


async def run_one_task_and_persist(
    client, progress_path: Path, tasks: list[dict], task_index: int
) -> list[dict]:
    task = tasks[task_index]
    task["result"] = await run_task(client, task["name"])
    task["status"] = "done"
    save_progress(progress_path, tasks)
    return tasks


async def run_long_horizon_agent(client, progress_path: Path, task_names: list[str]) -> dict:
    tasks = load_progress(progress_path)
    if tasks is None:
        tasks = [{"name": name, "status": "pending", "result": None} for name in task_names]
        save_progress(progress_path, tasks)

    for index, task in enumerate(tasks):
        if task["status"] == "done":
            continue
        tasks = await run_one_task_and_persist(client, progress_path, tasks, index)

    return {"tasks": tasks}
