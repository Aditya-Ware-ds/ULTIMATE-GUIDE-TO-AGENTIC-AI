# Lab 10.02 -- A2A-style task handoff

**Difficulty:** ★★★☆☆ · **Time:** ~1.5 hours

## Task

Implement a minimal, illustrative version of A2A's task lifecycle (this is
**not** the full A2A wire protocol/SDK -- it's the core state-machine concept,
simplified for learning) and use it to model one agent delegating a task to
another, including an `input-required` pause and resumption.

No API key needed -- this is pure Python state-machine logic, no LLM calls.

## Files

- `starter/a2a.py` -- skeleton with the task lifecycle to implement
- `solution/a2a.py` -- complete reference implementation
- `tests/` -- tests that exercise both

## Requirements

Implement these in `starter/a2a.py`:

- `class TaskState(StrEnum)` with values `SUBMITTED = "submitted"`,
  `WORKING = "working"`, `INPUT_REQUIRED = "input-required"`,
  `COMPLETED = "completed"`, `FAILED = "failed"`, `CANCELED = "canceled"`.
- `@dataclass class Task` with `id: str`, `state: TaskState = TaskState.SUBMITTED`,
  `result: str | None = None`, `history: list[str] = field(default_factory=list)`
  (append a short description of each transition to `history` as it happens,
  e.g. `"submitted -> working"`).
- `def start_work(task: Task, needs_input: bool) -> Task` -- transitions from
  `SUBMITTED` to `WORKING` (or `INPUT_REQUIRED` if `needs_input`). Raise
  `ValueError` if `task.state != TaskState.SUBMITTED`.
- `def provide_input(task: Task) -> Task` -- transitions from
  `INPUT_REQUIRED` to `WORKING`. Raise `ValueError` if
  `task.state != TaskState.INPUT_REQUIRED`.
- `def complete(task: Task, result: str) -> Task` -- transitions from
  `WORKING` to `COMPLETED`, setting `task.result`. Raise `ValueError` if
  `task.state != TaskState.WORKING`.
- `def fail(task: Task, reason: str) -> Task` -- transitions from `WORKING` to
  `FAILED`, setting `task.result = reason`. Raise `ValueError` if
  `task.state != TaskState.WORKING`.
- `def is_terminal(task: Task) -> bool` -- `True` for `COMPLETED`, `FAILED`,
  or `CANCELED`; `False` otherwise.
- `def delegate_task(task_id: str, request: str, needs_clarification_check) -> Task`
  -- a small orchestration function: create a `Task`, call
  `needs_clarification_check(request)` (a callable you're given, returning
  `bool`) to decide whether to start with `needs_input=True`, and call
  `start_work` accordingly. Return the task in whatever state that leaves it
  (do not auto-complete it -- that's a separate step, see tests).

## Acceptance criteria

- All tests in `tests/` pass against your `starter/a2a.py`.
- Every transition function raises `ValueError` when called from the wrong
  state (e.g. calling `complete()` on a `SUBMITTED` task) -- these are not
  silently ignored or auto-corrected.
- `Task.history` accurately records every transition in order.
- `is_terminal` correctly distinguishes terminal from non-terminal states.

## Running the tests

```bash
uv run pytest curriculum/10-protocols/labs/02-a2a-task-handoff/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/10-protocols/labs/02-a2a-task-handoff/tests
```

## Next

[`labs/03-agent-skill-package/`](../03-agent-skill-package/README.md)
