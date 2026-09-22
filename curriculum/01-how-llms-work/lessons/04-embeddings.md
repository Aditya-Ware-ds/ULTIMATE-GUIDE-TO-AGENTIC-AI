# Embeddings

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45 minutes

## Learning objectives

- Explain what an embedding is and why "similar meaning -> nearby vectors" is the whole point.
- Compute cosine similarity between vectors by hand.
- Know why embeddings are the foundation of Module 06's retrieval/RAG systems.

## Intuition

An embedding is a list of numbers (a vector) that represents a piece of text's
*meaning* in a way that supports geometric comparison: texts with similar meaning
produce vectors that are close together in that vector space, and unrelated texts
produce vectors that are far apart. This turns "are these two things similar?"
from a language problem into an arithmetic problem: compute a distance between
two lists of numbers.

## The concept

### From text to vector

```python
# Conceptually (using a real embeddings API):
vector_a = embed("The cat sat on the mat")  # e.g. 1536 numbers
vector_b = embed("A feline rested on the rug")  # e.g. 1536 numbers
vector_c = embed("Quarterly revenue increased 12%")  # e.g. 1536 numbers

# vector_a and vector_b should be close together (similar meaning)
# vector_c should be far from both (unrelated meaning)
```

An embedding model is trained so that semantic similarity in text corresponds to
geometric closeness in vector space. The exact numbers are opaque and not
individually meaningful -- what matters is relative distance between vectors.

### Measuring similarity: cosine similarity

```python
import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b, strict=True))
    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))
    return dot_product / (magnitude_a * magnitude_b)
```

Cosine similarity measures the angle between two vectors, ignoring their
magnitude -- it returns `1.0` for identical direction (maximally similar),
`0.0` for orthogonal (unrelated), and `-1.0` for opposite direction. It's the
standard similarity metric for text embeddings because it's insensitive to
vector length, which otherwise correlates with text length rather than meaning.

### Why this matters for RAG (Module 06)

Retrieval-augmented generation works by: embedding a corpus of documents once,
embedding an incoming query, and finding the documents whose embeddings are
closest (highest cosine similarity) to the query's embedding. This lesson's
`cosine_similarity` function *is* the core operation a vector database performs
at scale -- Module 06 just adds indexing structures to do it fast over millions
of vectors instead of a linear scan.

## Deeper: embeddings capture semantic similarity, not necessarily relevance

Two texts can be semantically similar (embedding-close) without one being a good
answer to the other as a *query* -- "What is the capital of France?" and "What is
the capital of Germany?" are embedding-close (same structure, same topic) but
neither answers the other. This is why real retrieval systems often combine
embedding similarity (semantic/"vector" search) with keyword-based search
(lexical/"sparse" search) -- Module 06's "hybrid search" -- rather than relying on
embeddings alone.

## When not to use this

Don't use embedding similarity for tasks that need exact or structural matching
(e.g. "does this text contain this exact phrase," "is this valid JSON") --
embeddings answer "how similar in meaning," not "is this exactly present."
Keyword/regex/parsing is the right tool for exact-match problems.

## Common mistakes

- Comparing embeddings from *different* embedding models directly -- each model
  defines its own vector space; a vector from model A and a vector from model B
  are not comparable even if they happen to have the same dimensionality.
- Using Euclidean distance when the embedding model's documentation recommends
  cosine similarity (or vice versa) -- check what the specific model was
  optimized/evaluated for; they can rank results differently.
- Assuming "most similar by embedding" always means "most useful as an answer" --
  see the deeper section above; this is exactly why reranking (Module 06) exists.

## Key takeaways

- Embeddings map text to vectors such that semantic similarity becomes geometric closeness.
- Cosine similarity is the standard metric: 1.0 = same direction, 0.0 = unrelated, -1.0 = opposite.
- Embedding similarity ≠ relevance -- real retrieval systems combine it with other signals (Module 06).

## Lab

[`labs/01-token-sampling-visualizer/`](../labs/01-token-sampling-visualizer/README.md)
