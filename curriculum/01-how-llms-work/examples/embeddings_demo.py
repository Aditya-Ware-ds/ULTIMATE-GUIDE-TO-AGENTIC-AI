"""Run: uv run python curriculum/01-how-llms-work/examples/embeddings_demo.py

Illustrates cosine similarity with a TOY embedding (character-trigram hashing),
not a real embedding model -- no API key needed, and this is for building
intuition about the cosine-similarity math only. Module 06 uses real embedding
models; see lessons/04-embeddings.md.
"""

from __future__ import annotations

import math
from collections import Counter


def toy_embed(text: str, dimensions: int = 64) -> list[float]:
    """A hashing-based bag-of-trigrams vector. Illustrative only -- real embedding
    models are trained neural networks, not a hash function.
    """
    vector = [0.0] * dimensions
    text = text.lower()
    trigrams = [text[i : i + 3] for i in range(len(text) - 2)]
    counts = Counter(trigrams)
    for trigram, count in counts.items():
        vector[hash(trigram) % dimensions] += count
    return vector


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b, strict=True))
    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def main() -> None:
    pairs = [
        ("The cat sat on the mat", "The cat sat on the rug"),
        ("The cat sat on the mat", "Quarterly revenue increased 12%"),
    ]
    for text_a, text_b in pairs:
        similarity = cosine_similarity(toy_embed(text_a), toy_embed(text_b))
        print(f"{text_a!r} vs. {text_b!r}\n  cosine similarity: {similarity:.3f}\n")


if __name__ == "__main__":
    main()
