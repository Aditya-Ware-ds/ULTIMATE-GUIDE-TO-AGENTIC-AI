# Module 17 -- Observability & debugging

**Difficulty:** ★★★★☆ · **Time estimate:** 5-6 hours

## Objectives

By the end of this module you can:

- Instrument an agent loop with `shared/tracing/` so every model call and tool call produces a real, nested OpenTelemetry span.
- Reconstruct a readable timeline of an agent run from its exported spans, for debugging a failure after the fact.
- Aggregate span attributes into a cost/usage summary for a run.

## Prerequisites

[Module 16 -- Evaluation](../16-evaluation/README.md)

## Why this module exists

`shared/tracing/tracer.py` was built in Phase 0 and unit-tested there
(`shared/tests/test_tracing.py` proves the span hierarchy and attributes
work correctly) -- but no lab has actually wired it around a real agent
loop yet. Module 16 gave you a way to know *whether* an agent got the right
answer; this module gives you a way to see *what actually happened* inside
a specific run, which is what you need once an eval catches a regression
and you have to find out why.

## Contents

- [`lessons/01-tracing-agent-loops.md`](lessons/01-tracing-agent-loops.md)
- [`lessons/02-replaying-failed-runs.md`](lessons/02-replaying-failed-runs.md)
- [`lessons/03-cost-and-latency-dashboards.md`](lessons/03-cost-and-latency-dashboards.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-traced-react-agent/`](labs/01-traced-react-agent/) -- a fully instrumented ReAct agent, plus trace replay and a usage summary
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 18 -- Security & safety](../18-security-and-safety/README.md)
