# Lab 04.01 -- ReAct agent for multi-hop questions

**Difficulty:** ★★★★☆ · **Time:** ~2-3 hours

## Task

Build a ReAct-style agent that answers multi-hop questions using a fake
`search` tool (a small hardcoded knowledge base) plus the `calculate` tool from
Module 03. "Multi-hop" means the answer requires chaining two or more tool
calls, where the second call's input depends on the first call's result --
exactly the pattern this module's lessons cover.

No API key needed -- tested entirely against `shared.llm.get_client("mock")`.

## Files

- `starter/agent.py` -- skeleton with the knowledge base, tools, and agent loop to implement
- `solution/agent.py` -- complete reference implementation
- `tests/` -- tests that exercise both

## Requirements

Implement these in `starter/agent.py`:

- `KNOWLEDGE_BASE: dict[str, str]` -- at least 4 entries covering a genuine
  2-hop chain, e.g. `{"capital of france": "Paris", "population of paris":
  "2.1 million", "capital of japan": "Tokyo", "population of tokyo": "14 million"}`
  (lowercase keys).
- `def search(query: str) -> str` -- look up `query.lower()` in
  `KNOWLEDGE_BASE`; raise `ValueError` with a clear message if not found.
- `SEARCH_TOOL: ToolDefinition` and `CALCULATE_TOOL: ToolDefinition` -- schemas
  for `search` and Module 03's `calculate` (you may import `calculate` from
  `curriculum.03_tool_use...` conceptually, but for this lab's independence,
  redefine a small `calculate(expression: str) -> float` locally using the same
  `ast`-based approach from Module 03 -- don't use `eval()`).
- `TOOL_REGISTRY: dict[str, Callable]` and `dispatch(tool_call, registry) -> ToolResult`
  -- same contract as Module 03's lab (unknown tool / execution error both
  become `is_error=True`, never raise).
- `async def run_react_agent(client: LLMClient, user_input: str, max_steps: int = 6) -> str`
  -- the full agent loop: system prompt instructing the model to reason before
  each tool call and give a final answer with no tool calls when done; loop
  calling the model, dispatching tool calls, and feeding results back; return
  the final text on natural completion, or a clear "stopped after N steps"
  message if `max_steps` is exhausted.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/agent.py`.
- `search` raises `ValueError` (not a silent empty result) for an unknown query.
- `run_react_agent` correctly handles a 2-hop scripted exchange (search -> search
  -> final answer) and a mixed exchange (search -> calculate -> final answer).
- `run_react_agent` stops cleanly at `max_steps` with a clear message, never
  raising or looping past the limit (same contract as Module 03/04's other
  loops).
- `dispatch` never raises, for both tools.

## Hints

- This lab's `calculate` can be a smaller copy of Module 03's -- you don't need
  every feature, just enough for simple two-operand expressions used in tests.
- Reuse the `Message`/`ToolResult` append pattern from Module 03's
  `run_tool_loop` and Module 04's lesson 1 example almost verbatim -- the loop
  structure hasn't changed, only the tools and system prompt have.

## Running the tests

```bash
uv run pytest curriculum/04-agent-loop/labs/01-react-agent/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/04-agent-loop/labs/01-react-agent/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 05 -- Context engineering](../../../05-context-engineering/README.md)
