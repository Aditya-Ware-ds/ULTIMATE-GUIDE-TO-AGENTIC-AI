# Deploy guide -- Multi-agent research system

Design sketch applying Module 19's patterns to this pipeline -- no new
runnable code (Module 19's lab already implements and tests the underlying
service/idempotency mechanics; this reuses that pattern by reference).

## Wrapping the pipeline as a service

A `POST /reports` endpoint (Module 19 lesson 01's `StreamingResponse`/
`TestClient` pattern) accepting `{"topic": ..., "idempotency_key": ...}`
and returning `run_traced_pipeline`'s result. Because a research report can
take multiple model calls and revision rounds, streaming intermediate
status (`"researching"`, `"drafting"`, `"critiquing (revision N)"`) as
server-sent events gives a caller visibility into a genuinely multi-step
process, rather than a single opaque wait.

## Idempotency for an expensive, multi-step operation

This pipeline is exactly the case Module 19 lesson 02 calls out: a
long-running, multi-call operation is precisely where a client is likely
to time out and retry. An `idempotency_key` per research request ensures a
retry returns the already-computed report instead of re-running the entire
researcher → writer → critic → (revise) chain a second time -- far more
consequential to duplicate here than a single-call operation, since a
duplicated run here costs 3-9x the token spend of a duplicated simple call.

## Cost and worker parallelism at scale

Module 08's parallelization point (restated in this capstone's
`ARCHITECTURE.md`): if research is extended to cover multiple sources
(Module 06's retrieval, per the "what this capstone doesn't attempt"
section), running multiple researcher instances concurrently across
sources is the natural latency lever, with a system-wide cost/step budget
(Module 12 lesson 02) capping total spend regardless of how many sources
are dispatched to.

## Observability in production

Module 17's spans (already wired into `research_pipeline.py`) export to
`InMemorySpanExporter` for testing; a production deployment would swap in
a real OTel-compatible backend (any collector supporting the standard OTLP
protocol) so the exact nested trace structure this capstone's tests verify
is available for real incident diagnosis, not just test assertions. Track
`mean_citation_accuracy` (from `eval_suite.py`) as a live production metric,
not just an offline eval score -- a real drop in citation accuracy over
time is a concrete, actionable signal that a prompt or model change
degraded quality, the same eval-driven-development discipline Module 16
lesson 01 describes, applied continuously in production rather than only
before a release.
