# Architecture -- Production coding agent

## Overview

```
                 ┌─────────────────────────┐
   task string   │   run_coding_agent()     │   {"status", "steps", "output"}
  ─────────────▶ │  (Module 04 ReAct loop)  │ ──────────────────────────────▶
                 └───────────┬─────────────┘
                             │ tool calls
                             ▼
                 ┌─────────────────────────┐
                 │  build_tool_registry()   │
                 │  read_file / write_file  │
                 │  / run_tests             │
                 └───────────┬─────────────┘
                             │
                             ▼
                 ┌─────────────────────────┐
                 │ shared/sandbox/          │  ← subprocess isolation,
                 │ shell_sandbox.run_shell  │    timeout, restricted env
                 └───────────┬─────────────┘
                             │
                             ▼
                       repo_root (a copy,
                     never the checked-in
                          template)
```

## Design rationale

### Why reuse Module 13's exact agent loop, unmodified

The agent loop, tool set, and independent-verification pattern are
identical to Module 13's lab. This is deliberate: the loop shape (Module
04's ReAct pattern) and the sandboxing/verification discipline (Module 13)
are already correct and tested; this capstone's actual contribution is the
**eval harness** that runs that same, unmodified agent against multiple
repos and reports an aggregate result. Rebuilding the agent loop
differently here would test nothing new and would risk introducing a
regression in a component this curriculum has already verified works.

### Why the eval harness takes the agent as an injected function

`run_eval(run_coding_agent_fn, client_factory, sample_repo_root, tasks)`
never imports `coding_agent` directly -- the agent implementation and the
client factory are both parameters. This means the harness could score a
completely different coding-agent implementation with no changes, the same
generality Module 16's `evaluate_dataset(client, agent_fn, dataset)`
has. An eval harness tightly coupled to one specific agent implementation
is a weaker piece of infrastructure than one that can score anything with
a compatible interface.

### Why `client_factory` instead of a single shared `client`

Each task gets its own fresh client (a fresh `MockLLMProvider` instance in
tests, or a fresh real client in production) rather than sharing one across
all tasks. This avoids one task's scripted responses leaking into another's
-- the same test-isolation reasoning Module 17's `clear_exported_spans`
autouse fixture applies to tracing state, applied here to per-task client
state.

### Why the sample repos are copied fresh per task, never mutated in place

Identical reasoning to Module 13's `repo_copy` fixture: running the
sandboxed `pytest` subprocess against a directory still nested under this
git repo risks it picking up this project's own `pyproject.toml`
configuration, and mutating the checked-in template would make eval runs
non-repeatable. `run_eval` copies each repo into a fresh
`tempfile.TemporaryDirectory()` (outside the git tree) before running the
agent against it.

## What this capstone does not attempt

This is not a claim of general coding-agent capability across arbitrary
real-world repositories -- the sample repos are small and deliberately
simple, chosen to make the eval harness's own correctness verifiable
offline with a scripted mock provider. A production deployment would need
a much larger and more realistic held-out bug set, plus live-model
evaluation (gated behind `@pytest.mark.live`, per this curriculum's
consistent pattern) before trusting a reported pass rate as a real
capability measurement.
