# Lab 13.01 -- Fix the failing test

**Difficulty:** ★★★★★ · **Time:** ~2-3 hours

## Task

Build a coding agent (Module 04's ReAct loop, plus `read_file`, `write_file`,
and `run_tests` tools) that fixes a bug in `sample_repo/` well enough for
its own test suite to pass, running entirely inside
`shared/sandbox/shell_sandbox.py`. No API key needed -- tested against
`shared.llm.get_client("mock")`.

`sample_repo/` contains a tiny package (`inventory.py`) with one bug and a
`test_inventory.py` that fails against it. It's checked into git as a
**read-only template**: `tests/conftest.py`'s `repo_copy` fixture copies it
into a fresh temp directory (outside this git repo, so a sandboxed `pytest`
run there never picks up this project's own `pyproject.toml`) before each
test, so your agent's edits never touch the tracked files.

## Files

- `starter/coding_agent.py` -- skeleton with the pieces to implement
- `solution/coding_agent.py` -- complete reference implementation
- `sample_repo/` -- the read-only buggy repo template
- `tests/` -- tests that exercise the file tools, the sandboxed test runner, and the full agent loop

## Requirements

Implement these in `starter/coding_agent.py`:

- `def resolve_within_repo(repo_root: Path, relative_path: str) -> Path` --
  resolve `relative_path` against `repo_root`; raise `ValueError` if the
  resolved path isn't inside `repo_root` (see lessons/02).
- `def read_file(repo_root: Path, relative_path: str) -> str` /
  `def write_file(repo_root: Path, relative_path: str, content: str) -> str`
  -- built on `resolve_within_repo`.
- `def run_tests(repo_root: Path) -> ShellResult` -- run `pytest -q` in
  `repo_root` via `shared.sandbox.shell_sandbox.run_shell`.
- `def build_tool_registry(repo_root: Path) -> dict[str, Callable]` -- a
  registry of the three tools as callables taking only the model-supplied
  arguments (bind `repo_root` via closure); `"run_tests"`'s callable should
  return `result.stdout + result.stderr` as a string.
- `def dispatch(tool_call, registry) -> ToolResult` -- same contract as
  prior modules.
- `async def run_coding_agent(client, repo_root: Path, task: str, max_steps: int = 6) -> dict`
  -- the ReAct loop (Module 04) using these tools. After the loop ends
  (naturally, or by exhausting `max_steps`), **independently re-run the
  tests** rather than trusting the model's own claim of success (see
  lessons/03), and return `{"status": "success"|"failed", "steps": <int>, "output": <str>}`.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/coding_agent.py`.
- `resolve_within_repo` raises `ValueError` on a path-traversal attempt
  (e.g. `"../../etc/passwd"`).
- `run_coding_agent` reports `"status": "failed"` when the model *claims*
  success without ever actually fixing the bug (the sample repo's tests
  still fail) -- this is the acceptance criterion that proves your loop
  checks reality, not the model's text.
- `run_coding_agent` reports `"status": "success"` and the correct `steps`
  count when the model reads the file, writes a real fix, and verifies with
  `run_tests` before giving a final answer.
- Hitting `max_steps` without a fix still returns `"status": "failed"`, with
  `steps` equal to `max_steps`.

## Running the tests

```bash
uv run pytest curriculum/13-coding-agents/labs/01-fix-the-failing-test/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/13-coding-agents/labs/01-fix-the-failing-test/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 14 -- Browser & computer-use agents](../../../14-browser-and-computer-use-agents/README.md)
