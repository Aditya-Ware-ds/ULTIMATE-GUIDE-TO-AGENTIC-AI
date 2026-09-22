# Context rot

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~45 minutes

## Learning objectives

- Define context rot and distinguish its two main failure modes.
- Explain why a bigger context window doesn't fix context rot.
- Apply practical mitigations: fewer irrelevant tokens, better positioning, and compaction.

## Intuition

It's tempting to think of a large context window as a container: as long as
everything fits, the model should use it all equally well. It doesn't. As
measured across many current models, output quality measurably degrades as
input length grows -- well before the context window is technically full. This
is **context rot**, and it means "does it fit" is the wrong question; "will the
model actually use it well" is the right one.

## The concept

### Two distinct failure modes

1. **Positional degradation ("lost in the middle")** -- accuracy on
   information depends on *where* it sits in the context, following a
   roughly U-shaped curve: high for information near the start or end,
   meaningfully lower for information buried in the middle. Controlled studies
   have found accuracy dropping by 20-30 points for mid-context information
   compared to the same information placed at the start or end.
2. **Length degradation** -- accuracy declines as total input length grows,
   *even when* the needed information is fixed and favorably positioned. This
   is a separate effect from position -- it happens even in a "trivial"
   copy-and-retrieve task with no genuine reasoning required, across many
   current frontier models.

### Why this matters specifically for agents

For a long-running agent (Module 04's loop, run for many steps), tool-call
results, intermediate reasoning, and retrieved documents (Module 06) all
accumulate as exactly the kind of long, heterogeneous context these effects
degrade on. For coding agents specifically (Module 13), context rot from
accumulated search/exploration/backtracking noise is one of the most common
real failure modes in practice -- not a single dramatic bug, but a slow
accuracy decline as a session goes on.

### Practical mitigations

- **Compaction (lesson 02)** -- less total context means less exposure to
  length degradation, directly.
- **Position what matters** -- when you control ordering (e.g. constructing a
  prompt with retrieved documents), put the most critical information near the
  start or end of the context, not buried in the middle, given the U-shaped
  effect.
- **Prune aggressively, not just append** -- actively remove content that's no
  longer relevant (a resolved sub-question, an old tool result superseded by a
  newer one) instead of only ever adding.
- **Don't rely on "the window is big enough" as your only strategy** -- a 1M-token
  window fitting your content says nothing about whether the model will use the
  middle of it well.

## Deeper: context rot is a reason to prefer fewer, higher-quality tokens over more, lower-quality ones

Given a choice between stuffing in five loosely-relevant documents "just in
case" versus two clearly relevant ones, the two-document version is very
plausibly the *better* choice for accuracy, not just cheaper -- more context
isn't free, and past some point it actively competes with the information that
matters. This directly informs Module 06's retrieval design (fewer,
better-ranked results beat more, noisier ones) and Module 08's
orchestrator-workers pattern (each worker gets a narrow, focused context rather
than the whole task's accumulated history).

## When not to use this

Don't treat every long-context task as doomed -- context rot is a measured
*degradation*, not a cliff; many tasks with genuinely necessary long context
still work acceptably. The point is to stop assuming "it fits" implies "it will
be used well," and to measure (Module 16) rather than assume either way for
your specific task.

## Common mistakes

- Choosing a model purely by its advertised maximum context window size, without
  checking how well it actually performs at the lengths and positions your task
  needs (Module 16's evals are how you'd actually check this).
- Burying the most important instruction or fact in the middle of a long
  prompt, when re-ordering to put it first or last is often free.
- Treating "we have a 1M-token window, so let's just include everything" as a
  strategy rather than a context-engineering failure -- more isn't automatically
  better, per this lesson.

## Key takeaways

- Context rot has two distinct failure modes: positional ("lost in the middle") and length-based degradation, and both start well before a context window is full.
- A bigger context window doesn't fix context rot -- it's about how well the model uses what's there, not whether it fits.
- Fewer, well-positioned, relevant tokens generally beat more tokens "just in case" -- this informs compaction, retrieval, and multi-agent context design in later modules.

## Lab

[`labs/01-compacting-agent/`](../labs/01-compacting-agent/README.md)
