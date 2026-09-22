"""Run: uv run python curriculum/07-memory-and-state/examples/memory_store_demo.py

A minimal external memory store: durable key-fact read/write to a JSON file.
See lessons/02-memory-stores.md. No API key needed.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path


def load_memory(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_memory(path: Path, memory: dict) -> None:
    path.write_text(json.dumps(memory, indent=2))


def remember_fact(path: Path, key: str, value: str) -> None:
    memory = load_memory(path)
    memory[key] = value
    save_memory(path, memory)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        memory_path = Path(tmp) / "memory.json"

        print("Before any writes:", load_memory(memory_path))

        remember_fact(memory_path, "preferred_units", "metric")
        remember_fact(memory_path, "preferred_language", "en")
        print("After two facts:", load_memory(memory_path))

        # Simulate a fresh process reading the same file later.
        fresh_read = load_memory(memory_path)
        print("Fresh read (simulating a new session):", fresh_read)


if __name__ == "__main__":
    main()
