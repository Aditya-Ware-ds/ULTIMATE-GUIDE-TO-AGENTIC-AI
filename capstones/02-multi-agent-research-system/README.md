# Capstone 2 -- Multi-agent research system

**Difficulty:** ★★★★★ · **Time:** ~4-6 hours
**Draws on:** Module 12 (multi-agent), Module 16 (evaluation), Module 17 (observability)

## Spec

Extend [`projects/04-multi-agent-content-pipeline/`](../../projects/04-multi-agent-content-pipeline/README.md)'s
researcher/writer/critic topology with real tracing (Module 17) and a
citation-accuracy eval suite (Module 16) -- with evals, tracing, and cost
visibility, per the original curriculum plan's capstone requirement.

No API key needed -- tested against `shared.llm.get_client("mock")`. See
[`ARCHITECTURE.md`](ARCHITECTURE.md) for design rationale,
[`THREAT_MODEL.md`](THREAT_MODEL.md) for the security analysis, and
[`DEPLOY.md`](DEPLOY.md) for how this would be deployed and scaled.

## Files

- `starter/research_pipeline.py`, `starter/eval_suite.py` -- skeletons with the pieces to implement
- `solution/research_pipeline.py`, `solution/eval_suite.py` -- complete reference implementation
- `tests/` -- tests for citation logic, traced-pipeline behavior and span structure, and the eval suite

## Requirements

### `research_pipeline.py`

`research`, `draft`, and `critique` are given, unchanged in logic from
`projects/04-multi-agent-content-pipeline/` except that each now wraps its
model call in a `chat_span` (Module 17). Implement:

- `def extract_citations(article: str) -> list[int]` -- every bracketed
  integer citation in `article` (e.g. `"...[1]...[2]..."` -> `[1, 2]`), in
  order of appearance.
- `def verify_citations(article: str, facts: list[str]) -> dict` --
  `{"total_citations": ..., "valid_citations": ..., "citation_accuracy": ...}`,
  where a citation is valid if it's a 1-indexed reference into `facts`.
  `{"total_citations": 0, "valid_citations": 0, "citation_accuracy": 0.0}`
  if there are no citations at all.
- `async def run_traced_pipeline(client, topic: str, max_revisions: int = 2) -> dict`
  -- the same control flow as `projects/04`'s `run_pipeline`, with the
  whole run wrapped in `invoke_agent_span("research-pipeline", ...)` and
  each worker call wrapped in its own
  `invoke_agent_span("researcher"/"writer"/"critic")`, plus the citation
  check added to the final `"success"`/`"escalated"` result.

### `eval_suite.py`

- `async def evaluate_citation_accuracy(pipeline_fn, client_factory, topics=None) -> dict`
  -- for each topic (default `DEFAULT_TOPICS`), get a fresh client, run
  `pipeline_fn`, and record its status and citation accuracy. Return
  `{"total": ..., "succeeded": ..., "mean_citation_accuracy": ..., "results": [...]}`,
  where the mean is computed only over succeeded topics.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/` implementations.
- A successful pipeline run's exported spans show real nesting: each
  worker's `invoke_agent` span is a genuine child of the pipeline's
  top-level `invoke_agent research-pipeline` span (verified via the
  parent/child span-ID check, not just that spans with the right names exist).
- `verify_citations` correctly distinguishes valid from hallucinated
  (out-of-range) citation numbers.
- `evaluate_citation_accuracy` excludes escalated (non-`"success"`) topics
  from the mean, and handles the all-escalated case without a
  division-by-zero.

## Running the tests

```bash
uv run pytest capstones/02-multi-agent-research-system/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest capstones/02-multi-agent-research-system/tests
```

## Next

[Capstone 3 -- Secure enterprise agent](../03-secure-enterprise-agent/README.md)
