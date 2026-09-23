# Verifiable rewards

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~40 minutes

## Learning objectives

- Explain what makes a reward "verifiable" and why that property matters for training, not just for evaluation.
- Write a deterministic reward function for a toy task, reusing Module 03/13's safe-execution patterns.
- Explain why RLVR is described as complementary to RLHF, not a replacement for it.

## Intuition

Module 16 established a principle for *evaluating* agents: prefer a
mechanical check over an LLM judge whenever one is available, because it's
faster, cheaper, and more reliable. **RLVR (Reinforcement Learning from
Verifiable Rewards)** applies the identical principle to *training*: instead
of a learned reward model (itself an approximation, trained on human
preference data, that can be gamed or simply wrong), train against a
reward that's computed by a deterministic, checkable process -- did the code
pass the tests, did the math answer match, did the generated SQL query
return the correct rows.

## The concept

### A verifiable reward function

```python
from shared.sandbox.code_sandbox import run_python


def verify_math_answer(candidate_expression: str, target: int) -> float:
    result = run_python(f"print({candidate_expression})")
    if not result.success:
        return 0.0
    try:
        return 1.0 if int(result.stdout.strip()) == target else 0.0
    except ValueError:
        return 0.0
```

This reuses Module 13's exact sandboxing discipline (candidate code is
model-generated, so it runs through `shared/sandbox/`, never a raw `eval()`)
-- for a genuinely verifiable task, the reward function *is* a real,
runnable check, not a prompt asking a model "is this correct?"

### Why "verifiable" matters more for training than for evaluation

An eval run happens occasionally, reviewed by a person. A training loop
computes a reward for every single sampled output, at scale, with no human
in the loop reviewing each one. A reward signal that's wrong even a small
fraction of the time systematically pushes the model's weights in a wrong
direction, repeated over millions of updates -- verifiability isn't a nice-
to-have here, it's what makes large-scale RL training trustworthy at all.

### RLVR is complementary to RLHF, not a replacement

RLVR works specifically where a task's correctness can be checked
mechanically: math, code that has tests, tool calls with a checkable
outcome. It does *not* apply to open-ended tasks with no ground truth to
check against -- "write a more engaging product description" has no
verifiable reward function the way "does this code pass its tests" does.
RLHF (reward modeling from human preferences) remains the applicable
approach for exactly that open-ended category -- the two are used together
in current training pipelines, covering different parts of a model's
capability, not competing for the same territory.

## Deeper: this is the same principle as Module 13's test-driven loop, one level up

Module 13's coding agent used "run the tests" as its *inference-time* stop
signal -- a mechanical check deciding when a single run was done. RLVR uses
the identical mechanical-check idea as a *training-time* reward signal --
deciding which of many sampled outputs to reinforce, across many runs. Same
principle (prefer a real, deterministic check over a judgment call),
applied at two different points in an agent's lifecycle.

## When not to use this

Don't force a verifiable-reward framing onto a task that has no actual
ground truth to check against -- a genuinely open-ended or subjective task
needs RLHF-style preference learning (or Module 16's LLM-as-judge, for
evaluation rather than training), not a fabricated "verifier" that doesn't
actually measure the right thing.

## Common mistakes

- Building a "verifier" that's actually just another LLM call dressed up as
  a mechanical check -- that's RLHF-adjacent reward modeling, not RLVR;
  it inherits the same reliability caveats Module 16 named for LLM-as-judge.
- Assuming RLVR replaces the need for human preference data entirely --
  it covers the mechanically-checkable slice of tasks, not everything a
  model needs to be trained on.
- Running model-generated candidate code for reward computation without
  sandboxing it, reopening exactly the risk Module 13 lesson 01 closes.

## Key takeaways

- A verifiable reward is computed by a deterministic, checkable process -- not a learned approximation -- the same "prefer a mechanical check" principle as Module 16, applied to training instead of evaluation.
- Verifiability matters more at training scale than at evaluation scale, since a training loop has no human reviewing each individual reward.
- RLVR is complementary to RLHF: it covers mechanically-checkable tasks (math, code, tool-use outcomes); RLHF still covers open-ended, subjective tasks with no ground truth to verify against.

## Lab

[`labs/01-verifiable-reward-loop/`](../labs/01-verifiable-reward-loop/README.md)
