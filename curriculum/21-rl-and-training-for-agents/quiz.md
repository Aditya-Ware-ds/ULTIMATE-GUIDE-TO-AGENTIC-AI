# Module 21 quiz

**1. What makes a reward "verifiable," and why does that matter more at training scale than at evaluation scale?**

<details><summary>Answer</summary>

A verifiable reward is computed by a deterministic, checkable process
(did the code pass tests, does the math answer match) rather than a
learned approximation. It matters more at training scale because a
training loop computes rewards for every sampled output with no human
reviewing each one -- an unreliable reward systematically pushes weights
in a wrong direction across millions of updates.

</details>

**2. Is RLVR a replacement for RLHF?**

<details><summary>Answer</summary>

No -- RLVR covers mechanically-checkable tasks (math, code with tests,
tool-use outcomes); RLHF remains the applicable approach for open-ended,
subjective tasks with no ground truth to verify against. They're used
together, covering different parts of a model's capability.

</details>

**3. What is reward hacking?**

<details><summary>Answer</summary>

Optimization pressure finding and exploiting the gap between a reward
function's letter and its actual intent -- maximizing the measured proxy
without actually solving the intended task, e.g. a "solution" that
hardcodes an expected output instead of computing it from the problem's
inputs.

</details>

**4. Why is reward hacking worse than random noise in a reward signal?**

<details><summary>Answer</summary>

Random noise averages out over enough training steps. Reward hacking is a
systematic exploit that training actively seeks out and reinforces, since
that's what optimization does -- find whatever maximizes the objective,
including unintended exploits.

</details>

**5. How does Module 18's "the tool is the trust boundary, not the model's intentions" principle apply to reward function design?**

<details><summary>Answer</summary>

A reward function is the training-time equivalent of a tool's permission
boundary -- it's what actually determines which behavior gets reinforced,
regardless of the model's or the designer's intentions. A loosely-specified
reward function is exploitable by the same optimization pressure that
makes RL training work, the same way an unconstrained tool is exploitable
by a manipulated model.

</details>

**6. What is GRPO's core formula for computing a candidate's advantage?**

<details><summary>Answer</summary>

`advantage_i = (r_i - mean(r)) / std(r)`, where `r` is the vector of
rewards for a group of sampled completions for the same prompt -- each
candidate's reward normalized against its own group's mean and standard
deviation.

</details>

**7. Why doesn't GRPO need a separate learned critic/value model, unlike PPO?**

<details><summary>Answer</summary>

The group itself provides the baseline (its own mean reward) that a
critic model would otherwise need to be trained to estimate -- verified
directly against Hugging Face TRL's current docs, which state GRPO
"eliminates this dependency entirely," reducing memory usage and training
complexity compared to PPO.

</details>

**8. Why does `group_relative_advantages` need to handle the case where every candidate in a group scored identically?**

<details><summary>Answer</summary>

The group's standard deviation would be zero, and dividing by it would
either raise a `ZeroDivisionError` or (worse) silently produce `NaN`
values that corrupt everything downstream -- correctly returning `[0.0, ...]`
reflects that there's genuinely no relative signal to learn from when
every candidate performed identically.

</details>

**9. Does this module's lab implement a real RL training step?**

<details><summary>Answer</summary>

No -- it implements the real, correct reward and advantage-computation
math (verifiable reward + GRPO's group-relative advantage formula), which
is genuinely testable and understandable offline. A full training step
also needs a policy-gradient update against real model weights across many
iterations, which is out of scope for this offline-testable curriculum.

</details>

**10. A team builds a "verifier" for a creative-writing task by asking an LLM whether a piece of writing is good. Is this RLVR?**

<details><summary>Answer</summary>

No -- an LLM call judging subjective quality is a learned approximation
(RLHF-adjacent reward modeling), not a deterministic, checkable process.
It inherits the same reliability caveats Module 16 named for LLM-as-judge,
and doesn't have RLVR's defining property: a reward that's mechanically
verifiable, not judged.

</details>
