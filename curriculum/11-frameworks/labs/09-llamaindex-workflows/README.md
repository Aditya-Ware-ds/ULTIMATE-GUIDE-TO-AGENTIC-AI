# Lab 11.09 -- Reference agent in LlamaIndex Workflows

**Last verified:** 2026-09-22 against `llama-index-core` 0.14.25 (installed and
executed directly).
**Difficulty:** ★★★☆☆ · **Time:** ~1 hour

## About this framework

LlamaIndex is best known for retrieval (Module 06's territory), but its
`agent.workflow.FunctionAgent` is a general tool-calling agent, built on
LlamaIndex's broader event-driven Workflows engine. Offline testing uses
`llama_index.core.llms.MockFunctionCallingLLM`, which takes a
`response_generator` callable you control completely -- the closest analogue
in this framework to this repo's own `MockLLMProvider`.

## Task

Build the module's [reference agent](../../README.md#the-reference-task-built-9-times)
using `FunctionTool` + `FunctionAgent`, tested with a scripted
`MockFunctionCallingLLM`.

## Install and run

```bash
uv run --with "llama-index-core>=0.12.0" pytest curriculum/11-frameworks/labs/09-llamaindex-workflows/tests
```

Skipped (not failed) via `pytest.importorskip` if `llama_index.core` isn't installed.

## Files

- `starter/agent.py` -- skeleton to implement
- `solution/agent.py` -- complete reference implementation
- `tests/` -- tests (skip if `llama_index.core` isn't installed)

## Requirements

Implement in `starter/agent.py`:

- `def calculate(expression: str) -> float` -- the `ast`-based safe evaluator
  from Module 03.
- `CALCULATE_TOOL: FunctionTool` -- built via
  `FunctionTool.from_defaults(fn=calculate, name="calculate", description=...)`.
- `def build_agent(llm) -> FunctionAgent` -- return
  `FunctionAgent(tools=[CALCULATE_TOOL], llm=llm)`.
- `async def run_agent(question: str, llm) -> str` -- build the agent and
  `await agent.run(question)`, returning the result as a string
  (`str(result)`).

## Acceptance criteria

- All tests pass when run with `llama-index-core` installed via the command above.
- `run_agent` correctly returns the scripted final answer when driven by a
  `MockFunctionCallingLLM` whose `response_generator` calls `calculate` then
  returns text.
- `calculate` itself still rejects non-arithmetic input.

## Running the tests

```bash
uv run --with "llama-index-core>=0.12.0" pytest curriculum/11-frameworks/labs/09-llamaindex-workflows/tests
LAB_TARGET=starter uv run --with "llama-index-core>=0.12.0" pytest curriculum/11-frameworks/labs/09-llamaindex-workflows/tests
```

## Next

[`lessons/02-comparison-matrix-and-how-to-choose.md`](../../lessons/02-comparison-matrix-and-how-to-choose.md)
