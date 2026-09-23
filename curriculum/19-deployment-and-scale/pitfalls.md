# Module 19 pitfalls

## Checking idempotency after already calling the agent

It's tempting to write `create_job` as "run the agent, then check if we've
seen this key before" -- but that defeats the entire point: by the time
you're checking, the (possibly consequential) work has already happened
again. The check for an existing `idempotency_key` in `_JOBS` must happen
**before** `run_agent_job` is ever called, not as an afterthought once the
result is in hand.

## Forgetting to clear `app.dependency_overrides` between tests

FastAPI's `app` object (and its `dependency_overrides` dict) can persist
state across tests if the same `app` instance is reused without cleanup.
This lab's `conftest.py` clears `dependency_overrides` after each test
specifically to prevent one test's mock client override from leaking into
the next test's assertions -- in a real project reusing the same `app`
object across many test modules, forgetting this produces confusing,
order-dependent failures.

## Treating "it streams" as sufficient proof it's faster

This lab's `stream_job` computes the full result before streaming any of
it, then chunks the already-complete string -- which demonstrates the
`StreamingResponse` mechanics but provides none of streaming's actual
latency benefit (a real win requires forwarding provider tokens as they
arrive, per lesson 01's "deeper" note). Don't mistake "the endpoint uses
`StreamingResponse`" for "this endpoint has lower latency" without checking
whether it's actually streaming from the source or just chunking a
finished result.

## Using `_JOBS`'s in-memory dict as if it were production-ready durable storage

This lab's `_JOBS: dict[str, dict] = {}` is fine for tests (a fresh module
load gives a fresh dict per test, matching the pattern used for `_SENT_EMAILS`
and `_ISSUED_REFUNDS` in earlier labs) but would lose all job state on a
process restart in a real deployment -- exactly the scenario lesson 01's
"durable jobs" section is about. A production version needs actual
persistent storage (a database, a durable queue) so a restart doesn't
silently forget in-flight or completed jobs.
