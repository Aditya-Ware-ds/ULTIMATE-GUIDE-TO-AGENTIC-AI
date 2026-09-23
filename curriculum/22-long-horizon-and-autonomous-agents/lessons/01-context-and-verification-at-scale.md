# Context and verification at scale

**Last verified:** 2026-09-22
**Difficulty:** ★★★★★ · **Time:** ~40 minutes

## Learning objectives

- Explain why context budgeting (Module 05) becomes harder, not just bigger, over a multi-hour task.
- Explain why self-verification becomes load-bearing rather than optional as a task's horizon grows.
- Recognize which of this curriculum's existing tools already scale to long-horizon use, and which need rethinking.

## Intuition

Module 05's context-engineering lesson solved context budgeting for a
single bounded loop: compact when you approach a limit, keep the system
prompt and recent messages, summarize the rest. A task that runs for hours
across dozens of sub-tasks hits that same limit not once, but repeatedly --
and naive compaction applied over and over can quietly erode exactly the
information a later sub-task needs, in a way that's invisible until that
sub-task fails.

## The concept

### Context budgeting compounds over a long horizon

A single agent loop's context grows once, up to `max_steps`. A long-horizon
agent's context grows across every sub-task it completes -- if each
sub-task's full history is kept, context exhaustion isn't a risk to guard
against once, it's a certainty to manage continuously. This is why
Module 22's lab (lesson 03) tracks progress in a **separate, durable file**
rather than the model's own context window: the record of what's been done
needs to survive and remain accessible independent of whatever compaction
happens to the live conversation.

### Self-verification becomes load-bearing, not optional

Module 13's coding agent independently re-ran the tests rather than
trusting the model's own claim of success -- a nice-to-have proof point for
a single, short task. Over a multi-hour horizon, it stops being optional:
without a mechanical check after each sub-task, an early, undetected
mistake compounds silently across every subsequent sub-task built on top of
it, and by the time a human notices something is wrong, hours of work may
need to be discarded rather than one step. Module 16's eval harness and
Module 13's "run the tests" principle both apply here, but now as a
continuous discipline applied after every sub-task, not a final check.

### What already scales, and what doesn't

- **Scales as-is**: Module 13's sandboxing (a subprocess boundary doesn't
  care how long the overall task has been running), Module 18's tool
  permissions (an allowlist is equally valid at hour one and hour six).
- **Needs rethinking**: Module 04's single-loop `max_steps` (a long-horizon
  agent needs a budget *per sub-task*, not one global step count for the
  entire multi-hour effort), Module 07's single-conversation checkpoint
  (sufficient for resuming mid-task, but not for tracking which of many
  independent sub-tasks are done -- lesson 03 builds the multi-task version
  of this idea).

## Deeper: this is why the ground rules for this whole curriculum matter here specifically

Ground Rule 1 (verify against current docs, date-stamp everything) and
Ground Rule 3 (all code must run) both exist because a long-running,
autonomous process compounds the cost of a wrong assumption the same way it
compounds the cost of an unverified mistake -- a stale API assumption
discovered at hour five of an autonomous run is far more expensive than one
caught in a five-minute interactive session. Long-horizon autonomy raises
the stakes on discipline that mattered all along.

## When not to use this

Don't add continuous self-verification and durable progress-tracking
overhead to a short, single-loop task that already completes reliably
within `max_steps` -- this module's techniques earn their cost specifically
at the multi-hour, multi-sub-task scale; applied to a five-second task,
they're pure overhead.

## Common mistakes

- Assuming a technique that works for a single bounded loop (Module 04's
  step budget, Module 07's single-conversation checkpoint) automatically
  scales to a multi-hour, multi-task effort without modification.
- Treating self-verification as a nice-to-have "extra check" rather than
  the thing that prevents hours of compounding, undetected error.
- Keeping all progress information only in the live conversation's context,
  where it's exactly as vulnerable to compaction/loss as everything else in
  that context.

## Key takeaways

- Context budgeting compounds over a long horizon -- durable, out-of-context progress tracking (lesson 03) is what survives repeated compaction.
- Self-verification (Module 13/16) becomes load-bearing over a long horizon, since an undetected early mistake compounds silently across every subsequent sub-task.
- Not every earlier module's pattern scales unmodified -- sandboxing and tool permissions do; single-loop step budgets and single-conversation checkpoints need a multi-task rethink (lesson 03).

## Lab

[`labs/01-progress-file-agent/`](../labs/01-progress-file-agent/README.md)
