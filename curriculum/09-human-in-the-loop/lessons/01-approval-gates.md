# Approval gates

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~45 minutes

## Learning objectives

- Decide which tools/actions need human approval and which don't.
- Implement an approval gate that intercepts a specific tool call before dispatch.
- Explain the cost of gating too much versus too little.

## Intuition

Not every tool call carries the same risk. Looking up the weather and sending
an email to a customer are not equivalent actions, even though both are "just
a tool call" mechanically. An **approval gate** is a checkpoint (in the
everyday sense, not necessarily Module 07's file-based one yet -- lesson 02
connects them) that stops execution before a specific, marked action runs,
until a human explicitly approves it.

## The concept

### Marking which tools require approval

```python
REQUIRES_APPROVAL = {"send_email", "delete_file", "charge_payment"}


def needs_approval(tool_call: ToolCall) -> bool:
    return tool_call.name in REQUIRES_APPROVAL
```

This is a deliberately simple design: a set of tool *names*. More granular
designs exist (e.g. approve `send_email` only above a certain size, or only to
external domains) -- but the simple version already forces the right question:
for *this* tool, is unattended execution acceptable, or does a mistake here
cost enough (money, reputation, irreversible data loss) that a human should
confirm first?

### What "gate" actually means in the agent loop

When the model calls a gated tool, the loop does **not** dispatch it
immediately the way Module 03's `dispatch` does for every other tool. Instead:
it pauses (lesson 02 covers exactly how), surfaces the pending action to a
human (lesson 03 covers how to do this clearly), and only proceeds to actually
call the tool once approved -- or reports back to the model that the action was
rejected, letting it decide what to do next (apologize, try something else,
ask a clarifying question).

## Deeper: the cost of over-gating

It's tempting to gate everything "to be safe." This has a real cost:  every
gate is a point where a human has to stop what they're doing and make a
decision, and a system that asks for approval on trivial, low-risk actions
trains users to rubber-stamp approvals without really evaluating them --
which defeats the entire purpose of having a gate for the genuinely risky
actions. Effective approval-gate design is selective specifically so that when
a gate *does* trigger, it's meaningful and gets real attention.

## When not to use this

Don't gate an action that's fully reversible and low-stakes (a search query, a
read-only lookup) -- there's no decision for a human to usefully make there,
and gating it only adds friction. Reserve gates for genuinely consequential,
hard-to-reverse, or costly actions.

## Common mistakes

- Gating by tool *category* too coarsely (e.g. gating every single write
  operation regardless of blast radius) instead of thinking about actual
  consequence and reversibility per action.
- No clear criteria for what's gated and why, leading to an ad-hoc, growing
  list that doesn't reflect a consistent risk assessment.
- Gating so much that approvals become routine box-checking rather than real
  scrutiny -- the over-gating trade-off above.

## Key takeaways

- An approval gate intercepts specific, marked tool calls before dispatch, requiring human sign-off first.
- Gate selectively, based on actual consequence and reversibility -- not everything, or the gate stops meaning anything.
- What happens on rejection matters as much as what happens on approval -- the model needs to see and react to a "no."

## Lab

[`labs/01-approval-gate/`](../labs/01-approval-gate/README.md)
