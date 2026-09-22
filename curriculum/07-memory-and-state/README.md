# Module 07 -- Memory & state

**Difficulty:** ★★★★☆ · **Time estimate:** 5-7 hours

## Objectives

By the end of this module you can:

- Distinguish short-term memory (this conversation) from long-term memory (across conversations), and episodic memory (specific past events) from semantic memory (general learned facts).
- Explain where memory can live and the trade-offs between keeping it in-context versus in an external store.
- Implement checkpointing: serializing an agent's state so a killed or restarted process can resume correctly.

## Prerequisites

[Module 06 -- Retrieval & agentic RAG](../06-retrieval-and-rag/README.md)

## Why this module exists

Everything from Module 04 onward has lived and died with a single Python
process's `messages` list. Real agents need to survive process restarts
(a deploy, a crash, a worker recycling), and some need to remember things
*across* separate conversations, not just within one. This module is where
"agent state" becomes something durable rather than something that only
exists in memory. It's easy to conflate with Module 05's compaction or
Module 06's retrieval -- this module is explicit about what's actually new:
persisting an agent's *own* state across process/run boundaries, not shrinking
a live conversation or finding documents.

## Contents

- [`lessons/01-memory-types.md`](lessons/01-memory-types.md)
- [`lessons/02-memory-stores.md`](lessons/02-memory-stores.md)
- [`lessons/03-checkpointing-and-resumption.md`](lessons/03-checkpointing-and-resumption.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-resumable-agent/`](labs/01-resumable-agent/) -- an agent that checkpoints its state and resumes correctly after a simulated crash
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 08 -- Planning & reasoning patterns](../08-planning-and-reasoning/README.md)
