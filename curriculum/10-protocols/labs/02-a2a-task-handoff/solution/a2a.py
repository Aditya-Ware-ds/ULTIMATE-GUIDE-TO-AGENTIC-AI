"""Lab 10.02: A2A-style task handoff -- reference solution. See ../README.md.

This is a simplified, illustrative version of A2A's task lifecycle concept --
not the full wire protocol/SDK.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum


class TaskState(StrEnum):
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input-required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


@dataclass
class Task:
    id: str
    state: TaskState = TaskState.SUBMITTED
    result: str | None = None
    history: list[str] = field(default_factory=list)


def _transition(task: Task, expected: TaskState, new_state: TaskState) -> Task:
    if task.state != expected:
        raise ValueError(f"Cannot transition from {task.state} (expected {expected})")
    task.history.append(f"{task.state.value} -> {new_state.value}")
    task.state = new_state
    return task


def start_work(task: Task, needs_input: bool) -> Task:
    new_state = TaskState.INPUT_REQUIRED if needs_input else TaskState.WORKING
    return _transition(task, TaskState.SUBMITTED, new_state)


def provide_input(task: Task) -> Task:
    return _transition(task, TaskState.INPUT_REQUIRED, TaskState.WORKING)


def complete(task: Task, result: str) -> Task:
    task = _transition(task, TaskState.WORKING, TaskState.COMPLETED)
    task.result = result
    return task


def fail(task: Task, reason: str) -> Task:
    task = _transition(task, TaskState.WORKING, TaskState.FAILED)
    task.result = reason
    return task


def is_terminal(task: Task) -> bool:
    return task.state in {TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELED}


def delegate_task(
    task_id: str, request: str, needs_clarification_check: Callable[[str], bool]
) -> Task:
    task = Task(id=task_id)
    needs_input = needs_clarification_check(request)
    return start_work(task, needs_input=needs_input)
