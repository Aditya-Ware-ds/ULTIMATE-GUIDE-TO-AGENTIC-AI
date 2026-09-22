# Chunking and embeddings

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45-60 minutes

## Learning objectives

- Chunk a document sensibly for retrieval, and explain the trade-offs in chunk size.
- Explain what embedding a chunk buys you, building on Module 01, lesson 04.
- Know which current embedding models are reasonable defaults, and roughly what they cost.

## Intuition

You can't (usefully) embed an entire book as one vector -- a single embedding
has to represent everything in the text, and cramming an entire document into
one vector loses the specific, fine-grained meaning a query usually needs to
match against. **Chunking** splits documents into smaller, individually
embeddable pieces, so retrieval can find the *specific* passage that answers a
question, not just "this whole document is vaguely related."

## The concept

### A simple, fixed-size chunker

```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # overlap so a sentence split across chunks isn't lost entirely
    return chunks
```

`chunk_size` is in characters here for simplicity; real systems often chunk by
token count (Module 01, lesson 01) since that's what actually determines
retrieval and context cost. `overlap` between consecutive chunks reduces the
chance that a sentence spanning a chunk boundary loses its meaning by being cut
in half with no surrounding context in either piece.

### Chunk size trade-offs

- **Smaller chunks** -- more precise retrieval (a chunk is more likely to be
  *specifically* about one thing), but more chunks to search over, and less
  surrounding context in each chunk if the model needs nearby information to
  interpret it correctly.
- **Larger chunks** -- more context per chunk, fewer chunks total, but each
  chunk's embedding represents a blend of everything in it, diluting precision
  -- a chunk covering three different subtopics won't match a query about any
  one of them as sharply as a chunk that's *only* about that subtopic.
- There's no universally correct chunk size -- it depends on document structure
  (natural paragraph/section boundaries usually beat arbitrary fixed-length
  cuts when available) and is worth tuning against your actual eval set
  (Module 16), not guessing once and leaving it.

### Embedding chunks (building on Module 01, lesson 04)

```python
# Real usage shape (illustrative -- requires an API key, not run in this
# module's offline examples/lab, which use a deterministic fake embed function):
# response = client.embeddings.create(model="text-embedding-3-small", input=chunk_text)
# vector = response.data[0].embedding
```

Current reasonable default embedding models (verified 2026-09-22, see
resources.md): OpenAI's `text-embedding-3-small` and Voyage AI's
`voyage-4-lite`, both around $0.02 per million tokens -- cheap enough that
embedding a large document corpus once is rarely the expensive part of a RAG
system (repeated query-time LLM calls usually dominate cost). Higher-accuracy
options (Voyage 4, Gemini Embedding 2) cost more per token and are worth it
specifically when retrieval accuracy is the measured bottleneck (Module 16),
not by default.

## Deeper: chunking is a retrieval-quality decision, not just a storage detail

It's tempting to treat chunking as plumbing -- something you configure once and
forget. In practice, chunk boundaries directly determine what retrieval *can*
find: information split awkwardly across a chunk boundary, with too little
overlap to keep it coherent in either piece, may never be retrievable no matter
how good your embedding model or ranking is. Chunking quality is a ceiling on
everything downstream in this module.

## When not to use this

Don't over-engineer chunking for a small, static document set where you could
reasonably fit the whole thing in context directly (Module 05) -- RAG earns its
complexity for corpora too large to fit in a single context window, or that
change independently of any one conversation. If your "knowledge base" is three
short documents, just put them in the system prompt.

## Common mistakes

- Chunking purely by a fixed character/token count with zero regard for
  document structure (paragraph breaks, headers) when that structure is
  available -- splitting mid-sentence at a fixed boundary loses more than
  splitting at a natural paragraph break would.
- No overlap between chunks, causing information right at a boundary to be
  effectively lost to retrieval.
- Assuming a bigger/more expensive embedding model automatically improves your
  system -- measure retrieval quality (Module 16) before paying more per token
  for marginal or no improvement on your specific documents and queries.

## Key takeaways

- Chunking splits documents into retrievable, individually-embeddable pieces; chunk size trades retrieval precision against per-chunk context.
- Overlap between chunks protects against information loss at chunk boundaries.
- Embedding is usually cheap relative to per-query LLM calls -- don't over-optimize embedding cost at the expense of retrieval quality.

## Lab

[`labs/01-agentic-rag/`](../labs/01-agentic-rag/README.md)
