"""Run: uv run python curriculum/05-context-engineering/examples/compaction_demo.py

Shows a growing message history getting compacted once it crosses a token
budget, keeping the system prompt and recent turns intact. See
lessons/02-compaction-and-summarization.md.
"""

from __future__ import annotations

import tiktoken

from shared.llm.types import Message, Role

_ENCODING = tiktoken.get_encoding("o200k_base")


def count_tokens(messages: list[Message]) -> int:
    return sum(len(_ENCODING.encode(m.content or "")) for m in messages)


def compact_messages(
    messages: list[Message], max_tokens: int, keep_recent: int = 4
) -> list[Message]:
    if count_tokens(messages) <= max_tokens:
        return messages

    system_messages = [m for m in messages if m.role == Role.SYSTEM]
    rest = [m for m in messages if m.role != Role.SYSTEM]
    recent = rest[-keep_recent:]
    older = rest[:-keep_recent]
    if not older:
        return messages

    summary = Message(
        role=Role.USER,
        content=f"[{len(older)} earlier messages omitted to stay within the context budget.]",
    )
    return [*system_messages, summary, *recent]


def main() -> None:
    messages = [Message(role=Role.SYSTEM, content="Be concise.")]
    for i in range(20):
        messages.append(Message(role=Role.USER, content=f"This is message number {i}. " * 10))

    print(f"Before compaction: {len(messages)} messages, {count_tokens(messages)} tokens")

    compacted = compact_messages(messages, max_tokens=200, keep_recent=4)

    print(f"After compaction:  {len(compacted)} messages, {count_tokens(compacted)} tokens")
    print("\nCompacted messages:")
    for m in compacted:
        preview = (m.content or "")[:50]
        print(f"  [{m.role.value}] {preview}")


if __name__ == "__main__":
    main()
