# Memory types

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45 minutes

## Learning objectives

- Distinguish short-term from long-term memory in an agent system.
- Distinguish episodic from semantic memory, and know which patterns from earlier modules already are which.
- Recognize which memory type a given agent requirement actually needs, instead of reaching for "add more memory" generically.

## Intuition

"Memory" is an overloaded word once you're building agents -- it can mean the
current conversation, a summary of a past conversation, a specific fact a user
told the agent last week, or a general pattern the agent has learned to apply.
Two axes make this concrete enough to design against: **short-term vs.
long-term** (how long the information persists) and **episodic vs. semantic**
(a specific remembered event vs. a general fact/pattern).

## The concept

### Short-term vs. long-term

- **Short-term memory** is the current conversation's context window -- exactly
  what Module 04's `messages` list holds, and what Module 05's compaction
  manages. It disappears when the conversation/process ends unless you
  explicitly persist it.
- **Long-term memory** survives across separate conversations or process
  restarts -- a user's stated preference from last week, a fact learned in a
  previous session, a running summary of everything an agent has done for a
  given user over time. This requires deliberate storage (lesson 02) --  it
  doesn't exist unless you build it.

### Episodic vs. semantic

- **Episodic memory** is a specific past event: "the user asked about refunds
  on March 3rd and I told them the 30-day policy." It's tied to a particular
  occurrence.
- **Semantic memory** is a general fact or learned pattern, detached from the
  specific event that taught it: "this user generally prefers short answers,"
  or "our refund policy is 30 days" (as a standalone fact, not "as I told
  someone once"). Semantic memory is often *derived from* episodic memory --
  noticing a pattern across many episodes and extracting the general fact.

### Where this shows up in what you've already built

| Pattern (from an earlier module) | Memory type |
|---|---|
| Module 04's `messages` list during one agent run | Short-term |
| Module 05's compacted summary placeholder | Short-term (still scoped to the current run) |
| Module 06's document corpus | Long-term, semantic (facts that exist independent of any conversation) |
| "Remember that this user prefers metric units" across sessions | Long-term, semantic |
| "Recall exactly what I told this user in our last conversation" | Long-term, episodic |

Naming the type clarifies the right mechanism: episodic long-term memory
usually means storing and later retrieving specific past interactions (a log,
searchable by conversation); semantic long-term memory usually means
extracting and storing a distilled fact once, rather than re-deriving it from
raw history every time.

## Deeper: most "the agent should remember X" requirements are actually semantic

When a product requirement says "the agent should remember what the user told
it," it usually means semantic memory (a distilled preference or fact) more
often than true episodic recall (the exact original conversation). Confusing
the two leads to over-engineering: building a full searchable conversation
history (episodic) when a single stored preference string (semantic) would
have satisfied the actual requirement far more simply and cheaply.

## When not to use this

Don't add long-term memory to a system where every interaction is genuinely
independent (a one-shot classification tool, a stateless API each call of
which stands alone) -- long-term memory adds real complexity (storage, privacy
considerations, staleness) that's wasted if nothing actually needs to persist
across calls.

## Common mistakes

- Treating "memory" as one undifferentiated feature to bolt on, instead of
  identifying which of the four combinations (short/long x episodic/semantic)
  an actual requirement needs.
- Building episodic storage (a full history log) when the requirement is
  really semantic (a handful of distilled facts) -- more storage, more
  retrieval complexity, and slower for no benefit.
- Confusing Module 05's compaction (which manages short-term memory within one
  run) with long-term memory (which persists across separate runs) -- they
  solve different problems and neither substitutes for the other.

## Key takeaways

- Short-term memory is the current run's context; long-term memory survives across runs and must be deliberately stored.
- Episodic memory is a specific remembered event; semantic memory is a general, distilled fact.
- Most "remember this" product requirements are semantic long-term memory, not full episodic recall -- identify which one you actually need before building storage for it.

## Lab

[`labs/01-resumable-agent/`](../labs/01-resumable-agent/README.md)
