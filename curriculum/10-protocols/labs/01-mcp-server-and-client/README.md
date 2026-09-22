# Lab 10.01 -- MCP server and client

**Difficulty:** ★★★★★ · **Time:** ~2-3 hours

## Task

Build a real MCP server wrapping Module 03's calculator and weather tools,
and a real MCP client that connects to it and calls both. Tests use the
in-process connection (`Client(mcp_server_instance)`) for speed and
determinism -- no subprocess, no network, no mock provider needed here (this
lab tests the protocol layer itself, not an LLM).

## Files

- `starter/server.py`, `starter/client.py` -- skeletons to implement
- `solution/server.py`, `solution/client.py` -- complete reference implementation
- `tests/` -- tests that exercise both

## Requirements

**`server.py`** -- build an `MCPServer` named `"agentic-ai-mastery-tools"` with:

- `def calculate(expression: str) -> float` -- reuse Module 03's `ast`-based
  safe evaluator (no `eval()`) as an `@mcp.tool()`.
- `def get_weather(city: str) -> str` -- a small canned lookup (reuse the
  `{"Paris": ..., "Tokyo": ...}` idea from Module 03/06's labs), raising
  `ValueError` for an unknown city, as an `@mcp.tool()`.
- Export the `MCPServer` instance as a module-level variable named `mcp`.

**`client.py`**:

- `async def list_available_tools(client) -> list[str]` -- return the names of
  every tool the connected server exposes.
- `async def call_calculate(client, expression: str) -> float` -- call the
  server's `calculate` tool and return the numeric result (parse it out of
  the response -- see hints).
- `async def call_get_weather(client, city: str) -> str` -- call the server's
  `get_weather` tool and return the text result.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/` files.
- `list_available_tools` returns exactly `["calculate", "get_weather"]` (order
  doesn't matter, but both must be present).
- `call_calculate` returns the correct numeric result for a valid expression.
- Calling `get_weather` with an unknown city surfaces as a tool error the
  client can detect (check `result.is_error` on the raw
  `client.call_tool(...)` response, or catch whatever your `call_get_weather`
  raises/returns -- your choice, document it in a docstring).

## Hints

- `mcp.tool()` reads your function's docstring for the tool's description --
  write a real one-liner, not a placeholder, per Module 03's lesson on
  descriptions.
- A tool's return value comes back as `result.content` (a list of content
  blocks, usually `TextContent` with a `.text` string) and, for tools with a
  scalar return type, also as `result.structured_content` (e.g.
  `{"result": 5.0}`) -- prefer `structured_content` when it's available; it
  avoids parsing text.
- For tests, construct the client with `Client(solution_or_starter_mcp_instance)`
  directly -- no `StdioServerParameters` needed.

## Running the tests

```bash
uv run pytest curriculum/10-protocols/labs/01-mcp-server-and-client/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/10-protocols/labs/01-mcp-server-and-client/tests
```

## Next

[`labs/02-a2a-task-handoff/`](../02-a2a-task-handoff/README.md)
