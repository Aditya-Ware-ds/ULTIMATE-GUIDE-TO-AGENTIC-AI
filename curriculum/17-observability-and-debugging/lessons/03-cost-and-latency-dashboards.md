# Cost and latency dashboards

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~30 minutes

## Learning objectives

- Aggregate token usage and duration across a run's spans into a summary.
- Explain why per-run cost/latency data needs to be aggregated over many runs to be useful for decisions.
- Connect a span-derived cost summary back to Module 02's cost-estimation math.

## Intuition

Lesson 01's spans record token usage per `chat` call as it happens. A single
run's numbers are interesting; what actually drives decisions (should we
switch models, is a prompt change making things more expensive, is p95
latency creeping up) comes from aggregating those numbers across many runs
over time -- exactly what a dashboard is for.

## The concept

### Summarizing one run's usage

```python
def summarize_usage(spans) -> dict:
    chat_spans = [s for s in spans if s.name.startswith("chat ")]
    input_tokens = sum(s.attributes.get("gen_ai.usage.input_tokens", 0) for s in chat_spans)
    output_tokens = sum(s.attributes.get("gen_ai.usage.output_tokens", 0) for s in chat_spans)
    total_duration_ms = sum((s.end_time - s.start_time) / 1_000_000 for s in chat_spans)
    return {
        "chat_calls": len(chat_spans),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_chat_duration_ms": total_duration_ms,
    }
```

This is a direct, mechanical rollup of exactly the attributes lesson 01's
`chat_span` calls recorded -- no new instrumentation needed, because the
data was already captured at the point where it was actually known.

### From token counts to an actual cost estimate

Feed `summarize_usage`'s `input_tokens`/`output_tokens` straight into
Module 02's `estimate_cost` (`shared/llm/pricing.py`) to turn a trace
summary into a real dollar figure for that run -- tracing and cost
estimation aren't separate concerns; a trace is what makes cost estimation
possible *after the fact*, for a run that already happened, rather than
only as an upfront prediction.

### Why single-run numbers aren't a dashboard

One run's cost and latency tell you about that run. A dashboard's actual
value comes from trends: cost per run over the last week (did a prompt
change quietly increase average token usage?), p50/p95 latency (is the
typical case fine but the tail getting worse?), and error rate (are more
runs than usual hitting `is_error` tool results or exhausting `max_steps`?).
None of that is visible from any single trace alone -- it requires
persisting and aggregating summaries like `summarize_usage`'s output across
every run, not just computing one.

## Deeper: this is the same "aggregate over runs" principle as Module 16's eval accuracy

Module 16's golden-dataset accuracy is only meaningful because it's
aggregated across a representative dataset, not judged on a single
question. Cost and latency dashboards apply the identical principle to
operational metrics instead of correctness: a single data point is noise;
a trend across many runs is signal.

## When not to use this

Don't build persistent dashboard infrastructure for an agent that runs a
handful of times total (a one-off analysis script, a personal tool) -- the
aggregation-over-time value proposition only exists once there's enough
volume of runs for trends to mean anything.

## Common mistakes

- Reporting only the mean latency, missing that a fat tail (a small
  fraction of runs that are dramatically slower) can matter more to actual
  user experience than the average.
- Computing cost from token counts using stale or hardcoded per-token
  prices instead of `shared/llm/pricing.py`'s verified, dated figures
  (Module 02) -- pricing changes, and a dashboard showing a wrong cost is
  worse than no dashboard.
- Building elaborate dashboard tooling before confirming the underlying
  trace data (lesson 01) is actually being captured correctly for every
  run -- a dashboard built on incomplete instrumentation reports confident,
  wrong numbers.

## Key takeaways

- Summarize a run's cost/latency by rolling up the attributes lesson 01's spans already recorded -- no new instrumentation needed.
- Feed summarized token counts into Module 02's `estimate_cost` to turn a trace into a real dollar figure.
- A dashboard's value comes from aggregating trends across many runs, the same "aggregate over many data points" principle as Module 16's eval accuracy, applied to cost and latency instead of correctness.

## Lab

[`labs/01-traced-react-agent/`](../labs/01-traced-react-agent/README.md)
