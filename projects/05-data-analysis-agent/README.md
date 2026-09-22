# Project 05 -- Data-analysis agent with a code sandbox

**Difficulty:** ★★★★☆ · **Time estimate:** 2-3 hours
**Comes after:** Level 4 (Modules 13-15)

## Spec

Build an agent that answers questions about a small bundled CSV dataset by
writing and running Python, entirely inside `shared/sandbox/code_sandbox.py`
-- reusing Module 13's exact sandboxing discipline (never `exec()`
model-generated code directly) for a new kind of task.

This is an integration project: it reuses Module 04's ReAct loop and
Module 13's sandboxed-execution pattern almost directly, applied to data
analysis instead of bug-fixing. No API key needed -- tested against
`shared.llm.get_client("mock")`.

`dataset/sales.csv` is a tiny, checked-in dataset (6 rows: 2 products across
3 months). It's a read-only template: `tests/conftest.py`'s `dataset_dir`
fixture copies it into a fresh temp directory per test, so the agent's
sandboxed code never touches the repo's tracked files (same reasoning as
Module 13's `repo_copy` fixture).

## Files

- `starter/data_agent.py` -- skeleton with the pieces to implement
- `solution/data_agent.py` -- complete reference implementation
- `dataset/sales.csv` -- the read-only bundled dataset template
- `tests/` -- tests that exercise real sandboxed execution, error handling, and the full agent loop

## Requirements

Implement these in `starter/data_agent.py`:

- `def run_analysis(code: str, dataset_dir: Path) -> str` -- run `code` via
  `shared.sandbox.code_sandbox.run_python(code, cwd=dataset_dir)`. Return
  `result.stdout` on success, or `f"Error running code:\n{result.stderr}"`
  if it failed -- never raise on the sandboxed code's own errors.
- `def build_tool_registry(dataset_dir: Path) -> dict[str, Callable]` -- a
  registry with one entry, `"run_analysis"`, as a callable taking only the
  model-supplied `code` argument (bind `dataset_dir` via closure).
- `def dispatch(tool_call, registry) -> ToolResult` -- same contract as
  prior modules.
- `async def run_data_analysis_agent(client, dataset_dir: Path, task: str, max_steps: int = 6) -> str`
  -- the ReAct loop (Module 04) using this one tool.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/data_agent.py`.
- `run_analysis` returns real, correct output for real correct code (e.g.
  summing revenue via `csv.DictReader`) -- this actually executes the code,
  it's not a stub.
- `run_analysis` surfaces a Python exception's traceback as an
  `"Error running code:\n..."` string instead of letting the exception
  propagate out of the sandbox.
- `run_data_analysis_agent` correctly continues the loop after a tool call
  that errors (the model gets to see the error and try again), matching the
  "self-correcting loop" pattern from Module 13.
- Hitting `max_steps` returns a message that says so, not a bare answer.

## Running the tests

```bash
uv run pytest projects/05-data-analysis-agent/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest projects/05-data-analysis-agent/tests
```

## Next

Level 4 (and its interleaved projects) is complete. Continue to
[Level 5, Module 16 -- Evaluation](../../curriculum/16-evaluation/README.md).
