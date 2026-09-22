"""Run: uv run python curriculum/06-retrieval-and-rag/examples/hybrid_search_demo.py

Shows a query where keyword search wins (an exact code) and one where semantic
search wins (a paraphrase), then combines both into a hybrid score. See
lessons/02-hybrid-search-and-ranking.md. Uses a deterministic hash-based toy
embedding (not a real model) so this runs offline with no API key.
"""

from __future__ import annotations

import hashlib
import math
from collections import Counter

DOCUMENTS = [
    "Error code E-4021 indicates a failed database connection.",
    "The system experienced a network outage affecting connectivity.",
    "Restart the server to apply the new configuration.",
]


def toy_embed(text: str, dimensions: int = 64) -> list[float]:
    vector = [0.0] * dimensions
    text = text.lower()
    for trigram, count in Counter(text[i : i + 3] for i in range(len(text) - 2)).items():
        bucket = int(hashlib.md5(trigram.encode()).hexdigest(), 16) % dimensions
        vector[bucket] += count
    return vector


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    return dot / (mag_a * mag_b) if mag_a and mag_b else 0.0


def keyword_score(query: str, document: str) -> float:
    query_words = set(query.lower().split())
    doc_words = set(document.lower().split())
    return len(query_words & doc_words) / len(query_words) if query_words else 0.0


def hybrid_score(cosine_sim: float, keyword_sim: float, alpha: float = 0.5) -> float:
    return alpha * cosine_sim + (1 - alpha) * keyword_sim


def rank(query: str) -> None:
    query_vector = toy_embed(query)
    print(f"Query: {query!r}")
    for doc in DOCUMENTS:
        cosine_sim = cosine_similarity(query_vector, toy_embed(doc))
        keyword_sim = keyword_score(query, doc)
        combined = hybrid_score(cosine_sim, keyword_sim)
        print(f"  cosine={cosine_sim:.3f} keyword={keyword_sim:.3f} hybrid={combined:.3f}  {doc}")
    print()


def main() -> None:
    rank("E-4021")  # exact code -- keyword should help a lot here
    rank("connection problem")  # paraphrase -- semantic similarity carries more weight


if __name__ == "__main__":
    main()
