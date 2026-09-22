# Project 01 -- Research assistant with citations

**Difficulty:** ★★★★☆ · **Time estimate:** 3-4 hours
**Comes after:** Level 1 (Modules 00-06)

## Spec

Build a research assistant that answers questions about spaceflight history
using a small bundled document corpus (`documents/`), citing which source
document supports each part of its answer, and **flagging citations that don't
correspond to a real source** -- a concrete, testable defense against the
hallucinated-citation failure mode covered in Module 01, lesson 05.

This is an integration project: it reuses Module 06's retrieval patterns
(chunking, a deterministic toy embedding, hybrid search) and Module 04's agent
loop almost directly, adding one new piece -- citation extraction and
verification -- rather than introducing new retrieval or agent-loop concepts.
Like the labs before it, it's split into `starter/` (skeleton with gaps) and
`solution/` (complete reference), tested the same way.

No API key needed -- tested against `shared.llm.get_client("mock")`, same as
every lab so far.

## Files

- `documents/` -- 5 short `.txt` files on spaceflight program history -- shared fixture data
- `starter/assistant.py` -- skeleton with the pieces to implement
- `solution/assistant.py` -- complete reference implementation
- `tests/` -- tests that exercise both

## Requirements

Implement these in `starter/assistant.py`:

- `def load_documents(documents_dir: Path) -> dict[str, str]`,
  `def chunk_text(text, chunk_size=300, overlap=50) -> list[str]`,
  `def toy_embed(text, dimensions=64) -> list[float]`,
  `def cosine_similarity(a, b) -> float`,
  `def keyword_score(query, chunk) -> float`,
  `def hybrid_score(cosine_sim, keyword_sim, alpha=0.5) -> float`
  -- same contracts as Module 06's lab (you may port that solution's
  implementations directly; the point of this project is the integration, not
  re-deriving retrieval math).
- `def build_index(documents: dict[str, str]) -> list[tuple[str, str, list[float]]]`
  -- **note the extra field versus Module 06**: each entry is
  `(source_name, chunk_text, embedding)` so retrieval results can be attributed
  to a specific source file.
- `def hybrid_search(query, index, top_k=3, alpha=0.5) -> list[tuple[str, str]]`
  -- returns `(source_name, chunk_text)` pairs, highest-scoring first.
- `SEARCH_TOOL: ToolDefinition` and `def dispatch(tool_call, index) -> ToolResult`
  -- `dispatch` formats each result as `f"[{source_name}]: {chunk_text}"` so the
  bracketed source name is visible to the model in the tool result, and
  instructs (via the search tool's description and/or system prompt) the model
  to cite sources the same way in its final answer.
- `def extract_citations(answer: str) -> list[str]` -- return every
  `[source_name]`-shaped bracketed tag found in `answer` (regex: `\[([\w.\-]+)\]`).
- `def verify_citations(answer: str, valid_sources: set[str]) -> list[str]` --
  return the citations from `extract_citations(answer)` that are **not** in
  `valid_sources` (i.e. fabricated/invalid citations). Empty list means every
  citation checks out.
- `@dataclass class ResearchAnswer` with fields `text: str`, `citations: list[str]`,
  `unverified_citations: list[str]`.
- `async def run_research_assistant(client, index, valid_sources, user_input, max_steps=5) -> ResearchAnswer`
  -- the agent loop (same shape as Modules 03-06): on reaching a final text
  answer, return a `ResearchAnswer` with `text` set to that answer,
  `citations` from `extract_citations`, and `unverified_citations` from
  `verify_citations` against `valid_sources`.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/assistant.py`.
- `load_documents` finds all 5 `.txt` files in `documents/`.
- A scripted final answer citing a real source (e.g. `"Apollo 11 landed in 1969 [apollo-program.txt]."`)
  produces `unverified_citations == []`.
- A scripted final answer citing a source that doesn't exist (e.g.
  `"...[gemini-program.txt]"`, which isn't in this corpus) produces that name in
  `unverified_citations`.
- `run_research_assistant` correctly handles a multi-hop exchange (two searches
  across different source documents before a final cited answer) and stops
  cleanly at `max_steps`.

## Why this matters beyond the exercise

A model can produce a citation that *looks* exactly as credible as a real one
-- confident, specifically formatted, plausible-sounding -- while referring to
a source that doesn't exist or wasn't actually retrieved. `verify_citations`
is a cheap, purely mechanical check (does this bracketed name match a real
source?) that catches one concrete instance of this failure mode. It does
**not** verify that the cited source actually *supports* the specific claim
next to it (that's a harder problem -- entailment checking -- out of scope
here, and still an active research area); it only catches citations pointing
to sources that don't exist at all. Know the difference before treating a
passing `verify_citations` check as "the answer is trustworthy."

## Running the tests

```bash
uv run pytest projects/01-research-assistant/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest projects/01-research-assistant/tests
```
