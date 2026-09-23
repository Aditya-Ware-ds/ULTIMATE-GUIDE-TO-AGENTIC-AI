# Capstone 1 -- Production coding agent

**Difficulty:** ★★★★★ · **Time:** ~4-6 hours
**Draws on:** Module 04 (agent loop), Module 13 (coding agents), Module 16 (evaluation), Module 18 (security)

## Spec

Build a coding agent that fixes real bugs in small sample repos, and an
eval harness that scores it across a set of repos -- the "held-out test
set" requirement from the original curriculum plan. This capstone
generalizes Module 13's lab (a single sample repo, one bug) into something
closer to a real evaluation: the same agent implementation run, unmodified,
against several different repos with different bugs, reporting an
aggregate pass rate.

No API key needed -- tested against `shared.llm.get_client("mock")`. See
[`ARCHITECTURE.md`](ARCHITECTURE.md) for design rationale,
[`THREAT_MODEL.md`](THREAT_MODEL.md) for the security analysis, and
[`DEPLOY.md`](DEPLOY.md) for how this would be deployed.

`sample_repo/{calculator,strings,numbers}/` are three small, read-only
template repos, each with one distinct, real bug (a wrong operator, a
no-op string function, a swapped min/max) and a failing test. Like Module
13's lab, each is copied into a fresh temp directory per test/eval run --
the agent's edits never touch the checked-in templates.

## Files

- `starter/coding_agent.py`, `starter/eval_harness.py` -- skeletons with the pieces to implement
- `solution/coding_agent.py`, `solution/eval_harness.py` -- complete reference implementation
- `sample_repo/` -- the three read-only buggy repo templates
- `tests/` -- tests for both the agent and the eval harness

## Requirements

### `coding_agent.py`

Identical contract to Module 13's lab: `resolve_within_repo`, `read_file`,
`write_file`, `run_tests`, `build_tool_registry`, `dispatch`, and
`run_coding_agent` (the ReAct loop, with an independent post-loop test
re-run -- never trust the model's own claim of success). If you've
completed Module 13's lab, this is the same implementation.

### `eval_harness.py`

- `async def run_eval(run_coding_agent_fn, client_factory, sample_repo_root: Path, tasks=None) -> dict`
  -- for each task in `tasks` (default `SAMPLE_TASKS`): copy
  `sample_repo_root/task["repo"]` into a fresh temp directory, get a fresh
  client from `client_factory()`, and call
  `run_coding_agent_fn(client, repo_copy, task["task"])`. Return
  `{"total": ..., "passed": ..., "pass_rate": ..., "results": [{"repo": ..., "status": ...}, ...]}`.

The harness is generic over the agent implementation (Module 16's
`evaluate_dataset` shape: the agent function and a client factory are
injected, not imported) -- it could score a different coding-agent
implementation entirely with no changes.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/` implementations.
- `run_coding_agent` never reports `"success"` without the sandboxed test
  suite actually passing (verified via the false-claim-of-success test).
- `run_eval` reports an accurate `pass_rate` across a mix of passing and
  failing repos (verified via the partial-pass-rate test).
- Every threat named in [`THREAT_MODEL.md`](THREAT_MODEL.md) maps to a
  specific, currently-passing test.

## Running the tests

```bash
uv run pytest capstones/01-production-coding-agent/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest capstones/01-production-coding-agent/tests
```

## Next

[Capstone 2 -- Multi-agent research system](../02-multi-agent-research-system/README.md)
