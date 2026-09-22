# Lab 12.01 -- Supervisor-worker

**Difficulty:** ★★★★☆ · **Time:** ~2 hours

## Task

Build a hand-rolled supervisor-worker system (lessons/01-topologies.md) with
three specialized workers (`researcher`, `writer`, `critic`) and no
framework. The supervisor routes a task to the right worker, then either
synthesizes the worker's output into a final answer or escalates -- it must
never treat a failed worker as a success (lessons/02-failure-modes.md). No
API key needed -- tested against `shared.llm.get_client("mock")`.

## Files

- `starter/agents.py` -- skeleton; the three workers are given, you implement routing/synthesis/supervision
- `solution/agents.py` -- complete reference implementation
- `tests/` -- tests that exercise routing, synthesis, success, and escalation

## Requirements

Implement these in `starter/agents.py` (the `researcher`/`writer`/`critic`
worker functions are already provided):

- `async def route_to_worker(client, task: str, worker_names: list[str]) -> str`
  -- ask the model (one user message) to choose exactly one name from
  `worker_names` and reply with only that name. Raise `ValueError` if the
  model's reply isn't in `worker_names` -- no silent default.
- `async def synthesize(client, task: str, worker_output: str) -> str` --
  ask the model to turn the worker's raw output into a final, polished
  answer for the user.
- `async def supervisor(client, task: str, workers: dict[str, WorkerFn]) -> dict`
  -- route to a worker, call it, then:
  - if the worker's result `"status"` is not `"success"`, return
    `{"status": "escalated", "worker": <name>, "reason": <worker's output>}`
    **without** calling `synthesize`,
  - otherwise return `{"status": "success", "worker": <name>, "output": <synthesized text>}`.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/agents.py`.
- `route_to_worker` raises `ValueError` when the model names a worker not in
  the allowed list.
- `supervisor` makes exactly 2 model calls (route + synthesize) on a
  successful worker run, and exactly 1 model call (route only) when the
  worker reports `"status": "error"` -- verified by asserting on
  `client.provider.call_count`.
- `supervisor` never calls `synthesize` on a failed worker's output (this is
  the "explicit status, not inferred success" discipline from
  lessons/02-failure-modes.md).

## Running the tests

```bash
uv run pytest curriculum/12-multi-agent-systems/labs/01-supervisor-worker/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/12-multi-agent-systems/labs/01-supervisor-worker/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[`projects/`](../../../../projects/README.md) for "MCP server for a real
public API" and "multi-agent content pipeline," then
[Module 13 -- Coding agents](../../../13-coding-agents/README.md)
