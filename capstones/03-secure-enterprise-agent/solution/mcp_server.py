"""Capstone 3: real MCP server exposing enterprise tools. Reference
solution. See ../README.md and ../ARCHITECTURE.md.

Verified against the installed `mcp` package (2026-09-22): raising
mcp.server.mcpserver.exceptions.ToolError (not a plain ValueError)
inside a tool is what propagates a specific error message back to the
client -- a plain exception is caught and replaced with a generic
"Error executing tool X" message instead.
"""

from __future__ import annotations

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("enterprise-agent-tools")

_RECORDS: dict[str, str] = {
    "emp-001": "Alice Smith, Engineering, Senior Software Engineer",
    "emp-002": "Bob Jones, Sales, Account Executive",
}

ANNOUNCEMENT_CHANNEL_ALLOWLIST: frozenset[str] = frozenset({"general", "engineering"})
_SENT_ANNOUNCEMENTS: list[dict] = []


@mcp.tool()
def lookup_record(record_id: str) -> str:
    """Look up an internal employee record by id."""
    if record_id not in _RECORDS:
        raise ToolError(f"No record found for id: {record_id!r}")
    return _RECORDS[record_id]


@mcp.tool()
def send_announcement(channel: str, message: str) -> str:
    """Send an internal announcement to a channel."""
    if channel not in ANNOUNCEMENT_CHANNEL_ALLOWLIST:
        raise ToolError(f"Refusing to send to {channel!r}: not on the approved channel allowlist")
    _SENT_ANNOUNCEMENTS.append({"channel": channel, "message": message})
    return f"Announcement sent to {channel}"


if __name__ == "__main__":
    mcp.run()
