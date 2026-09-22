# MCP overview and architecture

**Last verified:** 2026-09-22 (spec 2026-07-28; `mcp` Python package 2.2.0)
**Difficulty:** ★★★★☆ · **Time:** ~1 hour

## Learning objectives

- Explain what problem MCP (Model Context Protocol) solves and why it exists.
- Name the three architectural roles (host, client, server) and what each does.
- Explain what a server exposes (tools, resources, prompts) at a conceptual level.

## Intuition

Every tool you've built so far (Modules 03-09) was wired directly into your
own agent loop's code -- `TOOL_REGISTRY` was a Python dict you controlled. That
doesn't scale across organizations: if a company wants to expose "our
inventory system" as a tool any agent can use, hand-wiring custom integration
code for every possible agent framework is enormous duplicated effort. **MCP**
standardizes the wire protocol between an agent and a tool/data provider, the
same way HTTP standardizes communication between a browser and any web
server, regardless of who wrote either side.

## The concept

### The three roles

- **Host** -- the application the user interacts with (an IDE, a chat app, your
  own agent program). The host embeds one or more clients.
- **Client** -- lives inside the host, maintains a 1:1 connection to exactly
  one server, and translates between the host's needs and that server's
  protocol messages.
- **Server** -- a separate process (or remote service) that exposes
  capabilities: tools (callable functions, like Module 03's), resources (data
  the agent can read, like a file or a database record), and prompts (reusable
  prompt templates). A server has no knowledge of which host or which model is
  using it.

```
Host (your agent program)
  └── Client ──(MCP protocol)──> Server (exposes tools/resources/prompts)
```

One host can run multiple clients, each talking to a different server --  this
is how an agent ends up with tools from many independent sources without
custom integration code for each one.

### What a server exposes

- **Tools** -- the same concept as Module 03's `ToolDefinition`, but described
  and called over the MCP wire protocol instead of your own in-process dict.
- **Resources** -- readable data the client can fetch (e.g. `file:///...`,
  `greeting://{name}` -- URI-addressed content, parameterizable via templates).
- **Prompts** -- reusable, parameterized prompt templates a client can request
  and fill in, so prompt engineering for a specific capability can live with
  the server that knows the domain, not duplicated in every host.

### The current spec: 2026-07-28

As of 2026-09-22, the current MCP specification is dated 2026-07-28, a major
revision that moved to a **stateless protocol core** (no more required
session affinity between requests), added multi-round-trip requests and
header-based routing, and introduced a formal extensions framework. The
Python SDK (package `mcp`, version 2.x) was reworked to match. This lesson's
and the lab's code target that current SDK.

## Deeper: MCP standardizes access, not agent behavior

MCP says nothing about *how* an agent decides which tool to call or when --
that's still Module 03/04's territory (the agent loop, tool selection). MCP
only standardizes *how a client talks to a server* to discover and invoke
what's available. This separation matters: MCP works underneath any agent
loop shape (step-by-step, plan-and-execute, whatever Module 08 covered), it
doesn't replace or dictate any of it.

## When not to use this

Don't reach for a full MCP server for a tool that only your own single agent
program will ever call -- the protocol overhead (a separate process, a
transport layer) is unnecessary machinery for a Python function you can put
directly in a `TOOL_REGISTRY` dict (Module 03). MCP earns its complexity when
a capability needs to be shared across multiple, independently-built agents
or hosts.

## Common mistakes

- Conflating "tool" (an MCP server capability) with "agent" -- an MCP server is
  not itself an agent; it has no model, no loop, no decision-making. It's a
  capability provider an agent's client connects to.
- Assuming MCP dictates the agent loop or model choice -- it doesn't; those
  remain entirely up to the host/client side.
- Building against an outdated pre-2026-07-28 mental model of the protocol
  (session-based, not stateless) -- if you learned MCP from older material,
  re-check current docs; this is exactly the kind of fast-moving spec Ground
  Rule 1 warns about.

## Key takeaways

- MCP standardizes how a client discovers and calls tools/resources/prompts from any compliant server -- the same relationship HTTP has to browsers and web servers.
- Host embeds clients; each client talks to exactly one server; servers expose tools, resources, and prompts.
- The current spec (2026-07-28) is stateless-core; verify you're not working from stale, pre-rework documentation.

## Lab

[`labs/01-mcp-server-and-client/`](../labs/01-mcp-server-and-client/README.md)
