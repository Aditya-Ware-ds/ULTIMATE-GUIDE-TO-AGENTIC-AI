# Module 22 quiz

**1. Why does context budgeting (Module 05) become harder, not just bigger, over a multi-hour, multi-task agent?**

<details><summary>Answer</summary>

A single bounded loop hits its context limit once; a long-horizon agent
hits it repeatedly, across every sub-task it completes. Repeated
compaction can quietly erode information a later sub-task needs, in a way
invisible until that later sub-task fails -- which is why this module
tracks progress in a separate, durable file rather than relying on the
live conversation's context to retain it.

</details>

**2. Why does self-verification become load-bearing (not optional) over a long horizon?**

<details><summary>Answer</summary>

Without a mechanical check after each sub-task, an early undetected
mistake compounds silently across every subsequent sub-task built on top
of it -- by the time it surfaces, potentially hours of work need to be
discarded rather than one step's worth.

</details>

**3. If a single step succeeds with probability 0.95, what's the naive success probability of a 50-step dependent chain, and why does that number matter?**

<details><summary>Answer</summary>

About 7.7% (`0.95**50`). It matters because it's the concrete, computable
reason self-verification and checkpointing aren't optional polish for a
genuinely long-horizon plan -- a per-step reliability that sounds good
(95%) still produces a chain that fails the overwhelming majority of the
time without mitigation.

</details>

**4. How does checkpointing change the *effective* cost of a step failing, without changing the underlying per-step success probability?**

<details><summary>Answer</summary>

Without checkpointing, a failure means redoing the entire chain from the
start. With checkpointing, it means redoing only the one failed step --
the raw probability `p` per step is unchanged, but the *consequence* of a
failure drops from "redo everything" to "redo one step."

</details>

**5. How does this module's progress file differ from Module 07's single-conversation checkpoint?**

<details><summary>Answer</summary>

Module 07's checkpoint resumes a single, ongoing conversation mid-stream.
This module's progress file tracks the status (pending/done) of many
largely-independent tasks, letting a resumed run skip straight past
already-completed tasks to the next pending one -- a different, coarser
granularity suited to multi-task plans rather than one continuous
conversation.

</details>

**6. Why must `save_progress` be called after every individual task, not just once at the end of a run?**

<details><summary>Answer</summary>

If the process is killed mid-run and progress was only ever saved at the
end, a crash anywhere costs the entire run's work -- defeating the whole
purpose. Saving after each task means a crash costs only the in-flight
task, not everything completed before it.

</details>

**7. In this module's lab, what specifically proves the kill-and-resume behavior works correctly?**

<details><summary>Answer</summary>

Calling `run_one_task_and_persist` directly for the first task (simulating
a crash right after it, not letting a full run complete in one call --
Module 07's same test pattern), then calling `run_long_horizon_agent`
again and verifying the already-completed task is never re-run (via the
mock provider's call count, and it would raise if asked to run out of
scripted responses).

</details>

**8. Why is "this repository's `PROGRESS.md`" cited as a real instance of this lesson's pattern rather than a hypothetical example?**

<details><summary>Answer</summary>

Because it genuinely is one: this entire multi-session curriculum build
used a checklist-plus-status file, updated after each completed module,
with an "exact next step" note -- the identical progress-file pattern this
module's lab implements in code, used for real across this repository's
own construction, not invented as a teaching device.

</details>

**9. Why is choosing a progress file's task granularity a real design decision, not a detail to gloss over?**

<details><summary>Answer</summary>

Too coarse (one giant task) means a crash anywhere still costs everything,
giving none of the benefit. Too fine (tracking every micro-step) adds
tracking overhead disproportionate to the risk being managed. The right
granularity matches the size of a natural, independently-completable unit
of work -- like this repository's own choice of "one curriculum module per
progress-file entry."

</details>

**10. A long-horizon agent's task is re-run "just to be safe" even though its progress file marks it `"done"`. What does this undermine?**

<details><summary>Answer</summary>

The entire efficiency gain resumability provides -- if a task's `"done"`
status is trustworthy (verified per lesson 01, not just claimed), re-running
it anyway wastes exactly the work the progress file was designed to avoid
repeating. Trust in the status requires it be set only after genuine
verification, not re-checked by redoing the work regardless.

</details>
