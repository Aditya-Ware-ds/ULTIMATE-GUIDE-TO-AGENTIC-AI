# Lab 06.01 -- Agentic RAG over a small document set

**Difficulty:** ★★★★☆ · **Time:** ~3 hours

## Task

Build a small retrieval system (chunking, a deterministic fake embedding,
hybrid search) over the four support-doc `.txt` files in `documents/`, then
wire it into an agent loop as a `search_documents` tool the model can call
multiple times -- agentic RAG, per this module's lesson 03.

No API key or real embedding model needed -- `toy_embed()` is a deterministic,
offline stand-in (see `lessons/01-chunking-and-embeddings.md` for what a real
one looks like). Tested against `shared.llm.get_client("mock")`.

## Files

- `documents/` -- 4 short `.txt` files (refunds, shipping, warranty, account) -- shared fixture data, not something you edit
- `starter/rag.py` -- skeleton with the pieces to implement
- `solution/rag.py` -- complete reference implementation
- `tests/` -- tests that exercise both

## Requirements

Implement these in `starter/rag.py`:

- `def load_documents(documents_dir: Path) -> dict[str, str]` -- read every
  `.txt` file in `documents_dir`, keyed by filename (e.g. `"refunds.txt"`).
- `def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]`
  -- fixed-size chunking with overlap (see `lessons/01-chunking-and-embeddings.md`).
- `def toy_embed(text: str, dimensions: int = 64) -> list[float]` -- a
  deterministic hash-based bag-of-trigrams vector using `hashlib.md5` (NOT
  Python's built-in `hash()`, which is randomized per-process and would make
  this non-deterministic across test runs).
- `def cosine_similarity(a: list[float], b: list[float]) -> float`
- `def keyword_score(query: str, chunk: str) -> float` -- fraction of query
  words present in the chunk (see `lessons/02-hybrid-search-and-ranking.md`).
- `def hybrid_score(cosine_sim: float, keyword_sim: float, alpha: float = 0.5) -> float`
- `def build_index(documents: dict[str, str]) -> list[tuple[str, list[float]]]`
  -- chunk every document, embed every chunk, return a flat list of
  `(chunk_text, embedding)` pairs.
- `def hybrid_search(query: str, index: list[tuple[str, list[float]]], top_k: int = 3, alpha: float = 0.5) -> list[str]`
  -- return the `top_k` chunk texts ranked by `hybrid_score`, highest first.
- `SEARCH_TOOL: ToolDefinition` and `def dispatch(tool_call, index) -> ToolResult`
  -- `dispatch` calls `hybrid_search` and joins the results into
  `ToolResult.content`; never raises (same contract as prior modules).
- `async def run_agentic_rag(client: LLMClient, index, user_input: str, max_steps: int = 5) -> str`
  -- the agent loop: system prompt instructing the model to use
  `search_documents` (and that it may call it again with a refined query),
  loop dispatching tool calls until a final text answer or `max_steps`.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/rag.py`.
- `load_documents` finds all 4 `.txt` files in `documents/`.
- `hybrid_search` for a query like `"warranty claim"` ranks a chunk from
  `warranty.txt` above unrelated chunks.
- `run_agentic_rag` correctly handles both a single-search exchange and a
  multi-hop exchange (two searches before a final answer), and stops cleanly
  at `max_steps`.

## Hints

- Use `pathlib.Path.glob("*.txt")` in `load_documents`.
- `hashlib.md5(trigram.encode()).hexdigest()` gives you a stable hex string;
  convert with `int(..., 16) % dimensions` to get a stable bucket index.
- Reuse the `dispatch`/loop pattern from Modules 03-05 almost verbatim --
  what's new here is what the tool *does* (retrieval), not the loop mechanics.

## Running the tests

```bash
uv run pytest curriculum/06-retrieval-and-rag/labs/01-agentic-rag/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/06-retrieval-and-rag/labs/01-agentic-rag/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then the
"research assistant with citations" project in [`projects/`](../../../../projects/README.md),
then [Module 07 -- Memory & state](../../../07-memory-and-state/README.md)
