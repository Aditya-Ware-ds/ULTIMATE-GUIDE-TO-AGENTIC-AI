# Module 17 quiz

**1. Why does `run_traced_agent` need to be a distinct function from Module 04's `run_react_agent`, rather than the same function with tracing sprinkled in conditionally?**

<details><summary>Answer</summary>

Keeping tracing as a clean wrapper around the same core logic keeps the
agent's decision-making code readable and keeps instrumentation consistent
across every call site, instead of relying on each caller to remember to
add spans by hand -- and instrumentation should observe behavior, never
alter it.

</details>

**2. Why can't token usage be passed as a keyword argument to `chat_span()` when it opens?**

<details><summary>Answer</summary>

The response (and its usage numbers) doesn't exist yet at the moment the
span opens -- `chat_span()` only knows the model and provider at that
point. Usage must be recorded with `span.set_attribute(...)` inside the
`with` block, once `client.complete()` has actually returned.

</details>

**3. Why does span nesting (parent/child relationships) matter for debugging, not just having a flat list of events?**

<details><summary>Answer</summary>

Nesting is what lets a trace be reconstructed as a coherent, structured
run (an agent's spans containing its model/tool calls) rather than a bag of
timestamped events you'd have to manually correlate -- it's the difference
between a call stack and an unordered log.

</details>

**4. In `replay_trace`, why sort spans by `start_time` instead of by export order or span name?**

<details><summary>Answer</summary>

Export order and naming don't reflect when things actually happened;
`start_time` gives the true chronological sequence, which is what makes the
replayed output an accurate timeline of the run rather than an arbitrary
ordering.

</details>

**5. Why compute a span's indentation depth by walking its `parent` chain instead of assuming a fixed nesting pattern (e.g. "chat is always one level under invoke_agent")?**

<details><summary>Answer</summary>

A fixed assumption breaks the moment the actual topology is more complex
than a single flat loop -- Module 12's nested multi-agent spans, for
instance, can have several levels of nesting that a hardcoded assumption
wouldn't handle correctly. Walking the real parent relationship works for
any topology.

</details>

**6. Why does Module 12 lesson 02's point about multi-agent debugging needing "the whole conversation/handoff graph, not just one agent's log" connect directly to this module's replay technique?**

<details><summary>Answer</summary>

A trace with each agent's spans nested appropriately (a supervisor's span
containing its workers' spans) is exactly the whole-system visibility that
problem requires -- this module's replay technique is the general
mechanism that makes multi-agent debugging tractable, not a separate idea.

</details>

**7. Why is a single run's cost/latency number not yet "a dashboard"?**

<details><summary>Answer</summary>

A dashboard's value comes from trends across many runs (cost per run over
time, p50/p95 latency, error rate) -- a single run's numbers only describe
that one run, and questions like "did a prompt change quietly increase
average token usage" require aggregating summaries across many runs, not
computing one.

</details>

**8. Why should a cost dashboard prefer p95 (or another tail statistic) over just reporting mean latency?**

<details><summary>Answer</summary>

A mean can look fine while a meaningful fraction of runs are dramatically
slower than typical -- a fat tail that matters for real user experience but
gets averaged away by a mean alone. Tail statistics surface that risk.

</details>

**9. What's the general pattern this module uses for instrumenting any operation whose interesting details only become known partway through?**

<details><summary>Answer</summary>

Open the span first, do the real work, then record what you learned with
`span.set_attribute(...)` once it's actually known -- rather than trying to
gather all attributes upfront before the operation has even happened.

</details>

**10. A team builds elaborate dashboard tooling on top of their agent's traces, but the underlying spans are missing token-usage attributes on some model calls. What's the actual problem here?**

<details><summary>Answer</summary>

The dashboard is built on incomplete instrumentation -- it will report
confident-looking but wrong numbers (undercounted cost/usage) rather than
an obviously broken result. Verify the underlying trace data (lesson 01) is
being captured correctly for every run before trusting or building on
aggregated dashboard numbers.

</details>
