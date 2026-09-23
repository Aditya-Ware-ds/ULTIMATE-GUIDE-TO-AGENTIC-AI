# Module 21 pitfalls

## Letting `verify_math_answer` raise instead of returning 0.0

It's tempting to let a syntax error or a non-integer output propagate as an
exception, on the theory that "a malformed candidate is clearly wrong
anyway." But a reward function that can raise breaks the calling loop for
every other candidate in the same group too -- `run_python`'s
`result.success` check and a `try/except ValueError` around the integer
parse both exist specifically so a bad candidate quietly becomes a reward
of `0.0`, not a crash that takes down the whole batch's reward computation.

## Computing standard deviation with the sample formula (n-1) instead of the population formula (n)

`group_relative_advantages` in this lab uses the population variance
(dividing by `n`, not `n-1`) to match GRPO's actual formula as implemented
in current training libraries (verified against Hugging Face TRL). Using
the sample-variance convention instead produces subtly different numbers
that will fail this lab's exact-value tests (`[1.0, -1.0, 1.0, -1.0]` for
rewards `[1.0, 0.0, 1.0, 0.0]`) even though "sample vs. population std" is
a reasonable-sounding thing to get right or wrong either way in isolation
-- match the specific formula actually used, not a plausible-sounding
variant of it.

## Treating a passing test suite here as proof you understand real RL training

This lab's tests verify the reward function and the advantage formula are
implemented correctly -- they say nothing about policy-gradient updates,
learning rates, KL-divergence penalties against a reference policy, or any
of the other real machinery an actual GRPO training run needs. Passing
this lab's tests means you understand the reward/advantage math correctly,
which is genuinely useful and transferable -- it does not mean you've
implemented (or could immediately implement) a full RL training pipeline.

## Confusing "the reward function is deterministic" with "the reward function is correct"

`verify_math_answer` is deterministic (same input always gives the same
output) but that alone doesn't make it a *good* reward function -- lesson
02's reward-hacking material is precisely about deterministic reward
functions that are nonetheless exploitable because they check a proxy
(output matches) rather than the actual intended behavior (the candidate
genuinely computed the answer from the problem's inputs). Determinism and
correctness of specification are two different properties; a reward
function needs both.
