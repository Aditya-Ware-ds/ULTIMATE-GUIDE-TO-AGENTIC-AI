# GRPO and group-relative advantages

**Last verified:** 2026-09-22 (formula verified against [Hugging Face TRL's current GRPO trainer docs](https://huggingface.co/docs/trl/main/en/grpo_trainer))
**Difficulty:** ★★★★★ · **Time:** ~45 minutes

## Learning objectives

- Compute GRPO's group-relative advantage from a batch of sampled candidates and their verifiable rewards.
- Explain why GRPO avoids needing a separate learned value/critic model, unlike PPO.
- Recognize this module's lab as illustrating GRPO's reward/advantage math specifically, not a full RL training implementation.

## Intuition

Lesson 01 established a verifiable reward function; a real RLVR training
pipeline needs one more piece to turn rewards into a training signal: for a
*group* of sampled candidate outputs for the same prompt, which ones should
be reinforced more, and which less? **GRPO (Group Relative Policy
Optimization)**, introduced in DeepSeekMath and now widely used, answers
this with a specific, real formula this lesson implements directly.

## The concept

### The formula (verified against Hugging Face TRL's current docs)

For a group of `G` sampled completions with rewards `r_1, ..., r_G`:

```
advantage_i = (r_i - mean(r)) / std(r)
```

Each candidate's advantage is its reward, normalized against the *group's
own* mean and standard deviation -- a candidate scoring above the group
average gets a positive advantage (reinforce it more), one scoring below
gets a negative advantage (reinforce it less), and the group itself serves
as its own baseline.

### Implementing it directly

```python
def group_relative_advantages(rewards: list[float]) -> list[float]:
    n = len(rewards)
    mean_reward = sum(rewards) / n
    variance = sum((r - mean_reward) ** 2 for r in rewards) / n
    std_reward = variance**0.5
    if std_reward == 0:
        return [0.0] * n  # every candidate scored identically -- no signal to learn from
    return [(r - mean_reward) / std_reward for r in rewards]
```

Given rewards `[1.0, 1.0, 0.0, 0.0]` (two correct, two incorrect candidates
out of a group of four), this produces a positive advantage for the correct
ones and a negative advantage for the incorrect ones -- exactly the signal
a policy-gradient update would use to reinforce the correct candidates'
token choices and discourage the incorrect ones', without ever training a
separate critic network to estimate a baseline.

### Why no critic model is needed

PPO (the algorithm GRPO modifies) trains a separate value/critic network
specifically to estimate a baseline for computing advantages -- a second
full model, trained alongside the policy, adding real memory and compute
cost. GRPO's insight: **the group itself provides that baseline** (its own
mean reward), so no separate critic is needed at all. This is confirmed
directly in Hugging Face's current TRL documentation: GRPO "eliminates this
dependency entirely," reducing memory usage and simplifying training
compared to PPO.

## Deeper: this module's lab implements the math, not a training run

`group_relative_advantages` above is a real, correct implementation of
GRPO's actual advantage formula -- but computing an advantage is only one
piece of an actual RL training step (which also needs a policy-gradient
update, a real model's weights, and many training iterations). This
module's lab stops at the advantage computation deliberately: it's the
piece that's genuinely testable and understandable without GPU training
infrastructure, and understanding it precisely is what this lesson teaches,
without claiming to implement full RL training (which is out of scope for
an offline-testable curriculum, per this module's README).

## When not to use this

Don't reach for GRPO's group-relative framing for a task with only one
candidate output to evaluate at a time -- the entire mechanism depends on
having a genuine *group* of samples per prompt to normalize against; with a
single sample, there's no group statistic to compute at all.

## Common mistakes

- Computing advantage against a fixed, global baseline instead of each
  group's own mean/std -- this is exactly the "separate critic" approach
  GRPO is designed to avoid; the baseline must be recomputed per group.
- Not handling the zero-standard-deviation case (every candidate in a group
  scored identically) -- dividing by zero, or worse, silently producing
  `NaN` values that corrupt everything downstream.
- Treating this lesson's implementation as a complete RL training loop --
  it computes the advantage signal correctly, but a real training step
  still needs the policy-gradient update this module doesn't implement.

## Key takeaways

- GRPO computes each candidate's advantage as `(reward - group_mean) / group_std`, using the sampled group itself as the baseline.
- This eliminates the need for PPO's separate learned critic model, reducing memory and training complexity -- verified directly against Hugging Face TRL's current documentation.
- This module's lab implements the real advantage-computation math, not a full RL training run -- that's the genuinely offline-testable, understandable piece.

## Lab

[`labs/01-verifiable-reward-loop/`](../labs/01-verifiable-reward-loop/README.md)
