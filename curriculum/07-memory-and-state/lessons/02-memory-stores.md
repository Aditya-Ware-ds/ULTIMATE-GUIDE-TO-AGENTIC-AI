# Memory stores

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45 minutes

## Learning objectives

- Explain the trade-off between in-context memory and an external memory store.
- Design a minimal external memory store for a semantic long-term fact.
- Know what "memory" implementations across current frameworks are actually doing underneath.

## Intuition

Once you've decided you need long-term memory (lesson 01), you need somewhere
to put it. The two broad options: keep relevant facts *in the context window*
every time (simple, but competes with everything else in context -- Module 05)
or keep them in an *external store* (a file, a database, a vector index) and
retrieve only what's relevant into context when needed (Module 06's retrieval
machinery, applied to an agent's own memory instead of a document corpus).

## The concept

### In-context memory: the simplest option

```python
system_prompt = f"""You are a helpful assistant.
Known facts about this user: {user_facts_summary}
"""
```

If the total set of long-term facts you'd ever need is small (a handful of
preferences), just always include them in the system prompt. This is simple
and requires no extra infrastructure -- but it doesn't scale past a small,
fairly static fact set, per Module 05's context-budget lesson.

### External memory: a minimal store

```python
import json
from pathlib import Path


def load_memory(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_memory(path: Path, memory: dict) -> None:
    path.write_text(json.dumps(memory, indent=2))


def remember_fact(path: Path, key: str, value: str) -> None:
    memory = load_memory(path)
    memory[key] = value
    save_memory(path, memory)
```

A real production system would use an actual database (not a JSON file) and
likely combine this with retrieval (Module 06) once the memory store grows
past what fits comfortably in a prompt -- but the *shape* of the problem is
the same at any scale: write facts somewhere durable, read back only what's
relevant for the current context.

### What frameworks' "memory" features are actually doing

When Module 11's frameworks offer a built-in "memory" module, it's implementing
one of these two patterns (or a hybrid) underneath -- some combination of
"keep recent turns in context" (short-term, Module 04/05's territory) and
"store and retrieve facts from an external store" (long-term, this lesson).
Nothing here is magic; recognizing the pattern lets you evaluate whether a
framework's memory feature actually fits your use case, or is solving a
different problem than the one you have.

## Deeper: memory stores are a data-design problem, not just an engineering one

What you choose to store (raw conversation excerpts vs. distilled facts),
how you key it (per-user? per-topic?), and when you write to it (every turn?
only on explicit signals?) are design decisions with real consequences for
cost, staleness, and privacy -- not just implementation details. A memory
store that writes everything, indiscriminately, becomes exactly the kind of
noisy, low-signal content that Module 05's context-rot lesson warns against
once it's retrieved back into context.

## When not to use this

Don't build a general-purpose external memory store for a system with a small,
fixed set of long-term facts that fit comfortably in a system prompt --
in-context memory is simpler and sufficient. Reach for an external store when
the fact set grows large enough that including all of it would meaningfully
compete for context budget (Module 05), or when facts need to be shared/queried
across many separate conversations or users.

## Common mistakes

- Storing raw conversation transcripts as "memory" and re-summarizing them on
  every read, instead of distilling and storing the summary once (semantic
  memory, lesson 01) -- repeatedly paying the summarization cost for the same
  information.
- No expiry or update strategy -- a memory store that only ever appends can
  accumulate stale or contradictory facts over time with nothing correcting
  them.
- Treating a framework's "memory" feature as a black box without checking
  whether it's actually solving the memory-type problem you have (lesson 01) --
  it may be doing short-term context management when you needed long-term
  storage, or vice versa.

## Key takeaways

- In-context memory is simplest and fine for a small, fairly static fact set; external stores are needed once that set grows or must be shared across conversations.
- A minimal external memory store is just durable read/write of key facts -- the same shape scales conceptually from a JSON file to a real database.
- Framework "memory" features implement these same two patterns underneath -- know which one you need before trusting a built-in default.

## Lab

[`labs/01-resumable-agent/`](../labs/01-resumable-agent/README.md)
