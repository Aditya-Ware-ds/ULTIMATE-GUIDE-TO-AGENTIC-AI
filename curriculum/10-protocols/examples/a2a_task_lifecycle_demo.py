"""Run: uv run python curriculum/10-protocols/examples/a2a_task_lifecycle_demo.py

A simplified illustration of A2A's task lifecycle (submitted -> working ->
input-required -> completed), not the full A2A SDK/wire protocol. See
lessons/03-a2a-and-agent-skills.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class TaskState(StrEnum):
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input-required"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    state: TaskState = TaskState.SUBMITTED
    result: str | None = None


def start_work(task: Task, needs_input: bool) -> Task:
    task.state = TaskState.INPUT_REQUIRED if needs_input else TaskState.WORKING
    return task


def provide_input(task: Task) -> Task:
    if task.state != TaskState.INPUT_REQUIRED:
        raise ValueError(f"Task is not awaiting input (state={task.state})")
    task.state = TaskState.WORKING
    return task


def complete(task: Task, result: str) -> Task:
    task.state = TaskState.COMPLETED
    task.result = result
    return task


def main() -> None:
    task = Task(id="task-1")
    print(f"1. {task.state}")

    task = start_work(task, needs_input=True)
    print(f"2. {task.state} (the receiving agent needs clarification)")

    task = provide_input(task)
    print(f"3. {task.state} (client supplied the missing input)")

    task = complete(task, result="The requested report has been generated.")
    print(f"4. {task.state}: {task.result}")


if __name__ == "__main__":
    main()
