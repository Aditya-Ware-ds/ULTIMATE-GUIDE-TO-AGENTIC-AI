"""A standalone MCP server, meant to be spawned as a subprocess (see
mcp_stdio_client_demo.py). Run directly it does nothing until a client
connects and speaks MCP to it over stdin/stdout.
"""

from __future__ import annotations

from mcp.server import MCPServer

mcp = MCPServer("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


if __name__ == "__main__":
    mcp.run()  # defaults to stdio transport
