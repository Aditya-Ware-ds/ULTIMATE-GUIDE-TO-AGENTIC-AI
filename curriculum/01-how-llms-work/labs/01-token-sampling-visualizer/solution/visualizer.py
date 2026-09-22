"""Lab 01.01: token & sampling visualizer -- reference solution. See ../README.md."""

from __future__ import annotations

import math
import random

import tiktoken


def count_tokens(text: str, encoding_name: str = "o200k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


def token_pieces(text: str, encoding_name: str = "o200k_base") -> list[str]:
    encoding = tiktoken.get_encoding(encoding_name)
    token_ids = encoding.encode(text)
    return [encoding.decode([token_id]) for token_id in token_ids]


def softmax(logits: list[float], temperature: float) -> list[float]:
    if temperature <= 0:
        raise ValueError(f"temperature must be > 0, got {temperature}")
    scaled = [logit / temperature for logit in logits]
    max_scaled = max(scaled)
    exps = [math.exp(s - max_scaled) for s in scaled]
    total = sum(exps)
    return [e / total for e in exps]


def sample_index(probabilities: list[float], rng: random.Random) -> int:
    target = rng.random()
    cumulative = 0.0
    for index, probability in enumerate(probabilities):
        cumulative += probability
        if target < cumulative:
            return index
    return len(probabilities) - 1  # floating-point fallback for the last bucket


def most_likely_index(probabilities: list[float]) -> int:
    return max(range(len(probabilities)), key=lambda i: probabilities[i])
