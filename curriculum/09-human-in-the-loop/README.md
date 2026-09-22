# Module 09 -- Human-in-the-loop

**Difficulty:** ★★★★☆ · **Time estimate:** 5-6 hours

## Objectives

By the end of this module you can:

- Design an approval gate that pauses an agent before a risky action, instead of either always asking or never asking.
- Implement pause-and-resume for an agent awaiting a human decision, building directly on Module 07's checkpointing.
- Design escalation: when an agent should hand off to a human instead of continuing to try.
- Apply basic UX principles for surfacing an agent's pending action to a human clearly enough for them to decide.

## Prerequisites

[Module 08 -- Planning & reasoning patterns](../08-planning-and-reasoning/README.md)

## Why this module exists

Every agent so far has run to completion (or a step limit) without ever
checking in with a person. Real agents that can take consequential actions --
sending an email, spending money, deleting data -- need a way to stop and ask
first. This module is where "an agent that can act" becomes "an agent that
knows which actions need a human's sign-off," using exactly the pause/resume
mechanics Module 07 already built, applied to a new trigger: not a crash, but
a deliberate wait for a decision.

## Contents

- [`lessons/01-approval-gates.md`](lessons/01-approval-gates.md)
- [`lessons/02-interrupt-and-resume.md`](lessons/02-interrupt-and-resume.md)
- [`lessons/03-escalation-and-ux.md`](lessons/03-escalation-and-ux.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-approval-gate/`](labs/01-approval-gate/) -- an agent that pauses before a risky tool call and resumes once approved or rejected
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

Level 2 is complete after this module. See
[`projects/`](../../projects/README.md) for the "customer-support agent with
escalation" project, then [Module 10 -- Protocols](../10-protocols/README.md)
(Level 3 begins).
