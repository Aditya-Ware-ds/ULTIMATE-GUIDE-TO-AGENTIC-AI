# Lab 11.04 -- Reference agent in Google ADK

**Last verified:** 2026-09-22 against `google-adk` 2.9.2 (installed and
executed directly).
**Difficulty:** ★★★★☆ · **Time:** ~1.5 hours

## About this framework

Google's Agent Development Kit (ADK) is a code-first, session-oriented
framework -- agents run through a `Runner` bound to a session/user ID, which
is more ceremony than most other frameworks in this module for a simple
one-shot question, but reflects ADK's multi-turn, stateful design center.
For testing, ADK ships `InMemoryRunner.run_debug(...)`, an **official,
explicitly-documented debug/testing convenience method** ("designed for
developers ... who want to quickly test agents without dealing with session
management") -- combined with a hand-written `BaseLlm` subclass for scripting
responses, this gives clean offline testing.

## Task

Build the module's [reference agent](../../README.md#the-reference-task-built-9-times)
using a plain Python function tool + `LlmAgent`, tested with a
`ScriptedLlm(BaseLlm)` and `InMemoryRunner.run_debug(...)`.

## Install and run

```bash
uv run --with "google-adk>=1.0.0" pytest curriculum/11-frameworks/labs/04-google-adk/tests
```

Skipped (not failed) via `pytest.importorskip` if `google.adk` isn't
installed. The first run downloads a fairly large dependency tree (~48
packages) -- subsequent runs are fast once cached.

## Files

- `starter/agent.py` -- skeleton to implement
- `solution/agent.py` -- complete reference implementation
- `tests/` -- tests (skip if `google.adk` isn't installed)

## Requirements

Implement in `starter/agent.py`:

- `def calculate(expression: str) -> float` -- the `ast`-based safe evaluator
  from Module 03. ADK accepts a plain Python function directly as a tool (no
  decorator needed) -- it infers the schema from type hints and docstring.
- `def build_agent(model) -> LlmAgent` -- return
  `LlmAgent(name="calc_agent", model=model, instruction="Use the calculate tool to answer math questions.", tools=[calculate])`.
- `async def run_agent(question: str, model) -> str` -- build the agent,
  wrap it in `InMemoryRunner(agent=agent)`, call
  `await runner.run_debug(question, quiet=True)`, and return the last text
  part found across the returned events (see hint).

## Acceptance criteria

- All tests pass when run with `google-adk` installed via the command above.
- `run_agent` correctly returns the scripted final answer when driven by a
  `ScriptedLlm` that emits a function call, then text.
- `calculate` itself still rejects non-arithmetic input.

## Hint: extracting the final text from `run_debug`'s events

`run_debug` returns `list[Event]`; each event may have `event.content.parts`,
a list of parts that can be a function call or text. Walk the events in
order and keep the last part with a non-empty `.text` -- that's the agent's
final answer.

## Running the tests

```bash
uv run --with "google-adk>=1.0.0" pytest curriculum/11-frameworks/labs/04-google-adk/tests
LAB_TARGET=starter uv run --with "google-adk>=1.0.0" pytest curriculum/11-frameworks/labs/04-google-adk/tests
```
