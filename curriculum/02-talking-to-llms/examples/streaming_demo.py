"""Run: uv run python curriculum/02-talking-to-llms/examples/streaming_demo.py

Consumes a streamed mock response chunk by chunk. See lessons/02-streaming.md.
"""

from __future__ import annotations

import asyncio

from shared.llm import Message, Role, get_client


async def main() -> None:
    client = get_client("mock")
    client.provider.add_text("Streaming shows output as it is generated.")

    messages = [Message(role=Role.USER, content="Explain streaming in one sentence.")]

    full_text = ""
    print("Streamed output: ", end="")
    async for chunk in client.stream(messages):
        if chunk.delta:
            full_text += chunk.delta
            print(chunk.delta, end="", flush=True)
        if chunk.done:
            print()
    print(f"Collected {len(full_text)} characters total.")


if __name__ == "__main__":
    asyncio.run(main())
