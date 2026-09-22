# Module 09 quiz

**1. What's the difference between an approval gate and escalation?**

<details><summary>Answer</summary>

An approval gate asks permission before a specific risky action, then
continues (with or without that action). Escalation hands off the entire
task to a human because the agent shouldn't continue at all -- different
trigger, different outcome.

</details>

**2. Why should approval gates be selective rather than applied to every tool call?**

<details><summary>Answer</summary>

Gating everything trains users to rubber-stamp approvals without real
scrutiny, which defeats the purpose of having a gate for the genuinely risky
actions. Gates should be reserved for actions where a mistake is costly,
hard to reverse, or otherwise warrants a real decision.

</details>

**3. How is an approval gate structurally similar to Module 07's crash-recovery checkpointing?**

<details><summary>Answer</summary>

Both are "stop the loop, persist enough state to continue correctly, resume
from that state later." The difference is only *why* you stopped -- an
involuntary crash (Module 07) versus a deliberate wait for a human decision
(this module) -- the persistence/resume mechanics are the same.

</details>

**4. What extra piece of state does an approval-gate checkpoint need beyond Module 07's `messages` and `step`?**

<details><summary>Answer</summary>

The pending tool call itself -- the specific action awaiting a decision,
since it hasn't been dispatched yet and has no result in `messages` until
that decision is made.

</details>

**5. Why is a rejected action fed back to the model as a `ToolResult(is_error=True)` instead of raising an exception?**

<details><summary>Answer</summary>

It reuses the exact mechanism the model already knows how to react to
(Module 03's recoverable tool-failure pattern) instead of inventing a
separate code path -- the model can see the rejection and decide what to do
next (apologize, try something else), the same as any other recoverable
failure.

</details>

**6. Why is showing a raw tool call (`send_email({"to": "...", ...})`) to a human worse UX than a rendered, human-readable summary?**

<details><summary>Answer</summary>

It forces the human to mentally parse a function call under time pressure
instead of understanding the actual consequence of approving it. Rendering
it as what it means ("This agent wants to send an email to X about Y")
makes the decision faster and more accurate.

</details>

**7. Name two UX anti-patterns in human-in-the-loop design covered in this module.**

<details><summary>Answer</summary>

Any two of: approval fatigue (too many low-stakes gates causing
rubber-stamping), opaque escalation (handing off with no summary of what was
tried), or no visible progress during a long-running task.

</details>

**8. Why does a good escalation include a summary of what the agent already tried, rather than just an error message?**

<details><summary>Answer</summary>

Without it, the human receiving the escalation has to redo the agent's
diagnostic work from scratch, wasting the effort the agent already put in
and making the handoff far less useful than it could be.

</details>

**9. In this module's lab, why does `run_agent_with_approval` and `resume_after_approval` share a `_continue_loop` helper instead of each having its own full loop?**

<details><summary>Answer</summary>

Both entry points need identical loop behavior once they've set up their
starting `messages`/`step` -- the only difference between them is *how* that
starting state was produced (fresh vs. loaded-and-updated from a checkpoint).
Sharing the loop avoids duplicating logic (and duplicating bugs) between two
copies of the same behavior.

</details>

**10. What does "human-in-the-loop is a trust-calibration problem" mean?**

<details><summary>Answer</summary>

The goal isn't simply "add a human somewhere" -- it's matching an agent's
autonomy level to how much it's actually justified by its demonstrated
reliability on that specific action. Too little human involvement risks
costly mistakes; too much erodes the benefit of automation and trains users
to stop paying attention.

</details>
