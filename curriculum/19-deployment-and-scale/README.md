# Module 19 -- Deployment & scale

**Difficulty:** ★★★★☆ · **Time estimate:** 6-8 hours

## Objectives

By the end of this module you can:

- Wrap an agent in a streaming HTTP API service and test it without a real running server or network.
- Design idempotent job handling so a retried request never re-runs a consequential action twice.
- Explain prompt caching, model routing, and rate limiting as concrete cost/latency levers, not abstract concerns.

## Prerequisites

[Module 18 -- Security & safety](../18-security-and-safety/README.md)

## Why this module exists

Every agent built so far has run as a direct Python function call in a test
or a script. Level 5 closes by asking what changes once that same agent has
to run as a real service: requests can be retried by a flaky client,
network partitions and process restarts can happen mid-run, and cost/
latency stop being lab metadata and start being a real operating budget.
This module wraps an agent in a minimal FastAPI service to make those
concerns concrete rather than abstract.

## Contents

- [`lessons/01-streaming-services-and-durable-jobs.md`](lessons/01-streaming-services-and-durable-jobs.md)
- [`lessons/02-retries-idempotency-and-rate-limits.md`](lessons/02-retries-idempotency-and-rate-limits.md)
- [`lessons/03-prompt-caching-and-cost-optimization.md`](lessons/03-prompt-caching-and-cost-optimization.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-streaming-idempotent-service/`](labs/01-streaming-idempotent-service/) -- a FastAPI service wrapping an agent, with idempotent job handling and a streaming endpoint
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

Level 5 is complete after this module. See
[Level 6, Module 20 -- Optimizing agents](../20-optimizing-agents/README.md).
