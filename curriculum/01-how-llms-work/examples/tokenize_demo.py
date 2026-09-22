"""Run: uv run python curriculum/01-how-llms-work/examples/tokenize_demo.py

Shows real BPE tokenization with tiktoken, and how token count diverges from
word count -- as covered in lessons/01-tokens-and-tokenizers.md. Requires network
access on first run only (tiktoken downloads and caches its encoding file).
"""

from __future__ import annotations

import tiktoken

SAMPLES = [
    "Building agents is fun!",
    "unbelievably",
    "def fetch_json(url: str) -> dict:",
    "supercalifragilisticexpialidocious",
]


def main() -> None:
    encoding = tiktoken.get_encoding("o200k_base")

    for text in SAMPLES:
        token_ids = encoding.encode(text)
        pieces = [encoding.decode([tid]) for tid in token_ids]
        word_count = len(text.split())
        print(f"text: {text!r}")
        print(f"  words: {word_count}, tokens: {len(token_ids)}")
        print(f"  pieces: {pieces}")
        print()


if __name__ == "__main__":
    main()
