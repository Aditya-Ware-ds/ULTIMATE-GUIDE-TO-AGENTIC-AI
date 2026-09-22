# Module 16 quiz

**1. Why don't this repo's existing unit tests against the mock provider already tell you "how good" an agent is?**

<details><summary>Answer</summary>

Unit tests prove the code behaves correctly given a specific, scripted
model response -- they say nothing about how the agent performs across the
real variety of inputs it will actually see. A golden-dataset eval measures
that instead, against a representative set of real inputs with known-correct
answers.

</details>

**2. Why is exact-string matching usually the wrong way to grade a free-form agent answer?**

<details><summary>Answer</summary>

Two answers can be equally correct while being different strings ("Paris"
vs. "The capital of France is Paris.") -- exact matching would mark the
second wrong. Grading by meaning (LLM-as-judge) or by parsing out the
actual answer (when the format allows) handles this; exact-string matching
doesn't.

</details>

**3. What is position bias in an LLM-as-judge, and how do you mitigate it?**

<details><summary>Answer</summary>

A judge comparing two candidates side by side can favor whichever one
appears first (or second), regardless of actual quality. Mitigate by
running the comparison twice with the order swapped and only trusting a
verdict that agrees both times.

</details>

**4. Why is it risky to use the same model as both the agent under test and its own judge?**

<details><summary>Answer</summary>

Self-preference bias: a model tends to rate its own outputs more favorably
than an independent judge would. Use a different model, or at minimum a
fresh independent call, as the judge.

</details>

**5. When should you use a mechanical check instead of an LLM-as-judge?**

<details><summary>Answer</summary>

Whenever one is available -- an exact numeric answer, a well-formed JSON
shape, a passing test suite (Module 13's "run the tests" principle).
Reserve LLM-as-judge for genuinely open-ended correctness with no
deterministic check.

</details>

**6. How does a trajectory eval differ from an outcome eval?**

<details><summary>Answer</summary>

An outcome eval checks only the final answer. A trajectory eval checks the
sequence of steps that got there -- which tools were called, in what order,
whether there were redundant or contradictory calls, and whether errors
were recovered from cleanly. Two agents can score identically on an outcome
eval while one required far riskier or less efficient trajectories.

</details>

**7. Why might an agent that "got lucky" on a trajectory eval be a bigger production risk than one that failed?**

<details><summary>Answer</summary>

An agent that reached the right answer through an inefficient or fragile
path (redundant calls, a near-miss on the step budget) is far more likely
to fail on a slightly different input than one that reached the same answer
via a disciplined, minimal, correct trajectory -- the "success" masks an
underlying fragility an outcome eval alone wouldn't reveal.

</details>

**8. What does SWE-bench measure, and what does GAIA measure?**

<details><summary>Answer</summary>

SWE-bench: given a real GitHub issue and its repository, can an agent
produce a patch that makes the repository's hidden test suite pass -- a
realistic coding-agent benchmark. GAIA: over 450 real-world questions
across three difficulty levels requiring tool use, search, and multi-step
reasoning to reach an unambiguous answer.

</details>

**9. Why should you re-verify a public benchmark's current leaderboard numbers before quoting them, even if you're confident in what the benchmark measures?**

<details><summary>Answer</summary>

Leaderboards for these benchmarks are actively maintained and change as
new models are evaluated -- what's measured is stable, but the specific
current standings are exactly the kind of fast-moving claim Ground Rule 1
warns about; a memorized number can already be stale by the time you quote it.

</details>

**10. A team ships a public benchmark score for their new coding agent. Is that sufficient evidence it's ready for their own production use case?**

<details><summary>Answer</summary>

Not necessarily -- public benchmarks rarely match a specific task's actual
domain and constraints. A good public-benchmark score is useful for
external comparison, but a custom golden-dataset and trajectory eval built
around the team's actual task is what actually validates production
readiness for that specific use case.

</details>
