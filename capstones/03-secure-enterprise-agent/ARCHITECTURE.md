# Architecture -- Secure enterprise agent

## Overview

```
  user_input
      │
      ▼
run_agent_with_approval() ──▶ client.complete(messages, tools=TOOLS)
      │                                    │
      │                          tool call decided
      │                                    ▼
      │                    is tool_call.name in REQUIRES_APPROVAL?
      │                         │                      │
      │                        yes                     no
      │                         ▼                      ▼
      │                 save_checkpoint()         dispatch(mcp_client, tool_call)
      │                 return "paused"                 │
      │                                                  ▼
      │                                          real MCP call, via
      │                                    async with Client(mcp) as mcp_client
      ▼
resume_after_approval(approved: bool)
      │
      ├─ approved=True  → dispatch() for real (still subject to the
      │                    tool's own channel allowlist -- see below)
      └─ approved=False → synthetic is_error ToolResult, never dispatched
```

## Design rationale

### Why MCP (not a plain Python function registry) for tool execution

Module 09's original approval-gate lab used a local `TOOL_REGISTRY` dict.
This capstone replaces it with a real `mcp.server.MCPServer` and
`mcp.Client` (Module 10), because an "enterprise agent" realistically
integrates with tools that live behind a protocol boundary (a real MCP
server run by a different team, a different process, potentially a
different machine) rather than plain in-process functions. The agent-side
contract (`ToolDefinition`/`ToolCall`/`ToolResult`) is unchanged -- only
`dispatch`'s implementation changed, from a dict lookup to a real
protocol call. This is a deliberate demonstration that Module 09's
approval-gate pattern composes cleanly with Module 10's protocol layer
without needing to redesign either.

### Why `raise ToolError`, not a plain exception, inside `mcp_server.py`

Verified directly against the installed `mcp` package (2026-09-22): a
plain exception raised inside an `@mcp.tool()`-decorated function is
caught by the server and replaced with a generic `"Error executing tool
X"` message -- the original message (e.g. the specific channel-allowlist
violation) is **not** propagated to the client. Raising
`mcp.server.mcpserver.exceptions.ToolError(message)` instead is what
actually carries the specific message through to `result.content[0].text`
on the client side. This was discovered by installing the real package and
testing both paths directly (the same install-and-inspect discipline used
throughout Modules 10, 11, and 20) -- not assumed from the pattern used in
Module 18's plain-Python (non-MCP) `send_email` example, which had no such
wrapping to work around.

### Why the channel allowlist lives in the MCP tool, not in the agent's approval logic

This is Module 18 lesson 02's core point, applied through a protocol
boundary: the approval gate (a human saying "yes, send this") and the
allowlist (a mechanical check on *what* can be sent) are two independent
layers. A human approving a request doesn't bypass the allowlist -- the
tool enforces its own boundary regardless of what upstream (the model's
decision, or a human's approval) led to the call. `THREAT_MODEL.md`'s core
scenario proves this composition holds.

### Why the checkpoint is tested against a freshly loaded module and a freshly started MCP server

A real production restart doesn't preserve any Python object identity --
only the checkpoint file on disk survives. Testing resume against the
*same* in-memory `secure_agent`/`mcp_server` module instances used for the
pause would pass even if the implementation accidentally depended on some
in-memory state the checkpoint file doesn't actually capture. Loading
fresh module instances (a fresh `mcp.server.MCPServer`, fresh
`_SENT_ANNOUNCEMENTS`) for the resume step is what makes this test a
genuine proof of correct checkpointing, not an accidental pass.

## What this capstone does not attempt

`lookup_record`'s data (`_RECORDS`) is a small, hardcoded in-memory dict --
a real enterprise integration would connect to an actual HR/directory
system, which introduces its own authentication and data-freshness
concerns out of scope for demonstrating this capstone's actual subject:
the approval-gate + MCP + permission-boundary composition.
