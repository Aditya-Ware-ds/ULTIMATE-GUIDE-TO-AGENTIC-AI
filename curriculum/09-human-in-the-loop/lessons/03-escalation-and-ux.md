# Escalation and UX

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45 minutes

## Learning objectives

- Distinguish approval (asking before acting) from escalation (handing off because the agent is stuck or out of scope).
- Design what information a human actually needs to make a fast, correct approval decision.
- Recognize UX anti-patterns that make human-in-the-loop systems worse than no human at all.

## Intuition

Approval gates (lesson 01) ask permission *before* a specific risky action.
**Escalation** is different: the agent decides it should stop trying and hand
the entire task to a human, usually because it's stuck, the task is out of its
scope, or the stakes are too high for it to proceed with any confidence.
Both put a human in the loop, but at different points and for different
reasons -- approval is "let me act, with your sign-off"; escalation is "I
shouldn't be the one handling this."

## The concept

### When to escalate

- The agent has hit `max_steps` or exhausted retries without resolving the
  task (Module 04's stopping conditions -- escalation is a legitimate response
  to hitting a limit, not just returning an error).
- The task falls outside the agent's defined scope (e.g. a support agent
  handling only order status is asked a legal question).
- Confidence is genuinely low and the cost of a wrong answer is high (a
  medical, legal, or financial question the agent isn't equipped to answer
  reliably).
- The user explicitly asks for a human.

```python
def should_escalate(step_count: int, max_steps: int, out_of_scope: bool) -> bool:
    return step_count >= max_steps or out_of_scope
```

A real system's escalation trigger is more nuanced than this, but the shape
is the same: a clear, checkable condition, not a vague "if it seems hard."

### What a human needs to make a fast, good decision

For an approval gate specifically, surfacing *just* the tool name and raw
arguments (`send_email({"to": "...", "subject": "...", "body": "..."})`) forces
the human to mentally parse a function call under time pressure. Better:
render it as what it actually *means* -- "This agent wants to send an email to
jane@example.com with the subject 'Order Update' and the following body:
[text]. Approve?" The gap between a raw tool call and its human-readable
consequence is real UX work, not a rendering afterthought.

### UX anti-patterns

- **Approval fatigue**: too many low-stakes gates (lesson 01) trains users to
  click "approve" without reading, defeating the entire mechanism.
- **Opaque escalation**: handing off to a human with no context ("I couldn't
  handle this, here you go") forces the human to start from scratch,
  duplicating work the agent already did. A good escalation includes a summary
  of what was tried and why it didn't work.
- **No visible progress during a long-running agent task**: a human staring at
  a spinner with no sense of what's happening (Module 22 touches on this for
  long-horizon agents) tends to lose trust in the system regardless of whether
  it's actually working correctly.

## Deeper: human-in-the-loop is a trust-calibration problem

The goal of both approval gates and escalation isn't "add a human somewhere"
-- it's calibrating how much autonomy an agent has to exactly the level
justified by its actual reliability on that specific action or task type. Too
little human involvement risks costly mistakes; too much erodes any benefit
of automation and trains the human to stop paying attention. Getting this
calibration right is an ongoing design activity (revisited with real evidence
in Module 16), not a one-time setting.

## When not to use this

Don't design elaborate escalation logic for a system with no clear "who
receives the escalation and what do they do with it" -- an escalation with no
real human on the other end (or no clear next step for them) isn't
human-in-the-loop, it's just a dead end dressed up as one.

## Common mistakes

- Escalating with a bare error message instead of a summary of what was
  attempted -- the human has to redo the agent's diagnostic work from scratch.
- Confusing approval and escalation in a system's design -- an approval gate
  that never actually lets the agent continue after approval (functioning as a
  disguised escalation) or an escalation that pretends the agent might still
  resolve things (leaving the human waiting on the agent instead of taking
  over).
- Measuring human-in-the-loop success only by "did we add a checkpoint,"
  without checking whether real humans are actually engaging meaningfully with
  it (versus rubber-stamping).

## Key takeaways

- Approval asks permission before a specific action; escalation hands off the whole task because the agent shouldn't continue.
- Render pending actions in human-meaningful terms, not raw tool-call syntax -- this is real UX work, not a formatting detail.
- Both are trust-calibration decisions: too little human involvement risks costly mistakes, too much erodes the automation's value and trains rubber-stamping.

## Lab

[`labs/01-approval-gate/`](../labs/01-approval-gate/README.md)
