# Sampling and decoding: temperature, top-p, top-k

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45-60 minutes

## Learning objectives

- Explain, mechanically, how a model turns its raw output into a chosen next token.
- Predict how raising or lowering temperature changes an agent's behavior.
- Know when to use temperature 0 (or near it) versus a higher value in agent code.

## Intuition

At every step, a language model doesn't directly output "the next word." It
outputs a probability distribution over its entire vocabulary -- a score for
*every possible next token*. **Decoding** is the process of turning that
distribution into one chosen token. Temperature, top-p, and top-k are all knobs
that control *how* that choice gets made from the distribution -- not what the
distribution itself contains.

## The concept

### From logits to probabilities: softmax and temperature

The model's raw output for each possible next token is a number called a
**logit** (unbounded, can be negative). Softmax turns logits into a probability
distribution that sums to 1:

```python
import math


def softmax(logits: list[float], temperature: float = 1.0) -> list[float]:
    scaled = [logit / temperature for logit in logits]
    max_scaled = max(scaled)  # subtract max for numerical stability
    exps = [math.exp(s - max_scaled) for s in scaled]
    total = sum(exps)
    return [e / total for e in exps]
```

**Temperature** divides logits before the exponential. Temperature `1.0` leaves
the distribution as the model produced it. Temperature `< 1.0` (e.g. `0.2`) makes
the distribution sharper -- the most likely tokens become even more dominant,
making output more deterministic and repetitive. Temperature `> 1.0` flattens the
distribution -- less-likely tokens get relatively more chance, making output more
varied and "creative," but also more prone to incoherence and, for agents,
picking a less-appropriate tool.

### Top-p (nucleus sampling) and top-k

- **Top-k** restricts sampling to only the `k` highest-probability tokens,
  discarding the rest before sampling.
- **Top-p** (nucleus sampling) restricts sampling to the smallest set of
  top tokens whose cumulative probability reaches `p` (e.g. `p=0.9`) -- this
  adapts to how "peaked" or "flat" the distribution is at each step, unlike a
  fixed `k`.

These are usually combined with temperature, not used instead of it: temperature
reshapes the distribution, top-p/top-k then truncate it before the final random
draw.

### Why agent code usually wants low (or zero) temperature

For tasks with one clearly correct or best answer -- picking which tool to call,
extracting a specific field, following a strict format -- you generally want
temperature at or near `0`: the model should reliably pick its highest-confidence
answer, not roll dice on it. Higher temperature is for tasks that genuinely
benefit from variety: brainstorming, creative writing, generating diverse test
cases. Note that temperature `0` does not guarantee perfectly identical output
across calls for every provider (some backends have residual non-determinism from
batching/hardware), but it minimizes intentional randomness.

## Deeper: sampling is why hallucination isn't a "bug"

Every token, including ones that form a confidently-stated wrong fact, comes from
the exact same sampling process as every correct token. The model has no separate
"I don't actually know this" signal that stops generation -- it samples the next
most-probable-looking token whether or not the resulting sentence is true. This is
foundational to understanding hallucination (lesson 05) as a structural property
of the generation process, not a fixable defect.

## When not to use this

Don't tune temperature as your primary tool for improving output quality or
factual accuracy -- it controls *variety*, not *correctness*. A wrong answer at
temperature 0 is still wrong; lowering temperature just makes the model more
likely to consistently give the *same* answer, right or wrong. Structured outputs
(Module 02), better prompts, retrieval (Module 06), and verification steps
(Module 08's evaluator-optimizer) are the actual tools for correctness.

## Common mistakes

- Setting a high temperature on tool-selection or structured-output calls "to make
  the agent smarter," then being confused when it picks the wrong tool or breaks
  the output schema more often.
- Assuming temperature 0 means fully deterministic output across every provider
  and every call -- treat it as "as deterministic as this provider gets," not an
  absolute guarantee.
- Conflating top-p and top-k as interchangeable -- top-k is a fixed cutoff count;
  top-p adapts to the shape of the distribution at each step.

## Key takeaways

- Softmax turns logits into probabilities; temperature reshapes that distribution before sampling.
- Top-p/top-k truncate the candidate set the final random draw is made from.
- Low temperature for tasks with one right answer (tool calls, extraction); higher temperature for tasks that benefit from variety.

## Lab

[`labs/01-token-sampling-visualizer/`](../labs/01-token-sampling-visualizer/README.md)
