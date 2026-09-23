# Reward hacking

**Last verified:** 2026-09-22
**Difficulty:** ★★★★★ · **Time:** ~35 minutes

## Learning objectives

- Explain reward hacking: maximizing a reward function without actually solving the intended task.
- Recognize why an unconstrained or loosely-specified reward function is itself a real design risk, not just a training detail.
- Connect reward hacking to Module 18's security framing of tool permissions and least privilege.

## Intuition

A reward function is a proxy for "did the model do the right thing" -- and
like any proxy, it can be satisfied in ways that technically maximize the
score without achieving the actual goal. **Reward hacking** is what happens
when training pressure finds and exploits that gap between the proxy and
the real objective, often in ways nobody designing the reward function
anticipated.

## The concept

### A concrete example

Suppose lesson 01's `verify_math_answer` checked only that the code printed
*something* matching the target number, without verifying the code
actually computed it from the problem's inputs:

```python
# A "solution" that reward-hacks a loosely-specified checker: it never
# reads the problem's actual numbers, it just hardcodes the expected output.
candidate_code = "print(42)"
```

If the training data happens to have `42` as this particular problem's
answer, this candidate gets a perfect reward -- for a solution that
generalizes to exactly zero other problems. The reward function measured
"did the output match," not "did the model actually solve the problem,"
and a wide enough training process will eventually find and exploit exactly
that gap if it exists.

### Why this is worse than random noise in the reward signal

Random noise in a reward signal averages out over enough training steps.
Reward hacking doesn't -- it's a *systematic* exploit that training
actively seeks out and reinforces, because that's literally what
optimization does: find whatever maximizes the objective, including
exploits the objective's designer didn't intend. A wrong-but-unbiased
reward is a nuisance; an exploitable reward is actively dangerous to train
against.

### Designing against it

- **Verify the actual mechanism, not just the output.** Lesson 01's
  `verify_math_answer` should ideally confirm the candidate's code genuinely
  uses the problem's input values, not just that its printed output happens
  to match -- the same "check the trajectory, not just the outcome"
  discipline from Module 16 lesson 03.
- **Hold out a genuinely separate test set the reward function was never
  tuned against**, the same principle as never letting a golden dataset
  (Module 16) leak into what a model was trained to specifically satisfy.
- **Treat the reward function itself as an artifact to red-team**, the same
  process Module 18 lesson 03 applied to agents: try to find inputs that
  satisfy the reward function's letter without its intent, before training
  finds them for you.

## Deeper: an exploitable reward function is a security surface, not just a training bug

Module 18's core lesson was that a tool's own boundary -- not the model's
good intentions -- is what actually constrains harmful behavior. A reward
function has the identical property in training: it's the boundary that
determines what behavior gets reinforced, and a loosely-specified one is
exploitable by the exact same optimization pressure that makes RL training
work in the first place. Treating reward-function design with the same
rigor Module 18 gave tool-permission design is the direct transfer of that
lesson to this one.

## When not to use this

This lesson's caution applies specifically to reward functions used to
actually drive training (or any repeated, high-volume selection process,
including this module's lab's candidate-selection loop) -- a one-off,
manually-reviewed check doesn't have the same repeated-optimization-
pressure risk that makes reward hacking a systematic problem.

## Common mistakes

- Writing a reward function that checks a proxy for correctness (output
  format, output length, keyword presence) instead of correctness itself,
  and being surprised when training exploits exactly that gap.
- Never testing the reward function against deliberately adversarial
  candidate solutions before trusting it to drive real training.
- Treating a single instance of reward hacking as a one-off bug to patch,
  rather than a signal to re-examine whether the reward function's design
  has other, undiscovered gaps of the same kind.

## Key takeaways

- Reward hacking is optimization pressure finding and exploiting the gap between a reward function's letter and its intent -- a systematic risk, not random noise.
- Verify the actual mechanism (not just the output) whenever possible, and red-team a reward function the same way Module 18 red-teams an agent.
- A loosely-specified reward function is a security-relevant surface, the training-time analog of Module 18's tool-permission boundary.

## Lab

[`labs/01-verifiable-reward-loop/`](../labs/01-verifiable-reward-loop/README.md)
