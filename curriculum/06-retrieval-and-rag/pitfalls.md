# Module 06 pitfalls

## Using Python's `hash()` for a "deterministic" embedding

It's tempting to reach for the built-in `hash()` function for a quick
toy-embedding hashing scheme -- it's shorter than `hashlib.md5`. Python
randomizes string hashing per-process by default (a security feature, `PYTHONHASHSEED`),
which means `hash("some text")` returns a *different* value in different runs of
your program. A test asserting `toy_embed("x") == toy_embed("x")` would still
pass *within* one test run (same process), but any test comparing a hardcoded
expected vector, or comparing results generated across separate processes,
would fail unpredictably. `hashlib.md5` (or any `hashlib` function) has no such
randomization -- always prefer it for anything requiring stable, reproducible
hashing.

## `zip()` truncating silently on mismatched embedding dimensions

`cosine_similarity`'s `zip(a, b, strict=True)` will raise `ValueError` if `a`
and `b` have different lengths -- which is exactly what you want, since
comparing embeddings of different dimensionality is meaningless (Module 01,
lesson 04's "don't compare embeddings from different models" point). Without
`strict=True`, `zip` silently truncates to the shorter vector and returns a
plausible-looking (wrong) number instead of raising. This is the same
`zip`-safety point flagged in Module 02's pitfalls -- it keeps showing up
because it's a genuinely easy mistake with a genuinely silent failure mode.

## A `search_documents` tool that returns nothing useful for an empty result set

If `hybrid_search` returns an empty list (no chunks scored above whatever
implicit threshold, or an empty index) and `dispatch` joins that into an empty
string `ToolResult`, the model sees a blank tool result and has no signal about
*why* -- was the search broken, or is there genuinely no relevant information?
The solution's `dispatch` explicitly returns `"No relevant passages found."` in
this case, giving the model something actionable to reason about (try a
different query, or tell the user the information isn't available) instead of
an ambiguous blank.

## Chunk boundaries that cut through the exact fact a test query needs

If a test query's expected answer happens to be split across two chunks by an
unlucky chunk-size choice, `hybrid_search` may retrieve chunks that each
contain only *half* the needed fact, and neither individually scores well
against the query. This isn't a bug in your ranking code -- it's the chunking
trade-off from lesson 01 showing up directly. If a lab test seems to be failing
for no clear reason, check whether the expected keyword or concept is actually
intact within a single chunk for your chosen `chunk_size`/`overlap`, not split
across two.
