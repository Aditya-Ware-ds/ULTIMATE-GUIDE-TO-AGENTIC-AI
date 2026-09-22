# Lab 17.01 -- Traced ReAct agent

**Difficulty:** ★★★★☆ · **Time:** ~2 hours

## Task

Instrument a ReAct agent (Module 04's loop, using a `calculate` tool) with
`shared/tracing/`'s span context managers, then write functions to replay a
trace as a readable timeline and summarize its token usage. No API key
needed -- tested against `shared.llm.get_client("mock")`.

## Files

- `starter/traced_agent.py` -- skeleton with the pieces to implement
- `solution/traced_agent.py` -- complete reference implementation
- `tests/` -- tests that exercise span creation/nesting, replay, and usage summary

## Requirements

Implement these in `starter/traced_agent.py` (the `calculate` tool,
`dispatch`, and `_infer_provider_name` are already given):

- `async def run_traced_agent(client, user_input: str, max_steps: int = 6) -> str`
  -- Module 04's ReAct loop shape, wrapped in tracing spans:
  - the whole run in `invoke_agent_span("react-agent", **{"gen_ai.request.max_steps": max_steps})`
  - each model call in `chat_span(model=client.default_model, provider=_infer_provider_name(client))`,
    recording `gen_ai.usage.input_tokens`/`gen_ai.usage.output_tokens` on the
    span via `span.set_attribute(...)` once the response is known
  - each tool call in `execute_tool_span(tool_call.name)`
- `def replay_trace(spans) -> str` -- reconstruct a chronological, indented
  timeline from exported spans (see lessons/02-replaying-failed-runs.md):
  sort by `start_time`, indent by walking each span's `parent` chain, and
  print each span's name, duration in milliseconds, and attributes.
- `def summarize_usage(spans) -> dict` -- return
  `{"chat_calls": ..., "input_tokens": ..., "output_tokens": ...}` by
  summing the `gen_ai.usage.*` attributes across every span whose name
  starts with `"chat "`.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/traced_agent.py`.
- A natural-completion run (no tool calls) produces an `invoke_agent
  react-agent` span and at least one `chat` span.
- A tool-calling run produces an `execute_tool calculate` span nested (via
  the parent chain) under the `invoke_agent react-agent` span.
- Every `chat` span has `gen_ai.usage.input_tokens`/`gen_ai.usage.output_tokens`
  recorded once the model call completes.
- `replay_trace` orders spans chronologically and indents children one
  level under their parent.
- `summarize_usage` correctly sums token counts across multiple `chat` spans.

## Running the tests

```bash
uv run pytest curriculum/17-observability-and-debugging/labs/01-traced-react-agent/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/17-observability-and-debugging/labs/01-traced-react-agent/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 18 -- Security & safety](../../../18-security-and-safety/README.md)
