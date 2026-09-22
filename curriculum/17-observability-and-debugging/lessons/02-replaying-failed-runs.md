# Replaying failed runs

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~30 minutes

## Learning objectives

- Reconstruct a readable, ordered timeline of an agent run from its exported spans.
- Use a replayed trace to diagnose which specific step in a run caused a failure.
- Explain why a trace-based replay is more reliable than a plain-text log for this purpose.

## Intuition

Once lesson 01's spans exist, `get_exported_spans()` returns a flat tuple of
`ReadableSpan` objects -- useful data, but not yet a *story*. Replaying a
trace means turning that flat collection back into an ordered, nested
timeline a person can actually read and reason about, the same way a
debugger's call stack is more useful than a pile of unordered log lines.

## The concept

### Reconstructing the timeline

```python
def replay_trace(spans) -> str:
    spans_by_id = {s.context.span_id: s for s in spans}
    lines = []
    for span in sorted(spans, key=lambda s: s.start_time):
        depth = 0
        parent = span.parent
        while parent is not None:
            depth += 1
            parent_span = spans_by_id.get(parent.span_id)
            parent = parent_span.parent if parent_span else None
        duration_ms = (span.end_time - span.start_time) / 1_000_000
        attrs = ", ".join(f"{k}={v}" for k, v in span.attributes.items())
        lines.append(f"{'  ' * depth}{span.name} ({duration_ms:.1f}ms) [{attrs}]")
    return "\n".join(lines)
```

Sorting by `start_time` gives chronological order; walking each span's
`parent` chain gives its nesting depth, so a `chat` span inside an
`invoke_agent` span prints indented beneath it. The result reads like a
call stack unrolled over time -- exactly the shape that makes "which step
went wrong" a quick visual scan instead of a manual reconstruction.

### Using a replay to find a failure

Given a replayed trace, a failure usually shows up as one of:

- An `execute_tool` span whose recorded attributes show an error result
  (Module 03's `ToolResult.is_error`, if recorded as a span attribute) --
  the tool call itself failed.
- A `chat` span with unexpectedly high `gen_ai.usage.output_tokens` right
  before a failure -- often a sign the model produced a long, rambling
  response instead of a clean tool call or answer.
- An `invoke_agent` span whose total duration or child-span count is far
  higher than a typical successful run -- a sign the loop needed unusually
  many steps, which Module 04's stopping-condition discipline would have
  eventually cut off, but which is worth understanding regardless.

### Why this beats a plain-text log

A plain-text log (`print()` statements, or unstructured log lines) requires
you to already know what to look for and to manually correlate timestamps
across separate log entries. A trace's structure -- explicit parent/child
relationships, typed attributes, precise start/end times -- means the
correlation is already done; replaying it is reconstruction, not detective
work.

## Deeper: this is what makes multi-agent debugging (Module 12) actually tractable

Module 12 lesson 02 named the problem directly: multi-agent failures can
emerge from *interaction* between agents, which means debugging them
requires seeing the whole conversation/handoff graph, not just one agent's
log in isolation. A trace with each agent's `invoke_agent` span nested
appropriately (a supervisor's span containing its workers' spans) is
exactly the visibility that problem needs -- this module's replay technique
is the general mechanism Module 12 was implicitly asking for.

## When not to use this

Don't reach for full trace replay to debug a single, already-obvious
failure (a tool that raised an exception with a clear traceback) -- replay
earns its value for failures whose cause isn't obvious from the final
error alone, where seeing the whole sequence of steps leading up to it is
what actually reveals the problem.

## Common mistakes

- Sorting spans by name or by export order instead of `start_time`,
  producing a "timeline" that doesn't actually reflect what happened when.
- Computing nesting depth by string-matching span names (e.g. assuming
  `"chat"` is always one level under `"invoke_agent"`) instead of walking
  the actual `parent` relationship -- this breaks the moment topology gets
  more complex than a single flat loop (e.g. Module 12's nested agents).
- Discarding span attributes when summarizing a trace for a report, keeping
  only names and durations -- the attributes (tool names, token counts,
  error flags) are usually what actually explains *why* a step failed, not
  just that it took a certain amount of time.

## Key takeaways

- A trace replay reconstructs a chronological, nested timeline from a flat span collection -- sort by start time, nest by parent relationship.
- A replayed trace turns "which step failed" from manual log correlation into a quick visual scan.
- This same technique is what makes debugging Module 12's multi-agent interaction failures tractable, not just single-agent ones.

## Lab

[`labs/01-traced-react-agent/`](../labs/01-traced-react-agent/README.md)
