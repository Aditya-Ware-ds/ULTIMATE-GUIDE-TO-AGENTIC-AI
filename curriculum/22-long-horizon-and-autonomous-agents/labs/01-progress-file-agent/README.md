# Lab 22.01 -- Progress file agent

**Difficulty:** ★★★★★ · **Time:** ~2-3 hours

## Task

Build a multi-task agent that tracks its progress in a durable JSON file
and survives being killed and restarted mid-plan without repeating
completed work -- the same pattern this entire repository's own
`PROGRESS.md` has used across its whole multi-session build (see
lessons/03-progress-files-and-resumability.md). No API key needed --
tested against `shared.llm.get_client("mock")`.

## Files

- `starter/progress_agent.py` -- skeleton with the pieces to implement
- `solution/progress_agent.py` -- complete reference implementation
- `tests/` -- tests including the kill-and-resume scenario

## Requirements

Implement these in `starter/progress_agent.py`:

- `def load_progress(path: Path) -> list[dict] | None` -- return the
  `"tasks"` list from `path` (parsed as JSON), or `None` if `path` doesn't
  exist yet.
- `def save_progress(path: Path, tasks: list[dict]) -> None` -- write
  `{"tasks": tasks}` to `path` as JSON.
- `async def run_task(client, task_name: str) -> str` -- send `task_name`
  as a single user message, return the model's text response.
- `async def run_one_task_and_persist(client, progress_path, tasks, task_index) -> list[dict]`
  -- run `tasks[task_index]` via `run_task`, set its `"result"`, mark its
  `"status"` as `"done"`, call `save_progress`, and return `tasks`.
- `async def run_long_horizon_agent(client, progress_path: Path, task_names: list[str]) -> dict`
  -- load existing progress (or initialize a fresh one, all `"pending"`,
  and save it), then run every still-`"pending"` task in order via
  `run_one_task_and_persist`, skipping any already `"done"`. Return
  `{"tasks": tasks}`.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/progress_agent.py`.
- `load_progress` returns `None` for a nonexistent file, and round-trips
  correctly with `save_progress`.
- **The kill-and-resume test passes**: calling `run_one_task_and_persist`
  directly for one task (simulating a crash right after it), then calling
  `run_long_horizon_agent` again (simulating a restart), completes only the
  remaining tasks -- the already-`"done"` task is never re-run (verified via
  `client.provider.call_count` and the mock provider running out of
  scripted responses if it were).
- A fresh call to `run_long_horizon_agent` with no existing progress file
  initializes one with every task `"pending"` before running any of them.

## Running the tests

```bash
uv run pytest curriculum/22-long-horizon-and-autonomous-agents/labs/01-progress-file-agent/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/22-long-horizon-and-autonomous-agents/labs/01-progress-file-agent/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 23 -- Research literacy](../../../23-research-literacy/README.md)
