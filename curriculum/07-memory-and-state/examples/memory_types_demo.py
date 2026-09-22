"""Run: uv run python curriculum/07-memory-and-state/examples/memory_types_demo.py

Classifies a few example agent behaviors by memory type (short/long-term x
episodic/semantic). See lessons/01-memory-types.md. No API key needed.
"""

from __future__ import annotations

EXAMPLES = [
    ("The current back-and-forth in this chat", "short-term", "n/a (still live)"),
    ("A summary placeholder replacing old turns (Module 05)", "short-term", "n/a (still live)"),
    ("A document corpus used for RAG (Module 06)", "long-term", "semantic"),
    ("'This user prefers metric units' stored across sessions", "long-term", "semantic"),
    ("'On March 3rd this user asked about refunds' stored as a log entry", "long-term", "episodic"),
]


def main() -> None:
    print(f"{'Example':<65} {'Duration':<12} {'Type'}")
    print("-" * 95)
    for description, duration, memory_type in EXAMPLES:
        print(f"{description:<65} {duration:<12} {memory_type}")


if __name__ == "__main__":
    main()
