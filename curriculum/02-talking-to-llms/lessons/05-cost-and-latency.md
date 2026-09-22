# Cost and latency

**Last verified:** 2026-09-22
**Difficulty:** ★★☆☆☆ · **Time:** ~30-45 minutes

## Learning objectives

- Estimate the USD cost of a call before making it.
- Explain the main levers that affect latency and which ones you control.
- Know why this repo defaults every lab to the cheapest current model per provider.

## Intuition

Every LLM call has a real, calculable dollar cost and a real, often
user-perceptible time cost. Treating these as afterthoughts is how a prototype
that "worked fine in testing" turns into a production surprise -- either a bill
far larger than expected, or a product that feels sluggish. Estimating both
*before* you build is cheap; discovering them after shipping is not.

## The concept

### Cost: it's almost always a function of tokens

```python
from shared.llm.pricing import estimate_cost
from shared.llm.types import Usage

usage = Usage(input_tokens=1500, output_tokens=300)
cost = estimate_cost("anthropic", usage.input_tokens, usage.output_tokens)
print(f"${cost:.6f}")
```

`shared/llm/pricing.py` has this repo's verified, dated pricing table for each
provider's default cheap model. Input and output tokens are usually priced
*differently* (output is typically several times more expensive per token than
input) -- so a prompt that generates a long response costs more than one of the
same input length that generates a short one, even though the input side is
identical.

### Latency: what you control and what you don't

- **Time to first token** -- how long before *any* output arrives. Affected by
  model choice (bigger/reasoning models are slower to start), and by
  provider/network conditions. Streaming (lesson 02) improves *perceived*
  latency here without changing total generation time.
- **Total generation time** -- roughly proportional to output length and model
  size/reasoning depth. You control this by controlling `max_tokens`, prompting
  for concise output, and choosing an appropriately-sized model for the task
  (Module 19's model routing).
- **What you don't control directly**: provider infrastructure load, network
  conditions, and (for hidden-reasoning models, Module 01 lesson 05) how long the
  model's internal reasoning takes for a given problem.

### A back-of-envelope cost estimate before building

Before writing an agent that will make, say, 10,000 calls/day averaging 2K input
tokens and 500 output tokens on Claude Haiku 4.5 pricing
(`$1.00`/`$5.00` per million tokens, per `shared/llm/pricing.py`):

```
input:  10,000 * 2,000 / 1,000,000 * $1.00  = $20.00/day
output: 10,000 *   500 / 1,000,000 * $5.00  = $25.00/day
total: ~$45/day, ~$1,350/month
```

Doing this arithmetic *before* building, not after the first invoice, is the
whole point of this lesson.

## Deeper: why this repo defaults to cheap models

`shared/llm/client.py`'s `_DEFAULT_MODELS` and every lab's live-test path use
each provider's cheapest current small model (Claude Haiku 4.5, GPT-5 nano,
Gemini 3 Flash) specifically so working through this curriculum with real API
calls costs cents, not dollars, per Ground Rule "default to cheap/small models."
Module 19's "model routing" is the production version of this idea: use a cheap
model for most steps, and reserve an expensive/reasoning model for the specific
steps that actually need it.

## When not to use this

Don't over-optimize cost at the expense of correctness on tasks where being
wrong is expensive in some other way (a customer-facing factual error, a failed
production deploy) -- cost-consciousness is a design input, not the only one.
Cheapest-possible is the wrong default for a task where a $0.02 cost difference
per call is irrelevant next to the cost of a wrong answer.

## Common mistakes

- Estimating cost from a handful of manual test calls without accounting for
  the *distribution* of real usage (some inputs/outputs will be much longer than
  your test cases).
- Forgetting that a multi-step agent (Module 04 onward) pays for *every* model
  call in its loop, not just one -- a 5-step agent loop can easily cost 5-10x a
  single completion call, even before considering that each step resends
  growing conversation history (Module 01, lesson 02).
- Not accounting for prompt caching (Module 19) when estimating cost for a
  system with a large, stable system prompt reused across many calls -- caching
  can reduce that portion's cost by 90%+ on supporting providers.

## Key takeaways

- Cost is a function of input and output tokens, priced separately and usually asymmetrically (output costs more per token).
- Streaming improves perceived latency, not total generation time or cost.
- Estimate cost with real usage-volume assumptions before building, not after the first bill.

## Lab

[`labs/01-chat-and-extract/`](../labs/01-chat-and-extract/README.md)
