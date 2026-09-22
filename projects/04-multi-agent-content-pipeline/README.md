# Project 04 -- Multi-agent content pipeline

**Difficulty:** ★★★★☆ · **Time estimate:** 2-3 hours
**Comes after:** Level 3, Module 12 (Multi-agent systems)

## Spec

Build a content-production pipeline with three specialized stages --
**researcher** (gathers facts), **writer** (drafts and revises), and
**critic** (approves or requests revision) -- following Module 12's
supervisor-worker discipline: each stage reports an explicit status, and the
pipeline escalates rather than quietly returning something that looks
finished but isn't.

This is an integration project: it reuses Module 12's "explicit status, not
inferred success" pattern (research can fail outright) and Module 08's
evaluator-optimizer loop shape (draft -> critique -> revise, bounded by
`max_revisions`) for the writer/critic stages -- no new agent-loop mechanics.
No API key needed -- tested against `shared.llm.get_client("mock")`.

## Files

- `starter/pipeline.py` -- skeleton with the pieces to implement
- `solution/pipeline.py` -- complete reference implementation
- `tests/` -- tests that exercise every path (success, first-try, one
  revision, research failure, exhausted revisions)

## Requirements

Implement these in `starter/pipeline.py`:

- `async def research(client, topic: str) -> dict` -- request a structured
  `{"status": "success", "facts": [...]}` or `{"status": "error", "reason": "..."}`
  response for `topic`.
- `async def draft(client, topic: str, facts: list[str], feedback: str | None) -> str`
  -- write a short article using `facts`; if `feedback` is given, revise
  based on it.
- `async def critique(client, topic: str, article: str) -> tuple[bool, str]`
  -- request a structured `{"approved": bool, "feedback": str}` review.
- `async def run_pipeline(client, topic: str, max_revisions: int = 2) -> dict`:
  1. Call `research`. If its `"status"` isn't `"success"`, return
     `{"status": "escalated", "reason": <research's reason>}` immediately --
     **do not** call `draft` or `critique`.
  2. Call `draft` with the research facts.
  3. Loop up to `max_revisions + 1` times: `critique` the current draft. If
     approved, return `{"status": "success", "article": ..., "revisions": <count>}`
     (`revisions` is the 0-indexed loop count, so a first-try approval is `0`).
     Otherwise, if revisions remain, call `draft` again with the feedback.
  4. If never approved, return
     `{"status": "escalated", "reason": <mentions the last feedback>, "article": <last draft>}`.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/pipeline.py`.
- A research failure escalates immediately with **exactly 1** model call --
  `draft`/`critique` must never run afterward.
- A first-try approval makes exactly 3 model calls (research, draft, critique).
- One rejection followed by approval makes exactly 5 calls and returns
  `revisions: 1`.
- Exhausting `max_revisions` without approval escalates with the **last**
  draft attached, not an exception and not a false "success".

## Running the tests

```bash
uv run pytest projects/04-multi-agent-content-pipeline/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest projects/04-multi-agent-content-pipeline/tests
```

## Next

Level 3 (and its interleaved projects) is complete. Continue to
[Level 4, Module 13 -- Coding agents](../../curriculum/13-coding-agents/README.md).
