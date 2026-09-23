# Prompt caching, model routing, and cost optimization

**Last verified:** 2026-09-22 (against [Anthropic's current prompt-caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching))
**Difficulty:** ★★★★☆ · **Time:** ~40 minutes

## Learning objectives

- Explain how prompt caching mechanically reduces cost and latency for repeated prefixes.
- Apply model routing: sending different requests to different models based on their actual difficulty.
- Turn Module 17's cost dashboards into concrete optimization decisions at deployment scale.

## Intuition

Every module so far has treated a single request's cost as a fixed function
of its token count. At production scale, two more levers become available
that don't exist for a one-off script: **caching** content that repeats
across many requests, and **routing** different requests to different
models based on how hard they actually are -- both are ways of not paying
full price for work that doesn't need it.

## The concept

### Prompt caching, mechanically

Anthropic's current API (verified 2026-09-22) lets you mark content as
cacheable with a `cache_control` field, either automatically (one
top-level field) or on specific content blocks (system prompt, tool
definitions) for fine-grained control:

```json
{
  "system": [
    {"type": "text", "text": "You are an expert assistant...", "cache_control": {"type": "ephemeral"}}
  ],
  "messages": [...]
}
```

A cache hit costs roughly **10x less** than an uncached input token for
most models (as low as 20x less for some), at the cost of a slightly
more expensive first write. This is a large, mechanical win specifically
for content that's identical across many requests -- a long, stable system
prompt or tool-definition set (Module 03/13's tool descriptions, largely
unchanged across every call to the same agent) is exactly the shape of
content caching rewards; content that changes on every request (the actual
user message) gets no benefit from caching.

### Model routing

Not every request needs your most capable (and most expensive) model.
Module 08's routing pattern -- deciding which specialized handler a task
goes to -- applies directly to model choice: route simple, well-defined
requests to a cheap, fast model (Module 02's cost table), and route
requests that show signs of genuine difficulty (a first attempt with a low-
confidence or malformed response, a task matching a known-hard category) to
a stronger, more expensive one. This is the same escalation idea as
Module 12 lesson 02's "explicit status, not inferred success" -- a cheap
model's own signal of difficulty (rather than blind trust) decides whether
to escalate.

### From dashboards to decisions

Module 17's `summarize_usage` turned a single run's spans into a cost
figure. At deployment scale, the same rollup applied across many runs
answers concrete optimization questions: which fraction of requests would
have succeeded on a cheaper model (worth A/B testing a routing rule
against), whether a recent prompt change increased average cached-vs-
uncached token ratio (did caching stop working because the prompt now
changes per-request instead of staying stable), and whether cost per
successful outcome (not just cost per request) is trending in the right
direction.

## Deeper: caching and routing compose

The largest wins come from combining both: a cheap, fast model handling the
bulk of requests with a fully cached system prompt and tool definitions,
escalating only the harder fraction to an expensive model (which still
benefits from caching its own stable prefix). Neither lever alone captures
what the combination does.

## When not to use this

Don't add prompt caching for a system prompt or tool set that changes on
every single request -- caching only pays off for content that's actually
stable across calls; caching something that changes constantly adds
complexity for no benefit (and pays the more expensive cache-write cost
repeatedly with no matching cache-read savings).

## Common mistakes

- Routing purely on task category without ever validating that the
  cheaper model's actual success rate on that category is acceptable --
  Module 16's eval harness is exactly the tool for validating a routing
  rule before trusting it in production.
- Putting frequently-changing content (the actual user question) inside a
  cached block, which invalidates the cache on every request and wastes
  the more expensive cache-write cost for no matching savings.
- Optimizing cost per request without checking cost per *successful*
  outcome -- a cheaper model that fails more often can cost more overall
  once retries and escalations are counted.

## Key takeaways

- Prompt caching gives a large, mechanical cost/latency win specifically for stable, repeated content (system prompts, tool definitions) -- not for content that changes every request.
- Model routing sends easy requests to cheap models and escalates only genuinely hard ones, the same escalation discipline as Module 12's explicit-status pattern.
- Validate routing and caching decisions against real eval data (Module 16) and real cost dashboards (Module 17), not intuition alone.

## Lab

[`labs/01-streaming-idempotent-service/`](../labs/01-streaming-idempotent-service/README.md)
