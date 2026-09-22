# Lab 11.01 -- Reference agent in LangGraph

**Last verified:** 2026-09-22 against `langgraph` 1.2.12 and `langchain` 1.4.2
(installed and executed directly).
**Difficulty:** ★★★★☆ · **Time:** ~1.5 hours

## About this framework

LangGraph is the most-adopted production agent orchestration framework as of
2026, built around an explicit graph/state-machine model with first-class
checkpointing. Its own prebuilt `create_react_agent` (from
`langgraph.prebuilt`) is now **deprecated** in favor of `create_agent` from
the `langchain` package (verified directly -- several 2026-era tutorials still
show the old function; don't trust them without checking). Offline testing
means writing a small `BaseChatModel` subclass -- LangChain's built-in fake
chat models (e.g. `GenericFakeChatModel`) aren't built for scripting tool
calls, so a custom subclass overriding `_generate` and `bind_tools` is the
reliable path, similar in spirit to smolagents' custom `Model` subclass.

## Task

Build the module's [reference agent](../../README.md#the-reference-task-built-9-times)
using `langchain_core.tools.tool` + `langchain.agents.create_agent`, tested
with a hand-written `ScriptedChatModel(BaseChatModel)`.

## Install and run

```bash
uv run --with "langgraph>=1.0.0" --with "langchain>=1.0.0" pytest curriculum/11-frameworks/labs/01-langgraph/tests
```

Skipped (not failed) via `pytest.importorskip` if `langgraph`/`langchain` aren't installed.

## Files

- `starter/agent.py` -- skeleton to implement
- `solution/agent.py` -- complete reference implementation
- `tests/` -- tests (skip if the framework isn't installed)

## Requirements

Implement in `starter/agent.py`:

- `def calculate(expression: str) -> float` -- the `ast`-based safe evaluator
  from Module 03, decorated with `@tool` (from `langchain_core.tools`).
- `def build_agent(model)` -- return
  `create_agent(model, tools=[calculate], system_prompt="Use the calculate tool to answer math questions.")`.
- `def run_agent(question: str, model) -> str` -- build the agent, call
  `.invoke({"messages": [{"role": "user", "content": question}]})`, and return
  `result["messages"][-1].content`.

## Acceptance criteria

- All tests pass when run with `langgraph`/`langchain` installed via the
  command above.
- `run_agent` correctly returns the scripted final answer when driven by a
  `ScriptedChatModel` that emits a `calculate` tool call, then text.
- `calculate` itself still rejects non-arithmetic input.

## Hint: why `bind_tools` needs overriding too

`create_agent` calls `model.bind_tools(tools)` before every model call --
`BaseChatModel`'s default `bind_tools` raises `NotImplementedError` (it's an
abstract hook real chat model integrations implement to attach tool schemas
to outgoing requests). Since a scripted test model ignores the actual tool
schema and always returns whatever you scripted, overriding `bind_tools` to
just `return self` is sufficient -- don't spend time trying to make it "real."

## Running the tests

```bash
uv run --with "langgraph>=1.0.0" --with "langchain>=1.0.0" pytest curriculum/11-frameworks/labs/01-langgraph/tests
LAB_TARGET=starter uv run --with "langgraph>=1.0.0" --with "langchain>=1.0.0" pytest curriculum/11-frameworks/labs/01-langgraph/tests
```
