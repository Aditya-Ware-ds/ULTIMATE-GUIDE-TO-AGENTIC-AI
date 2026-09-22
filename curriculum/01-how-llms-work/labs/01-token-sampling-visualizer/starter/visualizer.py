"""Lab 01.01: token & sampling visualizer. See ../README.md for the full spec.

Fill in the five functions below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/01-how-llms-work/labs/01-token-sampling-visualizer/tests
"""

from __future__ import annotations

import random

import tiktoken  # noqa: F401 -- used once you implement count_tokens/token_pieces below


def count_tokens(text: str, encoding_name: str = "o200k_base") -> int:
    """Return the number of tokens `text` encodes to.

    TODO: implement this.
    """
    raise NotImplementedError


def token_pieces(text: str, encoding_name: str = "o200k_base") -> list[str]:
    """Return the decoded string for each individual token in `text`, in order.

    TODO: implement this. Encode once, then decode each token ID individually.
    """
    raise NotImplementedError


def softmax(logits: list[float], temperature: float) -> list[float]:
    """Apply temperature scaling, then softmax. Raise ValueError if temperature <= 0.

    TODO: implement this. See lessons/03-sampling-and-decoding.md for the formula
    (subtract the max scaled logit before exponentiating, for numerical stability).
    """
    raise NotImplementedError


def sample_index(probabilities: list[float], rng: random.Random) -> int:
    """Weighted-random draw over `probabilities` using `rng`.

    TODO: implement this via a cumulative-sum walk against rng.random() -- do not
    use rng.choices().
    """
    raise NotImplementedError


def most_likely_index(probabilities: list[float]) -> int:
    """Return the index of the highest probability.

    TODO: implement this.
    """
    raise NotImplementedError
