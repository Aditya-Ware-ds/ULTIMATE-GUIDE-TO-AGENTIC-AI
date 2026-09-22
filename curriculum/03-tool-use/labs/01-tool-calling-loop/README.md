# Lab 03.01 -- Calculator + weather tool-calling loop

**Difficulty:** ★★★★☆ · **Time:** ~2-3 hours

## Task

Build a small, hand-written (no framework) tool-calling loop with two tools: a
safe arithmetic calculator and a fake weather lookup. The loop should keep
calling the model, dispatching any tool calls, and feeding results back, until
the model responds with plain text (or a step budget is exhausted).

No API key needed -- everything is tested against `shared.llm.get_client("mock")`.

## Files

- `starter/tools.py` -- skeleton with six functions/classes to implement
- `solution/tools.py` -- complete reference implementation
- `tests/` -- tests that exercise both

## Requirements

Implement these in `starter/tools.py`:

- `def calculate(expression: str) -> float` -- safely evaluate a basic arithmetic
  expression (`+`, `-`, `*`, `/`, parentheses, numbers) using Python's `ast`
  module -- **do not use `eval()`** (this is a deliberate security lesson: never
  run untrusted, model-produced strings through `eval()`). Raise `ValueError` for
  anything that isn't a valid arithmetic expression (e.g. a name, a function
  call, a string literal).
- `def get_weather(city: str, unit: str = "celsius") -> dict` -- return canned
  weather data from a small hardcoded lookup table (at least `"Paris"` and
  `"Tokyo"`). Raise `ValueError` with a clear message for a city not in the
  table.
- `TOOL_DEFINITIONS: list[ToolDefinition]` -- module-level list with schemas for
  both tools (see `lessons/01-tool-schemas.md` for the shape).
- `TOOL_REGISTRY: dict[str, Callable]` -- module-level dict mapping `"calculate"`
  and `"get_weather"` to the functions above.
- `def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult`
  -- as covered in `lessons/02-dispatch-and-execution.md`: unknown tool name and
  any exception during execution both become an `is_error=True` `ToolResult`
  with an actionable message, never an unhandled exception.
- `async def run_tool_loop(client: LLMClient, system_prompt: str, user_input: str, max_steps: int = 5) -> str`
  -- send the user's message with `tools=TOOL_DEFINITIONS`; while the response
  has tool calls, dispatch each one, append the results as `tool`-role messages,
  and call the model again; once the response has no tool calls, return its text.
  If `max_steps` is reached without a final text response, return a clear
  message saying so (don't raise).

## Acceptance criteria

- All tests in `tests/` pass against your `starter/tools.py`.
- `calculate("2 + 2 * 3")` returns `8`; `calculate("__import__('os')")` (or any
  non-arithmetic input) raises `ValueError`, never executes anything.
- `dispatch` never raises -- every failure path returns an `is_error=True`
  `ToolResult`.
- `run_tool_loop` correctly handles a multi-step exchange (tool call -> result ->
  another tool call -> result -> final text) using the mock provider's scripted
  turns, and stops at `max_steps` without raising if the model never stops
  calling tools.

## Hints

- For `calculate`, parse with `ast.parse(expression, mode="eval")`, then walk the
  resulting `ast.Expression.body` recursively, allowing only `ast.BinOp` with
  `ast.Add`/`ast.Sub`/`ast.Mult`/`ast.Div`, `ast.UnaryOp` with `ast.USub`, and
  `ast.Constant` nodes holding `int`/`float`. Reject everything else.
- `run_tool_loop`'s message list needs a `Message(role=Role.TOOL, tool_result=result)`
  entry per dispatched tool call before the next `client.complete(...)` call.

## Running the tests

```bash
uv run pytest curriculum/03-tool-use/labs/01-tool-calling-loop/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/03-tool-use/labs/01-tool-calling-loop/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 04 -- The agent loop from scratch](../../../04-agent-loop/README.md)
