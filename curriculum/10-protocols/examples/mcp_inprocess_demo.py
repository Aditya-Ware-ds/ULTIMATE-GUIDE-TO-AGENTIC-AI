"""Run: uv run python curriculum/10-protocols/examples/mcp_inprocess_demo.py

A minimal MCP server and an in-process client calling its tool -- no
subprocess, no network. Verified to run against `mcp` package 2.2.0. See
lessons/02-building-mcp-server-and-client.md.
"""

from __future__ import annotations

import asyncio

from mcp import Client
from mcp.server import MCPServer

mcp = MCPServer("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


async def main() -> None:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        print("Tools exposed by the server:", [t.name for t in tools.tools])

        result = await client.call_tool("add", {"a": 2, "b": 3})
        print("call_tool('add', {'a': 2, 'b': 3}) ->", result.content)
        print("structured_content:", result.structured_content)


if __name__ == "__main__":
    asyncio.run(main())
