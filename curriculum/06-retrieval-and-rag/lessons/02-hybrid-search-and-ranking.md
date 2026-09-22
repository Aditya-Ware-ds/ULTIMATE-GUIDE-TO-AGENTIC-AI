# Hybrid search and reranking

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~1 hour

## Learning objectives

- Explain what lexical (keyword) search catches that semantic (embedding) search misses, and vice versa.
- Combine both into a hybrid ranking.
- Explain what a reranking step adds on top of an initial retrieval pass.

## Intuition

Embedding similarity (Module 01, lesson 04) is good at matching *meaning* --
"a big furry pet" retrieves a chunk about "dogs and cats" even with zero shared
words. It's comparatively weak at matching *exact terms* -- a specific product
code, an exact name, a rare technical term -- because those often carry
disproportionate importance that a general-purpose embedding doesn't
necessarily preserve as heavily as a human would expect. Keyword (lexical)
search is the mirror image: exact-term matching is its strength, and it's blind
to synonyms and paraphrase. **Hybrid search** combines both, so each covers the
other's blind spot.

## The concept

### A simple keyword overlap score

```python
def keyword_score(query: str, chunk: str) -> float:
    query_words = set(query.lower().split())
    chunk_words = set(chunk.lower().split())
    if not query_words:
        return 0.0
    return len(query_words & chunk_words) / len(query_words)
```

This is a deliberately simple lexical score (fraction of query words present in
the chunk) -- real systems typically use a more sophisticated algorithm (BM25 is
the standard), but the *combination* pattern below is the same regardless of
which lexical scorer you use.

### Combining scores into a hybrid rank

```python
def hybrid_score(cosine_sim: float, keyword_sim: float, alpha: float = 0.5) -> float:
    return alpha * cosine_sim + (1 - alpha) * keyword_sim
```

`alpha` controls the balance -- higher weights semantic similarity more, lower
weights exact keyword matching more. There's no universal correct value; it's
worth tuning against your eval set (Module 16), and it can reasonably differ by
query type (a query with a specific product code probably wants more keyword
weight than a conceptual question).

### What reranking adds

Initial retrieval (whether embedding-only or hybrid) typically pulls a larger
candidate set (say, top 20) cheaply. A **reranker** is a separate, often more
expensive model that re-scores just those candidates more carefully -- looking
at the actual query-chunk pair together (rather than comparing independently
pre-computed vectors), which can capture relevance signals a fast initial pass
misses. The typical pipeline: **retrieve** a broad candidate set cheaply ->
**rerank** that smaller set more expensively -> **use** only the top few after
reranking. This two-stage design keeps cost manageable (rerank a small
candidate set, not the entire corpus) while improving final precision.

## Deeper: retrieval quality is measurable, not a matter of taste

Every choice in this lesson -- chunk size, `alpha`, whether to rerank, which
reranker -- is something you should measure against a real eval set of
(query, expected-relevant-chunk) pairs, not tune by eyeballing a handful of
examples. Module 16 covers building this kind of eval rigorously; the mental
model to carry from this lesson is that retrieval is a component with
measurable precision/recall, not a black box you configure once by feel.

## When not to use this

Don't add hybrid search or reranking complexity to a small, homogeneous
document set where plain embedding similarity already performs well (measured,
not assumed) -- added pipeline stages cost latency and complexity that should
be justified by a measured accuracy gain, not added preemptively.

## Common mistakes

- Using embedding-only search for a corpus full of exact identifiers (product
  SKUs, error codes, specific names) where lexical matching would catch cases
  semantic similarity alone misses.
- Reranking the *entire* corpus instead of a cheaply-retrieved candidate subset
  -- this defeats the cost-saving point of a two-stage pipeline.
- Picking a hybrid `alpha` once, by feel, and never revisiting it as your
  document set or query patterns change.

## Key takeaways

- Semantic (embedding) search catches meaning/paraphrase; lexical (keyword) search catches exact terms -- hybrid search combines both because they have complementary blind spots.
- Reranking re-scores a small, cheaply-retrieved candidate set with a more careful (and more expensive) comparison, rather than being applied to the whole corpus.
- Every retrieval design choice here is measurable against a real eval set (Module 16) -- tune deliberately, not by feel.

## Lab

[`labs/01-agentic-rag/`](../labs/01-agentic-rag/README.md)
