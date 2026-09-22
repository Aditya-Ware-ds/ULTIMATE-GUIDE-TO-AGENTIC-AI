# Module 06 quiz

**1. Why can't you usefully embed an entire long document as a single vector for retrieval?**

<details><summary>Answer</summary>

A single embedding has to represent everything in the text, diluting the
specific meaning of any one part. Chunking lets retrieval find the specific
passage relevant to a query, instead of only "this whole document is vaguely
related."

</details>

**2. What's the trade-off between smaller and larger chunks?**

<details><summary>Answer</summary>

Smaller chunks retrieve more precisely (each chunk is more likely to be
specifically about one thing) but there are more of them to search and less
surrounding context per chunk. Larger chunks keep more context together but
dilute each chunk's embedding across more topics, reducing precision.

</details>

**3. Why include overlap between consecutive chunks?**

<details><summary>Answer</summary>

Without overlap, information spanning a chunk boundary can be split with no
surrounding context in either piece, effectively making it unretrievable.
Overlap keeps boundary-spanning content coherent in at least one chunk.

</details>

**4. Give an example query where keyword (lexical) search would outperform embedding (semantic) search, and one where the reverse is true.**

<details><summary>Answer</summary>

Keyword search wins on exact identifiers (a specific error code, product SKU,
or name) that semantic similarity doesn't necessarily weight heavily. Semantic
search wins on paraphrases ("a big furry pet" matching a chunk about "dogs and
cats") with no shared words at all.

</details>

**5. What does a reranking step add on top of an initial retrieval pass?**

<details><summary>Answer</summary>

It re-scores a smaller, cheaply-retrieved candidate set using a more careful
comparison that looks at the query and each candidate together (rather than
comparing independently pre-computed vectors), catching relevance signals the
faster initial pass misses -- while keeping cost manageable by only doing this
expensive step on a small candidate set, not the whole corpus.

</details>

**6. Why shouldn't you rerank your entire corpus instead of a pre-retrieved candidate subset?**

<details><summary>Answer</summary>

Reranking is more expensive per item than initial retrieval. Applying it to
the whole corpus defeats the cost-saving point of the two-stage
retrieve-then-rerank pipeline.

</details>

**7. What's the difference between naive RAG and agentic RAG?**

<details><summary>Answer</summary>

Naive RAG is a fixed pipeline: retrieve once, then generate one answer.
Agentic RAG makes retrieval a tool the model can call zero, one, or several
times, with follow-up queries informed by what it already found, inside the
regular agent loop.

</details>

**8. Why does a `search_documents` tool's description need to explicitly say the model may call it again with a refined query?**

<details><summary>Answer</summary>

Without that explicit permission, many models default to treating one search
as sufficient, undermining the point of agentic (multi-step) retrieval --
Module 03's lesson on tool descriptions mattering as much as schemas applies
directly here.

</details>

**9. Is agentic RAG always better than naive RAG? Why or why not?**

<details><summary>Answer</summary>

No. Agentic RAG costs more (extra model calls per retrieval step) for the same
question. It's worth that cost specifically for multi-hop or exploratory
retrieval needs; for simple single-fact lookups, naive RAG is cheaper and
equally accurate.

</details>

**10. In this module's lab, why is `toy_embed` built with `hashlib.md5` instead of Python's built-in `hash()`?**

<details><summary>Answer</summary>

Python's built-in `hash()` for strings is randomized per process by default,
so the same text would embed to different vectors across separate runs,
breaking deterministic tests. `hashlib.md5` produces the same digest for the
same input every time, on any run.

</details>
