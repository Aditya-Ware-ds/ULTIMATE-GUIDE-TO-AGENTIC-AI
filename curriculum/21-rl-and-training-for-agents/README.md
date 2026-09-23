# Module 21 -- RL and training for agents

**Difficulty:** ★★★★★ · **Time estimate:** 5-7 hours

## Objectives

By the end of this module you can:

- Explain why verifiable rewards (RLVR) matter for training agents on math/code/tool-use tasks specifically.
- Compute GRPO's group-relative advantage from a batch of sampled candidates and their verifiable rewards.
- Recognize reward hacking and explain why an unconstrained reward function is itself a security-relevant surface.

## Prerequisites

[Module 20 -- Optimizing agents](../20-optimizing-agents/README.md)

## Why this module exists

Module 20 optimized a program's prompt and few-shot examples against a
metric. This module covers the next level up: optimizing the model's
*weights* against a reward signal via reinforcement learning. This
curriculum doesn't run real RL training (no GPU infrastructure, and it
would break every offline-testing ground rule since day one) -- what it
does teach, hands-on and fully verifiable, is the actual mathematical core
of the current dominant approach (RLVR + GRPO): a deterministic reward
function and a group-relative advantage calculation, both real, both
testable, without needing to actually train a model.

## Contents

- [`lessons/01-verifiable-rewards.md`](lessons/01-verifiable-rewards.md)
- [`lessons/02-reward-hacking.md`](lessons/02-reward-hacking.md)
- [`lessons/03-grpo-and-group-relative-advantages.md`](lessons/03-grpo-and-group-relative-advantages.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-verifiable-reward-loop/`](labs/01-verifiable-reward-loop/) -- a verifiable reward function and GRPO-style advantage computation over sampled candidates
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 22 -- Long-horizon & autonomous agents](../22-long-horizon-and-autonomous-agents/README.md)
