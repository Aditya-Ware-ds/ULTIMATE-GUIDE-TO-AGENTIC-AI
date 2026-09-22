# Lab 11.02 -- Reference agent in the OpenAI Agents SDK

**Last verified:** 2026-09-22 against `openai-agents` 0.22.3 (installed and
executed directly).
**Difficulty:** ★★★★☆ · **Time:** ~1.5 hours

## About this framework

The OpenAI Agents SDK is deliberately minimal -- an `Agent` (name,
instructions, tools, model) and a `Runner` that drives the loop. Offline
testing means implementing the SDK's `Model` protocol (`agents.models.interface.Model`)
directly: a class with an async `get_response(...)` method returning a
`ModelResponse` built from the same typed output items (`ResponseFunctionToolCall`,
`ResponseOutputMessage`) the real OpenAI Responses API returns -- there's no
separate "fake model" helper shipped, but the protocol itself is small and
stable enough to implement directly.

## Task

Build the module's [reference agent](../../README.md#the-reference-task-built-9-times)
using `@function_tool` + `Agent` + `Runner.run`, tested with a hand-written
`ScriptedModel(Model)`.

## Install and run

```bash
uv run --with "openai-agents>=0.5.0" pytest curriculum/11-frameworks/labs/02-openai-agents-sdk/tests
```

Skipped (not failed) via `pytest.importorskip` if `agents` isn't installed.
No `OPENAI_API_KEY` needed -- you'll see a harmless
`"OPENAI_API_KEY is not set, skipping trace export"` message; that's the
SDK's optional telemetry export being skipped, not a failure.

## Files

- `starter/agent.py` -- skeleton to implement
- `solution/agent.py` -- complete reference implementation
- `tests/` -- tests (skip if `agents` isn't installed)

## Requirements

Implement in `starter/agent.py`:

- `def _evaluate(expression: str) -> float` -- the `ast`-based safe evaluator
  from Module 03, kept as a plain function separate from the tool wrapper
  below (the SDK's tool-invocation path needs a real `ToolContext`, so it
  isn't meant to be called directly in tests -- keeping the logic in its own
  testable function is the standard pattern for this).
- `calculate` -- an `@function_tool`-decorated function that calls
  `_evaluate(expression)`. Like smolagents, this SDK parses a Google-style
  `Args:` docstring block to build the tool schema.
- `def build_agent(model) -> Agent` -- return an `Agent(name="calc_agent",
  instructions="Use the calculate tool to answer math questions.",
  tools=[calculate], model=model)`.
- `async def run_agent(question: str, model) -> str` -- `await Runner.run(agent, question)`
  and return `result.final_output`.

## Acceptance criteria

- All tests pass when run with `openai-agents` installed via the command above.
- `run_agent` correctly returns the scripted final answer when driven by a
  `ScriptedModel` that emits a function-call output item, then a message item.
- `calculate` itself still rejects non-arithmetic input.

## Running the tests

```bash
uv run --with "openai-agents>=0.5.0" pytest curriculum/11-frameworks/labs/02-openai-agents-sdk/tests
LAB_TARGET=starter uv run --with "openai-agents>=0.5.0" pytest curriculum/11-frameworks/labs/02-openai-agents-sdk/tests
```
