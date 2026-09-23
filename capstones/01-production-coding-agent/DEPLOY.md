# Deploy guide -- Production coding agent

This sketches how Module 19's deployment patterns apply to this capstone's
agent -- it's a design document, not new runnable code (Module 19's own
lab already implements and tests the underlying service-wrapping and
idempotency mechanics in full; this capstone reuses that pattern rather
than reimplementing it).

## Wrapping the agent as a service

Following Module 19 lesson 01 directly: a `POST /fix-bug` endpoint,
dependency-injected with `get_llm_client` the same way Module 19's lab's
`create_job` endpoint is, accepting `{"repo_id": ..., "task": ...,
"idempotency_key": ...}` and returning `{"status", "steps", "output"}`
from `run_coding_agent`. `TestClient` (no real server) tests this
end-to-end the same way Module 19's lab does, swapping in the mock
provider via `app.dependency_overrides`.

## Idempotency

A retried request (the client didn't get a response due to a network
issue, but the agent actually ran) must not re-run the agent against the
same repo a second time -- Module 19 lesson 02's idempotency-key pattern
applies directly: the same `idempotency_key` returns the already-computed
fix result instead of re-invoking `run_coding_agent`, which matters here
specifically because a second run against an already-modified repo could
produce a different (and potentially worse) result than the first.

## Durable jobs for long-running fixes

A genuinely hard bug might need more than a single request/response cycle
worth of time -- Module 19 lesson 01's "durable job" pattern (itself
Module 07's checkpoint/resume, triggered by infrastructure events)
applies: submit the fix as a background job, poll `GET /fix-bug/{job_id}`
for status, and let a worker-process restart resume from wherever the
agent's own loop state was checkpointed, rather than losing all progress
on a mid-run interruption.

## Cost and model routing

Per Module 19 lesson 03: route straightforward, well-scoped bug-fix
requests (a small, clearly-described bug in a small file) to a cheap, fast
model with a cached, stable system prompt and tool-definition set; escalate
to a stronger model only when the cheap model's own attempt shows signs of
genuine difficulty (repeatedly failing `run_tests`, hitting `max_steps`) --
the same escalation discipline as Module 12 lesson 02's explicit-status
pattern, applied to model selection instead of worker dispatch.

## Sandboxing at deployment scale

Every one of `THREAT_MODEL.md`'s defenses (path-scoping, the fixed
`pytest`-only test command, the independent post-loop verification) holds
regardless of deployment scale -- they're properties of the tool layer
(Module 18's "the tool is the trust boundary" framing), not the request
volume. What changes at scale is the *operational* surface: rate limiting
(Module 19 lesson 02) to bound how many concurrent sandboxed subprocesses
a single deployment runs, and observability (Module 17) to catch a rising
failure rate before it's discovered by users rather than dashboards.
