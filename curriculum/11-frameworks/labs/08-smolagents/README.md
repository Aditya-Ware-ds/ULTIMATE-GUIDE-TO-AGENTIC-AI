# Lab 11.08 -- Reference agent in smolagents

**Last verified:** 2026-09-22 against `smolagents` 1.26.0 (installed and
executed directly).
**Difficulty:** ★★★☆☆ · **Time:** ~1 hour

## About this framework

smolagents (Hugging Face) is a minimal, code-first agent library. Its
`ToolCallingAgent` runs the same observe-think-act loop from Module 04, but
the framework's signature idea (used by its sibling `CodeAgent`, not used in
this lab) is having the model write and execute Python code directly instead
of emitting structured tool-call JSON -- `ToolCallingAgent` is the
closer-to-this-repo's-Module-03 JSON-tool-call style, and what this lab uses.
Testing offline means subclassing `smolagents.models.Model` and overriding
`generate()` -- there's no single official "fake model" class, but the
`Model` base class is a small, stable interface built exactly for this kind
of subclassing.

## Task

Build the module's [reference agent](../../README.md#the-reference-task-built-9-times)
using `@tool`-decorated function and `ToolCallingAgent`, tested with a small
hand-written `ScriptedModel(Model)` subclass.

## Install and run

```bash
uv run --with "smolagents>=1.0.0" pytest curriculum/11-frameworks/labs/08-smolagents/tests
```

Skipped (not failed) via `pytest.importorskip` if `smolagents` isn't installed.

## Files

- `starter/agent.py` -- skeleton to implement
- `solution/agent.py` -- complete reference implementation
- `tests/` -- tests (skip if `smolagents` isn't installed)

## Requirements

Implement in `starter/agent.py`:

- `def calculate(expression: str) -> float` -- the `ast`-based safe evaluator
  from Module 03, decorated with `@tool`. **Important**: smolagents parses
  the docstring's `Args:` section to build the tool schema -- your docstring
  needs a proper Google-style `Args:` block (see the hint below), not just a
  one-line summary.
- `def build_agent(model) -> ToolCallingAgent` -- return a
  `ToolCallingAgent(tools=[calculate], model=model)` (accepting `model` as a
  parameter is what lets tests inject a scripted fake).
- `def run_agent(question: str, model) -> str` -- build the agent and call
  `.run(question)`, returning the result.

## Acceptance criteria

- All tests pass when run with `smolagents` installed via the command above.
- `run_agent` correctly returns the scripted final answer when driven by a
  `ScriptedModel` that calls `calculate` then `final_answer`.
- `calculate` itself still rejects non-arithmetic input.

## Hint: the docstring format smolagents requires

```python
@tool
def calculate(expression: str) -> float:
    """Evaluate a basic arithmetic expression.

    Args:
        expression: The arithmetic expression to evaluate.
    """
    ...
```

Omitting the `Args:` block causes a schema-generation error at agent
construction time, not a silent failure -- if you hit that, check your
docstring format first.

## Running the tests

```bash
uv run --with "smolagents>=1.0.0" pytest curriculum/11-frameworks/labs/08-smolagents/tests
LAB_TARGET=starter uv run --with "smolagents>=1.0.0" pytest curriculum/11-frameworks/labs/08-smolagents/tests
```
