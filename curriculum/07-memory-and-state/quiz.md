# Module 07 quiz

**1. What's the difference between short-term and long-term memory in an agent system?**

<details><summary>Answer</summary>

Short-term memory is the current run's context (the `messages` list for this
conversation); it disappears when the run ends unless explicitly persisted.
Long-term memory survives across separate runs/conversations and requires
deliberate durable storage.

</details>

**2. Give an example of episodic memory and an example of semantic memory.**

<details><summary>Answer</summary>

Episodic: "the user asked about refunds on March 3rd and I explained the
policy" (a specific past event). Semantic: "our refund policy is 30 days" or
"this user prefers metric units" (a general, distilled fact detached from any
one occurrence).

</details>

**3. A product requirement says "the agent should remember the user's preferences." Is this usually episodic or semantic memory?**

<details><summary>Answer</summary>

Usually semantic -- a distilled preference (e.g. "prefers metric units")
rather than the full episodic history of every conversation where that
preference came up. Building full episodic recall when semantic memory would
satisfy the requirement is over-engineering.

</details>

**4. When is in-context memory (always including facts in the system prompt) sufficient, versus needing an external store?**

<details><summary>Answer</summary>

In-context memory is sufficient for a small, fairly static fact set that
doesn't meaningfully compete for context budget. An external store becomes
necessary once the fact set grows large, changes often, or needs to be shared
or queried across many separate conversations or users.

</details>

**5. Why don't dataclasses like `Message` serialize to JSON automatically?**

<details><summary>Answer</summary>

`json.dumps()` only knows how to serialize JSON's native types (dict, list,
str, number, bool, None) -- a dataclass instance (and an enum) isn't one of
those, so it needs explicit conversion (e.g. via `dataclasses.asdict` plus
handling the enum's `.value`) before it can be serialized, and the reverse
conversion to reconstruct the objects on load.

</details>

**6. Why should an agent checkpoint after every step rather than only at the end of a run?**

<details><summary>Answer</summary>

Checkpointing only at the end protects nothing -- a crash before completion
loses everything regardless, exactly as if there were no checkpointing at all.
Checkpointing incrementally after each step means at most one step's worth of
work is ever lost to an interruption.

</details>

**7. Why should a checkpoint file be deleted after a run completes successfully?**

<details><summary>Answer</summary>

A stale checkpoint left behind after completion could be accidentally loaded
by a later, unrelated run, causing it to incorrectly "resume" from someone
else's finished conversation -- a real correctness bug, not just leftover
clutter.

</details>

**8. Does checkpointing alone make it safe to resume a run that includes a tool with a real side effect (like sending an email)?**

<details><summary>Answer</summary>

No. Checkpointing prevents *state* loss, but if a crash happens after a
side-effecting action executed but before that step's checkpoint saved,
resuming naively could repeat the action. That requires designing the tool to
be idempotent (safe to call again with the same identifying information),
which is covered in Module 19.

</details>

**9. In this module's lab, why does the "kill and resume" test call `run_one_step` manually instead of just calling `run_resumable_agent` twice?**

<details><summary>Answer</summary>

Calling `run_resumable_agent` once would run the scripted exchange to
completion in a single call, since nothing stops it mid-way. Calling
`run_one_step` directly and saving a checkpoint from that partial state
simulates a process being interrupted after exactly one step, which is what
the test needs to prove real resumption (not re-doing the first step's model
call) rather than just "the function works end to end."

</details>

**10. Why is a `messages` list serialized to a checkpoint, rather than, say, only a summary of the conversation?**

<details><summary>Answer</summary>

The model needs its complete history to continue reasoning correctly on
resume -- a summary loses information the same way Module 05's compaction
does, which is an acceptable trade-off for managing a live context budget but
not appropriate for a checkpoint whose entire purpose is faithfully resuming
exactly where the run left off.

</details>
