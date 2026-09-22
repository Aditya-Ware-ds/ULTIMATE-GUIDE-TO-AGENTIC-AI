# Module 12 -- Multi-agent systems

**Difficulty:** ★★★★★ · **Time estimate:** 7-9 hours

## Objectives

By the end of this module you can:

- Explain and implement the supervisor-worker topology, building directly on Module 08's orchestrator-workers pattern.
- Explain hierarchical, handoff, swarm, and debate topologies and when each fits.
- Name concrete multi-agent failure modes and design against them.
- Decide when multi-agent is the wrong answer to a problem a single agent could solve.

## Prerequisites

[Module 11 -- Frameworks](../11-frameworks/README.md)

## Why this module exists

Module 08's orchestrator-workers pattern was multi-agent systems in
miniature -- this module gives that idea its full name and a fuller
vocabulary (topologies, failure modes), and is the last stop before Level 4's
specialized agents. Every framework in Module 11 has some multi-agent
feature (CrewAI's crews, LangGraph's sub-graphs, Google ADK's agent
composition); this module builds the underlying pattern by hand first, per
Ground Rule 6, so you understand exactly what those features are automating.

## Contents

- [`lessons/01-topologies.md`](lessons/01-topologies.md)
- [`lessons/02-failure-modes.md`](lessons/02-failure-modes.md)
- [`lessons/03-when-multi-agent-is-a-mistake.md`](lessons/03-when-multi-agent-is-a-mistake.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-supervisor-worker/`](labs/01-supervisor-worker/) -- a hand-rolled supervisor with 3 specialized workers
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

Level 3 is complete after this module. See [`projects/`](../../projects/README.md)
for "MCP server for a real public API" and "multi-agent content pipeline,"
then [Module 13 -- Coding agents](../13-coding-agents/README.md) (Level 4 begins).
