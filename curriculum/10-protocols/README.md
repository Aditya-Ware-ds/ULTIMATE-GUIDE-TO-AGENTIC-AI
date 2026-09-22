# Module 10 -- Protocols

**Difficulty:** ★★★★☆ · **Time estimate:** 7-9 hours

## Objectives

By the end of this module you can:

- Explain what MCP standardizes and why it exists, and build both an MCP server and an MCP client against the current spec.
- Explain what A2A standardizes (agent-to-agent task handoff) and implement a minimal task lifecycle.
- Explain what Agent Skills standardizes (portable, on-demand agent capabilities) and package a tool as a `SKILL.md`.
- Know which of these three problems each protocol solves, so you reach for the right one.

## Prerequisites

Level 2 (Modules 07-09) and the "customer-support agent with escalation" project.

## Why this module exists

Every tool, memory store, and multi-step pattern you've built so far has been
wired up by hand, specific to this repo. Real agent ecosystems need
*standards* so a tool built by one team works with an agent built by another,
without custom integration code every time. This module covers the three
current standards that matter most: MCP (how an agent discovers and calls
tools/resources from any compliant server), A2A (how one agent hands work to
another), and Agent Skills (how an agent loads portable, on-demand
capabilities). Module 11 then shows how full frameworks build on top of these
same standards.

## Contents

- [`lessons/01-mcp-overview-and-architecture.md`](lessons/01-mcp-overview-and-architecture.md)
- [`lessons/02-building-mcp-server-and-client.md`](lessons/02-building-mcp-server-and-client.md)
- [`lessons/03-a2a-and-agent-skills.md`](lessons/03-a2a-and-agent-skills.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-mcp-server-and-client/`](labs/01-mcp-server-and-client/) -- build a real MCP server wrapping Module 03's tools, and a real client that calls it
- [`labs/02-a2a-task-handoff/`](labs/02-a2a-task-handoff/) -- a minimal two-agent task handoff following A2A's task lifecycle
- [`labs/03-agent-skill-package/`](labs/03-agent-skill-package/) -- package a tool as a validated `SKILL.md`
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 11 -- Frameworks](../11-frameworks/README.md)
