# Lab 11.05 -- Reference agent in CrewAI

**Last verified:** 2026-09-22 against `crewai` 1.15.22 (installed and
executed directly).
**Difficulty:** ★★★★☆ · **Time:** ~1.5 hours

## About this framework

CrewAI organizes work around **roles**: an `Agent` (role, goal, backstory,
tools), a `Task` (description, expected output, assigned agent), and a
`Crew` (agents + tasks, run via `.kickoff()`) -- a higher-level abstraction
than this module's other frameworks, built for multi-agent "teams" (Module
12's territory), used here with just one agent for the reference task.
**Important difference from every other framework in this module**:
CrewAI's `BaseLLM.call(...)` hands you `available_functions` directly and
expects *your LLM implementation* to decide whether and how to invoke them --
there's no separate "tool call" object for an external executor to
interpret. A scripted fake LLM here calls the tool itself and returns the
final text in one `call()` invocation, which is a legitimate use of the
actual extension point, not a workaround.

## Task

Build the module's [reference agent](../../README.md#the-reference-task-built-9-times)
using `@tool` + `Agent` + `Task` + `Crew`, tested with a hand-written
`ScriptedLLM(BaseLLM)`.

## Install and run

```bash
uv run --with "crewai>=1.0.0" pytest curriculum/11-frameworks/labs/05-crewai/tests
```

Skipped (not failed) via `pytest.importorskip` if `crewai` isn't installed.
This is a heavy dependency (CrewAI bundles vector-store/RAG tooling by
default) -- expect a sizable first-time download.

## Files

- `starter/agent.py` -- skeleton to implement
- `solution/agent.py` -- complete reference implementation
- `tests/` -- tests (skip if `crewai` isn't installed)

## Requirements

Implement in `starter/agent.py`:

- `def calculate(expression: str) -> float` -- the `ast`-based safe evaluator
  from Module 03, decorated with `@tool("calculate")` (from `crewai.tools`).
- `def build_crew(llm, question: str) -> Crew` -- construct an `Agent`
  (role="Calculator", goal="Answer math questions", backstory="You use the
  calculate tool.", tools=[calculate], llm=llm), a `Task` whose
  `description` is `question` (with an `expected_output` describing a
  numeric answer), and return a `Crew(agents=[agent], tasks=[task])`. Note
  the task description is fixed at crew-construction time in this simple
  design -- that's why `question` is a parameter here, not baked in.
- `def run_agent(question: str, llm) -> str` -- build the crew via
  `build_crew` and call `.kickoff()`, returning `str(result)`.

## Acceptance criteria

- All tests pass when run with `crewai` installed via the command above.
- `run_agent` correctly returns the scripted final answer when driven by a
  `ScriptedLLM` whose `call()` invokes `calculate` via `available_functions`.
- `calculate` itself still rejects non-arithmetic input.

## Running the tests

```bash
uv run --with "crewai>=1.0.0" pytest curriculum/11-frameworks/labs/05-crewai/tests
LAB_TARGET=starter uv run --with "crewai>=1.0.0" pytest curriculum/11-frameworks/labs/05-crewai/tests
```
