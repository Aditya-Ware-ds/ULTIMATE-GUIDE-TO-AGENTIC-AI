# Deploy guide -- Secure enterprise agent

Design sketch applying Module 19's patterns to this agent -- no new
runnable code (reuses Module 19's already-tested service/idempotency
mechanics by reference).

## Wrapping the agent as a service, with a real approval UI

`POST /requests` starts `run_agent_with_approval` and returns either a
`"done"` result or a `"paused"` state with the pending tool call's details
-- exactly what a real approval UI would render for a human reviewer
(Module 09's HITL framing). `POST /requests/{id}/approve` and
`POST /requests/{id}/reject` call `resume_after_approval` with
`approved=True`/`False` respectively. The MCP server itself would run as
its own long-lived process (or a separate service entirely), with the
agent service holding a persistent `mcp.Client` connection to it -- this
capstone's in-process `Client(mcp)` testing pattern stands in for what
would be a real network connection to a separately deployed MCP server in
production.

## Idempotency for approval actions specifically

Module 19 lesson 02's idempotency pattern matters here in a specific way:
a human reviewer double-clicking "approve" (a slow UI, a network retry)
must not cause `send_announcement` to fire twice. An idempotency key tied
to the specific pending request ensures a repeated approval action returns
the already-completed result instead of dispatching the consequential tool
a second time -- arguably more important here than in Module 19's own
lab's example, since this specific tool's side effect (a real internal
announcement) is highly visible and embarrassing to duplicate.

## Checkpoint storage in production

This capstone's `save_checkpoint`/`load_checkpoint` write to a local JSON
file, fine for tests. A real deployment needs durable, shared storage (a
database row, not a local file) so the pause state survives a worker
process restart and is visible to whichever server instance eventually
receives the approval decision -- Module 19 lesson 01's "durable jobs"
point, applied specifically to the approval-gate checkpoint.

## Observability and audit logging

Every approval decision (who approved, when, what was approved) needs a
durable audit trail -- not just Module 17's operational tracing, but a
compliance-relevant record specific to an enterprise agent with real
side effects. This is a genuinely different (additional) concern from
Module 17's cost/latency-focused tracing: an audit log needs to answer "who
approved this and when," which a performance trace doesn't capture by
default and would need extending to record.

## Rate limiting and abuse prevention

Per Module 19 lesson 02's rate-limiting point, applied to a tool with real
organizational visibility: bound how many approval requests a single user
or agent session can generate in a given window, independent of whether
each individual request is legitimate -- a compromised or malfunctioning
upstream system generating a flood of plausible-looking approval requests
is itself a risk this agent's tool-level defenses alone don't address.
