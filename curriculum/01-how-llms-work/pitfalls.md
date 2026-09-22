# Module 01 pitfalls

## Numerical instability in softmax

If you implement softmax as `exp(logit / temperature) / sum(...)` *without*
subtracting the maximum scaled logit first, large logits or a small temperature
(which makes `logit / temperature` large) can overflow `math.exp()` and raise
`OverflowError`, or produce `inf` values that silently corrupt the result. The
lesson's and solution's formula subtracts `max(scaled)` before exponentiating
specifically to prevent this -- the result is mathematically identical (softmax
is shift-invariant) but numerically stable. If your tests pass with small example
logits but you later feed real model logits (which can be large negative/positive
numbers) and get `nan`/`inf`, this is almost certainly why.

## Floating-point edge cases in `sample_index`

A cumulative-sum walk against `rng.random()` can, due to floating-point rounding,
have the cumulative sum fall *just* short of `1.0` on the last element even
though the probabilities were mathematically supposed to sum to exactly 1. If
your implementation doesn't have a fallback (returning the last index if the
loop completes without triggering the `target < cumulative` condition), you can
get an `IndexError`-adjacent bug (falling through the function with no return).
The solution's `return len(probabilities) - 1` after the loop exists specifically
for this edge case -- don't skip it.

## Tokenizer mismatch silently producing wrong cost estimates

If you use this lab's `count_tokens` (which uses `tiktoken`, an OpenAI tokenizer)
to estimate cost or context usage for a non-OpenAI model, you will get a number
that *looks* plausible and *is* wrong -- there's no error, just a systematically
biased estimate (see lesson 01's ~15-20% undercount figure for Claude). This
class of bug is dangerous precisely because it fails silently rather than
raising an exception.

## Confusing "lower temperature" with "more correct"

If your agent gives a wrong answer at temperature 0, lowering temperature
further (it's already at the minimum) or re-running at the same temperature and
hoping for a different, correct answer, are both category errors. Temperature
controls variety in *which* plausible-looking token gets picked; it says nothing
about whether the model's underlying "beliefs" are correct. A systematically
wrong model at temperature 0 will just be *consistently* wrong. If you're
debugging incorrect agent output, look at grounding/retrieval/prompt quality
(Modules 05-06), not the sampling parameters.
