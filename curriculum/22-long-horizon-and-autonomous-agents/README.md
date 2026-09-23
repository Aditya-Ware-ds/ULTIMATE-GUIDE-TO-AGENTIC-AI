# Module 22 -- Long-horizon & autonomous agents

**Difficulty:** ★★★★★ · **Time estimate:** 5-6 hours

## Objectives

By the end of this module you can:

- Explain why context management, self-verification, and checkpointing all matter more, not less, as a task's time horizon grows from steps to hours.
- Compute how reliability degrades across dependent steps, and explain why that makes self-verification load-bearing rather than optional.
- Build a progress-file-tracking agent that survives being killed and restarted mid-plan without repeating completed work.

## Prerequisites

[Module 21 -- RL and training for agents](../21-rl-and-training-for-agents/README.md)

## Why this module exists

Every prior module built agents that complete in seconds to minutes, within
a single bounded loop (`max_steps`). A genuinely long-horizon, autonomous
agent -- one working for hours across many discrete sub-tasks -- faces the
same failure modes at a much larger scale, and needs the same defenses
(Module 05's context budgeting, Module 07's checkpointing, Module 13's
self-verification) applied continuously rather than once. This module's
lab has a deliberate full-circle property: the pattern it teaches --
a durable, checkable progress file that lets work resume exactly where it
left off after an interruption -- is the exact mechanism this whole
repository's own `PROGRESS.md` has used across its entire multi-session
build. You're not implementing a hypothetical example; you're implementing
the thing that built this curriculum.

## Contents

- [`lessons/01-context-and-verification-at-scale.md`](lessons/01-context-and-verification-at-scale.md)
- [`lessons/02-reliability-math.md`](lessons/02-reliability-math.md)
- [`lessons/03-progress-files-and-resumability.md`](lessons/03-progress-files-and-resumability.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-progress-file-agent/`](labs/01-progress-file-agent/) -- a multi-task agent that survives being killed and restarted mid-plan
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 23 -- Research literacy](../23-research-literacy/README.md)
