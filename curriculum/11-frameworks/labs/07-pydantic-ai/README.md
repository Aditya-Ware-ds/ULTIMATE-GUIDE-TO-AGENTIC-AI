# Lab 11.07 -- Reference agent in Pydantic AI

**Last verified:** 2026-09-22 against `pydantic-ai` 2.47.0 (installed and
executed directly).
**Difficulty:** ★★★☆☆ · **Time:** ~1 hour

## About this framework

Pydantic AI (from the team behind Pydantic) is a typed, validation-first
agent framework -- tools and outputs are defined with regular Python type
hints and Pydantic models, and the framework validates everything against
them. Its testing story is unusually good for this module's purposes: it
ships **`TestModel`** (auto-calls tools with synthetic arguments -- good for
exercising code paths, not for scripting exact behavior) and **`FunctionModel`**
(a plain Python function you control completely, returning exactly the
response you script) built in, specifically for offline testing.

## Task

Build the module's [reference agent](../../README.md#the-reference-task-built-9-times)
using Pydantic AI's `Agent` class and `@agent.tool_plain` decorator, tested
with `FunctionModel` (not `TestModel` -- see pitfalls.md for why `TestModel`'s
default auto-calling behavior doesn't fit this task).

## Install and run

This framework is **not** in the default `make setup` install (see the
module README for why). Run its tests with an ephemeral overlay environment:

```bash
uv run --with "pydantic-ai>=2.0.0" pytest curriculum/11-frameworks/labs/07-pydantic-ai/tests
```

Without `pydantic-ai` installed, these tests are skipped (not failed) via
`pytest.importorskip` -- `make test` stays green without it.

## Files

- `starter/agent.py` -- skeleton to implement
- `solution/agent.py` -- complete reference implementation
- `tests/` -- tests (skip if `pydantic_ai` isn't installed)

## Requirements

Implement in `starter/agent.py`:

- `def calculate(expression: str) -> float` -- the `ast`-based safe evaluator
  from Module 03 (no `eval()`).
- `AGENT: Agent` -- module-level `pydantic_ai.Agent` instance with a system
  prompt instructing it to use the `calculate` tool for math questions, and
  `calculate` registered via `@AGENT.tool_plain`.
- `def run_agent(question: str, model) -> str` -- call
  `AGENT.run_sync(question, model=model).output` and return it (accepting
  `model` as a parameter, rather than hardcoding one, is what lets tests inject
  `FunctionModel`).

## Acceptance criteria

- All tests pass when run with `pydantic-ai` installed via the command above.
- `run_agent` correctly returns the scripted final answer when driven by a
  `FunctionModel` that calls `calculate` then returns text.
- `calculate` itself still rejects non-arithmetic input (same contract as
  every prior module's version).

## Running the tests

```bash
uv run --with "pydantic-ai>=2.0.0" pytest curriculum/11-frameworks/labs/07-pydantic-ai/tests
LAB_TARGET=starter uv run --with "pydantic-ai>=2.0.0" pytest curriculum/11-frameworks/labs/07-pydantic-ai/tests
```
