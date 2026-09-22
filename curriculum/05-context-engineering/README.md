# Module 05 -- Context engineering

**Difficulty:** ★★★★☆ · **Time estimate:** 5-7 hours

## Objectives

By the end of this module you can:

- Enumerate everything that competes for space in an agent's context window and make deliberate decisions about what belongs there.
- Design tool descriptions and system prompts as context-budget items, not free text.
- Implement a compaction strategy that keeps a long-running agent under a token budget.
- Explain context rot (including "lost in the middle") and why a bigger context window doesn't make it go away.

## Prerequisites

[Module 04 -- The agent loop from scratch](../04-agent-loop/README.md)

## Why this module exists

Module 04's agent loop appends to `messages` forever. Left unchecked, that's a
correctness bug waiting to happen: conversations grow past context limits,
costs balloon (Module 02's stateless-resend point), and -- as this module
covers -- quality silently degrades well before you hit any hard limit at all.
Context engineering is the discipline of treating the context window as a
scarce, actively-managed resource, which is exactly what a production agent
loop needs on top of Module 04's mechanics.

## Contents

- [`lessons/01-what-goes-in-context.md`](lessons/01-what-goes-in-context.md)
- [`lessons/02-compaction-and-summarization.md`](lessons/02-compaction-and-summarization.md)
- [`lessons/03-context-rot.md`](lessons/03-context-rot.md)
- [`examples/`](examples/) -- small runnable demos (against the mock provider -- no API key needed)
- [`labs/01-compacting-agent/`](labs/01-compacting-agent/) -- add a compaction strategy to an agent loop and prove it survives a long trace
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 06 -- Retrieval & agentic RAG](../06-retrieval-and-rag/README.md)
