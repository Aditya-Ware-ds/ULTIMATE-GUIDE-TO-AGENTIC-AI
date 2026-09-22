# Lab 11.03 -- Reference agent in the Claude Agent SDK

**Last verified:** 2026-09-22 against `claude-agent-sdk` 0.2.157 (installed
and inspected/executed directly, short of a live model call -- see below).
**Difficulty:** ★★★☆☆ · **Time:** ~1 hour

## About this framework -- and why it's different from the other 8

The Claude Agent SDK is not a "bring your own model" agent framework like
the other 8 in this module. It's a thin Python wrapper around the **actual
Claude Code agent loop** -- the same tool execution, permission system, and
loop that powers the Claude Code CLI -- bundled and driven from your own
program. `query()`/`ClaudeSDKClient` always call the real, bundled Claude
Code CLI, which always calls a real Claude model. There is no `Model`/
`BaseLlm`/`BaseChatModel`-style protocol to substitute a scripted fake
response, unlike every other framework in this module -- verified directly by
inspecting `ClaudeAgentOptions`'s full field list (no model-injection point)
and confirming `query()` has no parameter for it either.

**Consequence for this lab, honestly stated**: the full agent-loop test
**requires a real Anthropic API key or Claude subscription** and is marked
`@pytest.mark.live` (excluded from `make test`/default `pytest` runs, per
this repo's `live` marker convention -- see `pyproject.toml`). What *is*
offline-testable, and what this lab's default test covers: the tool
definition and the arithmetic logic itself, which don't depend on the SDK
actually calling a model.

## Task

Build the module's [reference agent](../../README.md#the-reference-task-built-9-times)
using `@tool` + `create_sdk_mcp_server` (this SDK exposes custom tools via an
in-process MCP server -- the exact mechanism Module 10 built by hand) +
`ClaudeAgentOptions` + `query()`.

## Install and run

```bash
# Offline-testable parts (tool definition, arithmetic logic):
uv run --with "claude-agent-sdk>=0.2.0" pytest curriculum/11-frameworks/labs/03-claude-agent-sdk/tests

# Full agent loop (requires a real ANTHROPIC_API_KEY or Claude Code CLI auth):
uv run --with "claude-agent-sdk>=0.2.0" pytest -m live curriculum/11-frameworks/labs/03-claude-agent-sdk/tests
```

Skipped (not failed) via `pytest.importorskip` if `claude_agent_sdk` isn't installed.

## Files

- `starter/agent.py` -- skeleton to implement
- `solution/agent.py` -- complete reference implementation
- `tests/` -- offline tests (default) + one `live`-marked end-to-end test

## Requirements

Implement in `starter/agent.py`:

- `def _evaluate(expression: str) -> float` -- the `ast`-based safe evaluator
  from Module 03, kept separate and directly testable (same reasoning as the
  OpenAI Agents SDK lab: the actual tool handler below needs the SDK's async
  MCP-tool calling convention, which isn't meant to be invoked directly in
  tests).
- `calculate` -- an `@tool("calculate", "Evaluate a basic arithmetic
  expression.", {"expression": str})`-decorated **async** function taking
  `args: dict` and returning
  `{"content": [{"type": "text", "text": str(_evaluate(args["expression"]))}]}`
  (this SDK's tool handlers return MCP-shaped content dicts directly, not a
  bare value -- see Module 10, lesson 2 for the same content-block shape).
- `def build_options() -> ClaudeAgentOptions` -- wrap `calculate` in
  `create_sdk_mcp_server("calculator", tools=[calculate])`, and return
  `ClaudeAgentOptions(mcp_servers={"calculator": server},
  allowed_tools=["mcp__calculator__calculate"],
  system_prompt="Use the calculate tool to answer math questions.",
  model="claude-haiku-4-5")` (the cheap default model, per
  `shared/llm/pricing.py` and Ground Rule 8).
- `async def run_agent(question: str) -> str` -- call
  `query(prompt=question, options=build_options())`, iterate the returned
  async generator, and return the text of the final `AssistantMessage`
  (concatenate its `TextBlock` parts).

## Acceptance criteria

- The offline tests pass when run with `claude-agent-sdk` installed via the
  first command above: `_evaluate` handles arithmetic correctly and rejects
  non-arithmetic input; `build_options()` constructs without error and has
  the calculator tool wired in.
- The `live`-marked test (only run explicitly, with a real key) confirms
  `run_agent` answers "15 times 7, plus 3" correctly using the real model.

## Running the tests

```bash
uv run --with "claude-agent-sdk>=0.2.0" pytest curriculum/11-frameworks/labs/03-claude-agent-sdk/tests
LAB_TARGET=starter uv run --with "claude-agent-sdk>=0.2.0" pytest curriculum/11-frameworks/labs/03-claude-agent-sdk/tests
```
