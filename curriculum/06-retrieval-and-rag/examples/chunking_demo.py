"""Run: uv run python curriculum/06-retrieval-and-rag/examples/chunking_demo.py

Shows fixed-size chunking with overlap, and the effect of chunk size on chunk
count. See lessons/01-chunking-and-embeddings.md.
"""

from __future__ import annotations

SAMPLE_TEXT = (
    "Retrieval-augmented generation grounds an agent's answers in real documents. "
    "Chunking splits a document into retrievable pieces. Embeddings turn each "
    "chunk into a vector so similarity search can find relevant passages. "
    "Hybrid search combines embeddings with keyword matching. Reranking then "
    "re-scores the top candidates more carefully before the final answer."
)


def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def main() -> None:
    for chunk_size in (50, 100, 200):
        chunks = chunk_text(SAMPLE_TEXT, chunk_size=chunk_size, overlap=10)
        print(f"chunk_size={chunk_size}: {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            print(f"  [{i}] {chunk!r}")
        print()


if __name__ == "__main__":
    main()
