# Threat model -- Multi-agent research system

Following Module 18's four-step red-team framing and Module 12 lesson 02's
named multi-agent failure modes, applied to this specific pipeline. Every
threat maps to a specific, currently-passing test in `tests/`.

## Threat 1: a fabricated ("hallucinated") citation presented as accurate

**Scenario**: the writer worker cites a fact number that doesn't exist in
the research results (e.g. `[5]` when only 2 facts were returned), and
without a check, the article would present unverified content as sourced.

**Defense**: `verify_citations` mechanically checks every extracted
citation against the actual `facts` list's length -- an out-of-range
citation is counted as invalid and lowers the reported `citation_accuracy`,
rather than being silently accepted because it merely looks like a
citation.

**Proof**: `test_verify_citations_some_invalid`.

## Threat 2: the pipeline reports success despite a critic rejection

**Scenario**: per Module 12 lesson 02's core failure mode, a supervisor
(here, the pipeline's return logic) could claim success based on the
writer's output existing at all, rather than the critic's actual approval.

**Defense**: `run_traced_pipeline` only returns `"status": "success"` when
`critique`'s `approved` flag is `True` -- an unapproved draft after
exhausting `max_revisions` returns `"status": "escalated"` with the reason
and the last draft attached, never masked as a success.

**Proof**: `test_run_traced_pipeline_revises_once_then_succeeds` (positive
path) and `projects/04-multi-agent-content-pipeline/`'s existing
`test_pipeline_escalates_with_last_draft_after_exhausting_revisions`
(negative path, inherited unchanged from the project this capstone
extends).

## Threat 3: an untrusted research failure silently producing a low-quality article anyway

**Scenario**: if `research` returns `"status": "error"` (no reliable
sources for a topic) and the pipeline proceeded to draft an article anyway,
it would fabricate content with no factual basis at all.

**Defense**: `run_traced_pipeline` checks `research_result["status"]`
immediately and escalates before ever calling `draft` if research failed --
inherited unchanged from `projects/04-multi-agent-content-pipeline/`'s
exact discipline (Module 12 lesson 02's "explicit status, not inferred
success," now applied at the very first stage of the pipeline).

**Proof**: `test_run_traced_pipeline_escalates_immediately_on_research_failure`.

## Threat 4: an untraceable multi-agent failure

**Scenario**: without real span nesting, diagnosing *why* a specific bad
report was produced would require reconstructing the interaction between
researcher, writer, and critic from application logs alone -- slow, and
often impossible after the fact (Module 17 lesson 02's exact concern).

**Defense**: every worker's `invoke_agent` span is a genuine child of the
pipeline's top-level span, verified by walking the actual parent/child
`span_id` relationship (not just checking that spans with the right names
exist in some order) -- so a real production trace can be replayed
(Module 17 lesson 02's `replay_trace`) to see exactly which worker did
what, in what order.

**Proof**: `test_run_traced_pipeline_worker_spans_nest_under_the_pipeline_span`.

## What this threat model does not cover

This capstone's `research`/`draft`/`critique` workers call the LLM with
plain topic strings, not untrusted external content (unlike Module 18's
`read_document`-based indirect-injection scenario) -- so prompt-injection
risk via retrieved/tool content specifically is out of scope for *this*
pipeline's current tool surface. A production version that retrieves real
documents (Module 06) for the researcher stage would need Module 18's
full indirect-injection threat analysis applied to that retrieval step
specifically, the same way Capstone 3 applies it to a richer, tool-using
agent.
