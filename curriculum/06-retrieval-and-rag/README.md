# Module 06 -- Retrieval & agentic RAG

**Difficulty:** ★★★★☆ · **Time estimate:** 6-8 hours

## Objectives

By the end of this module you can:

- Chunk documents sensibly for retrieval.
- Explain embeddings-based (semantic) search, keyword (lexical) search, and why hybrid search combines them.
- Implement a reranking step and explain what it fixes that similarity search alone doesn't.
- Explain the difference between naive RAG (always retrieve, then answer) and agentic RAG (the model decides when and what to retrieve), and build the latter.

## Prerequisites

[Module 05 -- Context engineering](../05-context-engineering/README.md) and Module 01, lesson 04 (Embeddings).

## Why this module exists

An agent's own training data goes stale and can't cover private/current
information. Retrieval-augmented generation (RAG) is how you ground an agent's
answers in real, current, specific documents instead of relying purely on
parametric memory (Module 01, lesson 05's discussion of hallucination is the
direct motivation here). This module builds retrieval from first principles --
chunking, embedding, ranking -- then makes it *agentic*: giving the model a
search tool it decides how and when to use, using everything from Module 03's
tool-calling loop.

## Contents

- [`lessons/01-chunking-and-embeddings.md`](lessons/01-chunking-and-embeddings.md)
- [`lessons/02-hybrid-search-and-ranking.md`](lessons/02-hybrid-search-and-ranking.md)
- [`lessons/03-agentic-rag.md`](lessons/03-agentic-rag.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed -- a deterministic fake embedding function stands in for a real one)
- [`labs/01-agentic-rag/`](labs/01-agentic-rag/) -- agentic RAG over a small bundled document set
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 07 -- Memory & state](../07-memory-and-state/README.md) (Level 2 begins)

Before moving on, also see [`projects/`](../../projects/README.md) for the
"research assistant with citations" project, which builds on this module.
