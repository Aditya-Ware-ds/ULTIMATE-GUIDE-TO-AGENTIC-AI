"""Run: uv run python curriculum/10-protocols/examples/mcp_stdio_client_demo.py

Spawns mcp_stdio_server.py as a real subprocess and calls its tool over
stdio -- a real, separate-process MCP connection, not the in-process
shortcut used for tests. See lessons/02-building-mcp-server-and-client.md.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters

SERVER_SCRIPT = Path(__file__).parent / "mcp_stdio_server.py"


async def main() -> None:
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER_SCRIPT)])
    async with Client(params) as client:
        tools = await client.list_tools()
        print("Tools exposed by the subprocess server:", [t.name for t in tools.tools])

        result = await client.call_tool("add", {"a": 10, "b": 20})
        print("call_tool('add', {'a': 10, 'b': 20}) ->", result.content)


if __name__ == "__main__":
    asyncio.run(main())
