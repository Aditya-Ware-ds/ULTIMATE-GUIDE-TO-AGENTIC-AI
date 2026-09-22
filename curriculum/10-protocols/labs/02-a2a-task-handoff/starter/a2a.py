"""Lab 10.02: A2A-style task handoff. See ../README.md for the full spec.

This is a simplified, illustrative version of A2A's task lifecycle concept --
not the full wire protocol/SDK. Fill in the pieces below. Run the tests with:
    LAB_TARGET=starter uv run pytest \
        curriculum/10-protocols/labs/02-a2a-task-handoff/tests
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field  # noqa: F401 -- used below
from enum import StrEnum  # noqa: F401 -- used below


class TaskState(StrEnum):
    """TODO: define SUBMITTED, WORKING, INPUT_REQUIRED, COMPLETED, FAILED, CANCELED."""


@dataclass
class Task:
    """TODO: define id, state (default SUBMITTED), result, history (default empty list)."""


def start_work(task: Task, needs_input: bool) -> Task:
    """TODO: implement this (see ../README.md)."""
    raise NotImplementedError


def provide_input(task: Task) -> Task:
    """TODO: implement this."""
    raise NotImplementedError


def complete(task: Task, result: str) -> Task:
    """TODO: implement this."""
    raise NotImplementedError


def fail(task: Task, reason: str) -> Task:
    """TODO: implement this."""
    raise NotImplementedError


def is_terminal(task: Task) -> bool:
    """TODO: implement this."""
    raise NotImplementedError


def delegate_task(
    task_id: str, request: str, needs_clarification_check: Callable[[str], bool]
) -> Task:
    """TODO: implement this (see ../README.md)."""
    raise NotImplementedError
