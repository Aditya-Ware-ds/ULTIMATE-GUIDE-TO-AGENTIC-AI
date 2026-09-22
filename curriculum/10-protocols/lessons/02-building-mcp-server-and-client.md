# Building an MCP server and client

**Last verified:** 2026-09-22 against `mcp` package version 2.2.0 (installed and
executed directly to confirm this exact code runs, not just read from docs).
**Difficulty:** ★★★★★ · **Time:** ~1.5 hours

## Learning objectives

- Build a minimal MCP server exposing a tool, using the current Python SDK.
- Build an MCP client that connects to a server and calls its tool, both over stdio (a real subprocess) and in-process (for fast tests).
- Explain why in-process connection is useful for testing even though real deployments use stdio or HTTP.

## Intuition

The Python SDK's current high-level API (`mcp.server.MCPServer`) looks almost
exactly like Module 03's tool definitions -- a decorator over a plain Python
function -- because that's deliberate: MCP wants defining a tool to feel as
close to "just write a function" as possible, and handles the protocol
plumbing (JSON-RPC messages, schema generation from your function's type
hints) for you.

## The concept

### A minimal server

```python
from mcp.server import MCPServer

mcp = MCPServer("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


if __name__ == "__main__":
    mcp.run()  # defaults to stdio transport
```

`mcp.tool()` inspects `add`'s type hints and docstring to generate the JSON
Schema tool definition automatically (Module 03's `ToolDefinition.parameters`,
but generated for you instead of hand-written). `mcp.run()` defaults to the
`stdio` transport -- the server reads requests from stdin and writes responses
to stdout, which is exactly what lets a client spawn it as a subprocess and
talk to it without any network setup.

### A client over stdio (a real subprocess)

```python
import asyncio
from mcp import Client, StdioServerParameters


async def main() -> None:
    params = StdioServerParameters(command="python", args=["server.py"])
    async with Client(params) as client:
        tools = await client.list_tools()
        result = await client.call_tool("add", {"a": 10, "b": 20})
        print(result.content)  # [TextContent(type='text', text='30', ...)]


asyncio.run(main())
```

`Client` spawns `python server.py` as a child process and speaks MCP over its
stdin/stdout -- this is a real, separate process, exactly like a production
deployment where the server might be written and run independently of the
client.

### A client connected in-process (useful for tests)

```python
from mcp.server import MCPServer
from mcp import Client

mcp = MCPServer("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


async def main() -> None:
    async with Client(mcp) as client:  # the MCPServer instance directly, no subprocess
        result = await client.call_tool("add", {"a": 2, "b": 3})
        print(result.content)  # [TextContent(type='text', text='5', ...)]
```

`Client` accepts an `MCPServer` instance directly (not just connection
parameters) for exactly this reason: fast, deterministic, no-subprocess
testing. This is what this module's lab uses for its automated tests -- the
protocol behavior is identical either way, only the transport differs.

## Deeper: schema generation from type hints is convenient and has limits

Auto-generating a tool's JSON Schema from Python type hints (as `mcp.tool()`
does) saves the hand-writing Module 03 required, but it inherits Python's type
system's limits -- there's no way to auto-generate an `enum` constraint or a
detailed per-field description purely from a type hint. `mcp.tool()` also
reads your function's docstring for the tool's description, which is exactly
why Module 03's lesson on writing clear, model-facing descriptions still
applies -- the docstring you write *is* what the model sees, auto-generated
schema or not.

## When not to use this

Don't wrap trivial, single-use, single-agent tools in a full MCP server
process (lesson 01's point) -- the subprocess/protocol overhead only pays off
when the tool needs to be shared across independently-built clients.

## Common mistakes

- Forgetting `if __name__ == "__main__": mcp.run()` in a server meant to be
  spawned as a subprocess -- without it, running the script does nothing (the
  decorators just registered tools; nothing serves them).
- Assuming `Client(mcp_server_instance)` (in-process) and
  `Client(StdioServerParameters(...))` (subprocess) require different calling
  code beyond construction -- `list_tools()`/`call_tool()` work identically
  either way, which is exactly why the in-process form is safe to use for
  tests of the same code path a subprocess deployment would exercise.
- Not handling `result.content` correctly -- it's a list of content blocks
  (usually `TextContent`), not a plain string; check `structured_content` if
  you need the raw typed return value instead of text.

## Key takeaways

- `mcp.server.MCPServer` + `@mcp.tool()` auto-generates a JSON Schema tool definition from your function's type hints and docstring.
- `mcp.run()` defaults to stdio transport, letting any client spawn your server as a subprocess with no network setup.
- `Client` can connect to a real subprocess (`StdioServerParameters`) or directly to an in-process `MCPServer` instance -- the same protocol behavior either way, which is why tests can use the faster in-process form.

## Lab

[`labs/01-mcp-server-and-client/`](../labs/01-mcp-server-and-client/README.md)
