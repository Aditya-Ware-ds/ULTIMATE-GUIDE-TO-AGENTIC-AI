# Agent reliability math

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~30 minutes

## Learning objectives

- Compute how a single step's success probability compounds across a chain of dependent steps.
- Explain why this makes self-verification and checkpointing more valuable, not less, as a plan grows longer.
- Recognize the same math applies whether "steps" means agent loop iterations or sub-tasks in a long-horizon plan.

## Intuition

If a single step succeeds with probability `p`, and a task needs `n`
dependent steps to all succeed, the naive probability of the whole chain
succeeding isn't `p` -- it's `p` multiplied by itself `n` times. This simple
fact is why long-horizon autonomy is fundamentally harder than short-loop
agents, even when each individual step is reasonably reliable.

## The concept

### The compounding formula

```python
def naive_chain_success_probability(step_success_probability: float, num_steps: int) -> float:
    return step_success_probability**num_steps
```

At `p = 0.95` per step (a 95% success rate, which sounds quite good), the
whole-chain probability drops fast: `0.95**5 ≈ 0.77`, `0.95**20 ≈ 0.36`,
`0.95**50 ≈ 0.08`. A plan with 50 dependent sub-tasks, each individually
95% reliable, succeeds *end to end* only about 8% of the time if nothing
else changes. This is not a pessimistic edge case -- it's the direct
mathematical consequence of dependent steps compounding multiplicatively,
and it's exactly why "just make each step slightly more reliable" doesn't
solve long-horizon autonomy on its own.

### Why self-verification changes the math

If each step is independently *verified* before moving on (Module 13's
"run the tests" principle, applied per sub-task), a failure is caught and
corrected at the step where it happened, rather than silently propagating
forward and only surfacing as a mysterious failure many steps later. This
doesn't raise the underlying per-step success probability `p` -- it changes
what happens when a step *doesn't* succeed: instead of contaminating every
subsequent step, a caught failure can be retried or escalated in place,
which is a fundamentally different (and much better) reliability profile
than the naive compounding formula assumes.

### Why checkpointing changes the math too

Checkpointing (Module 07, extended to multi-task form in lesson 03) means a
failure at step 30 of 50 doesn't cost you steps 1-29's already-verified
work -- you resume from step 30, not step 1. Combined with per-step
verification, the *effective* cost of any single step's failure drops from
"redo the entire chain" to "redo one step," which is the actual reason
long-horizon autonomous agents are viable at all despite the raw
compounding math above.

## Deeper: this is the quantitative case for everything Modules 07/13/16 already built

This lesson doesn't introduce new techniques -- it gives you the actual
number that justifies why Module 07's checkpointing, Module 13's
self-verification, and Module 16's eval harness matter as much as they do.
"95% per-step reliability compounds to 8% over 50 steps without mitigation"
is the concrete, computable reason those techniques aren't optional
polish for a genuinely long-horizon agent.

## When not to use this

Don't over-invest in checkpointing and per-step verification for a short
chain (a handful of steps) where naive compounding still leaves acceptable
end-to-end reliability -- at `n=3` and `p=0.95`, the chain still succeeds
about 86% of the time, often good enough without the full apparatus lesson
03 builds.

## Common mistakes

- Assuming a high per-step success rate (95%, 99%) automatically means a
  long multi-step plan will succeed reliably, without doing the actual
  multiplicative math.
- Treating self-verification and checkpointing as separate, optional
  features rather than understanding they change the *shape* of the
  reliability formula itself (turning "redo everything" into "redo one
  step" on failure).
- Only computing this math after a long-horizon system is already failing
  in production, rather than using it upfront to decide how much
  verification/checkpointing infrastructure a planned task actually needs.

## Key takeaways

- Naive multi-step success probability compounds as `p**n` -- even a 95% per-step success rate degrades to single digits over 50 dependent steps.
- Self-verification catches failures at the step where they happen instead of letting them silently propagate forward.
- Checkpointing means a failure costs "redo one step," not "redo the whole chain" -- together, these are why long-horizon autonomy is viable despite the raw compounding math.

## Lab

[`labs/01-progress-file-agent/`](../labs/01-progress-file-agent/README.md)
