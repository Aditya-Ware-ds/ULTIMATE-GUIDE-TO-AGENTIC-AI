# Lab 11.06 -- Reference agent in Microsoft Agent Framework

**Last verified:** 2026-09-22 against `agent-framework` 1.19.0 (installed and
executed directly).
**Difficulty:** ★★★★☆ · **Time:** ~1.5 hours

## About this framework

Microsoft Agent Framework reached 1.0 GA in April 2026, merging the
previously-separate AutoGen and Semantic Kernel projects into one SDK for
.NET and Python. Its core shape is a `BaseChatClient` (implements
`get_response`) wrapped by an `Agent`. **The one genuinely tricky part,
verified directly by hitting it**: a chat client used for tool-calling must
also inherit from `agent_framework._tools.FunctionInvocationLayer` -- without
that mixin, `Agent` logs "the provided chat client does not support function
invoking" and silently never re-calls your client with the tool's result, so
the run ends with an empty final answer instead of an error. This is exactly
the kind of undocumented-in-the-obvious-place detail that makes installing
and testing a framework directly (rather than trusting a tutorial) worth the
extra time.

## Task

Build the module's [reference agent](../../README.md#the-reference-task-built-9-times)
using a plain Python function tool + `Agent`, tested with a
`ScriptedChatClient(FunctionInvocationLayer, BaseChatClient)`.

## Install and run

```bash
uv run --with "agent-framework>=1.0.0" pytest curriculum/11-frameworks/labs/06-microsoft-agent-framework/tests
```

Skipped (not failed) via `pytest.importorskip` if `agent_framework` isn't
installed. This is a large dependency (~210 packages, including a bundled
`claude-agent-sdk`) -- expect a sizable first-time download.

## Files

- `starter/agent.py` -- skeleton to implement
- `solution/agent.py` -- complete reference implementation
- `tests/` -- tests (skip if `agent_framework` isn't installed)

## Requirements

Implement in `starter/agent.py`:

- `def calculate(expression: str) -> float` -- the `ast`-based safe evaluator
  from Module 03.
- `def build_agent(client) -> Agent` -- return
  `Agent(client, instructions="Use the calculate tool to answer math questions.", tools=[calculate])`.
- `async def run_agent(question: str, client) -> str` -- build the agent,
  `await agent.run(question)`, and return `result.text`.

## Acceptance criteria

- All tests pass when run with `agent-framework` installed via the command above.
- `run_agent` correctly returns the scripted final answer when driven by a
  `ScriptedChatClient` that emits a function-call content, then text.
- `calculate` itself still rejects non-arithmetic input.

## Hint: the `FunctionInvocationLayer` mixin

```python
from agent_framework._tools import FunctionInvocationLayer
from agent_framework import BaseChatClient


class ScriptedChatClient(FunctionInvocationLayer, BaseChatClient): ...
```

Without this mixin (used as the *first* base, so its `__init__` runs and
chains correctly via `super()`), tool calls are silently never dispatched
back to your client -- there's no exception, just a wrong (empty) answer.
This is only needed in your **test fixture**, not in `starter/agent.py`
itself -- `build_agent`/`run_agent` accept any client that already
implements the interface correctly.

## Running the tests

```bash
uv run --with "agent-framework>=1.0.0" pytest curriculum/11-frameworks/labs/06-microsoft-agent-framework/tests
LAB_TARGET=starter uv run --with "agent-framework>=1.0.0" pytest curriculum/11-frameworks/labs/06-microsoft-agent-framework/tests
```
