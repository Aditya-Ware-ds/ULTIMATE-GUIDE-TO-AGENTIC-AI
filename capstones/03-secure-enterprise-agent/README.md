# Capstone 3 -- Secure enterprise agent

**Difficulty:** ★★★★★ · **Time:** ~4-6 hours
**Draws on:** Module 09 (HITL), Module 10 (MCP), Module 18 (security)

## Spec

Build an enterprise assistant agent with real MCP tools (a record lookup
and an internal announcement tool), a human-approval gate in front of the
consequential tool, and a genuine red-team report proving the tool's own
permission boundary holds even if a human approves a bad request -- with
MCP tools, human approval gates, and a red-team report, per the original
curriculum plan's capstone requirement.

No API key needed -- tested against `shared.llm.get_client("mock")` and a
real, in-process MCP server/client (Module 10's pattern). See
[`ARCHITECTURE.md`](ARCHITECTURE.md) for design rationale,
[`THREAT_MODEL.md`](THREAT_MODEL.md) for the full red-team report, and
[`DEPLOY.md`](DEPLOY.md) for how this would be deployed.

## Files

- `starter/mcp_server.py`, `starter/secure_agent.py` -- skeletons (only `secure_agent.py` has gaps -- `mcp_server.py` is given, it's Module 10 review)
- `solution/mcp_server.py`, `solution/secure_agent.py` -- complete reference implementation
- `tests/` -- tests including the core red-team and kill-and-resume scenarios

## Requirements

### `mcp_server.py` (given, no gaps -- read it before starting)

A real `mcp.server.MCPServer` exposing `lookup_record(record_id) -> str`
(read-only) and `send_announcement(channel, message) -> str` (checks
`channel` against `ANNOUNCEMENT_CHANNEL_ALLOWLIST`, raising
`mcp.server.mcpserver.exceptions.ToolError` -- not a plain exception, see
`ARCHITECTURE.md` for why -- if it isn't allowlisted).

### `secure_agent.py`

Implement, building on Module 09's approval-gate pattern
(`message_to_dict`/`from_dict`, `save_checkpoint`/`load_checkpoint`,
`AgentResult` are given, unchanged in shape):

- `async def dispatch(mcp_client, tool_call: ToolCall) -> ToolResult` --
  call the real MCP tool and wrap its result/error as a `ToolResult` (see
  the starter's docstring for the exact contract).
- `async def _continue_loop(client, mcp_client, checkpoint_path, messages, step, max_steps) -> AgentResult`
  -- the approval-gate loop: pause (save checkpoint, don't dispatch) on any
  tool in `REQUIRES_APPROVAL`; dispatch and continue otherwise.
- `async def run_agent_with_approval(client, mcp_client, checkpoint_path, user_input, max_steps=10) -> AgentResult`
- `async def resume_after_approval(client, mcp_client, checkpoint_path, approved, max_steps=10) -> AgentResult`

## Acceptance criteria

- All tests in `tests/` pass against your `starter/secure_agent.py`.
- `send_announcement` is never dispatched before approval -- verified via
  `mcp_server_module._SENT_ANNOUNCEMENTS` staying empty at the `"paused"` state.
- **The red-team test passes**: an approved request to a non-allowlisted
  channel is still blocked at the tool layer -- `_SENT_ANNOUNCEMENTS` stays
  empty even when `resume_after_approval(..., approved=True)` is called.
- **The kill-and-resume test passes**: a checkpoint written by one
  `run_agent_with_approval` call is correctly resumed by
  `resume_after_approval` called against a **freshly loaded** agent module
  and a **freshly started** MCP server -- proving the checkpoint file on
  disk carries everything needed, not any in-memory state.

## Running the tests

```bash
uv run pytest capstones/03-secure-enterprise-agent/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest capstones/03-secure-enterprise-agent/tests
```

## Next

This is the last capstone. See [PROGRESS.md](../../PROGRESS.md) for the
final pass that closes out the whole curriculum.
