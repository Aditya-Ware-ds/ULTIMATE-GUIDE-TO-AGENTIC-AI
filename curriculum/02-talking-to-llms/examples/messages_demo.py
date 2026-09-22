"""Run: uv run python curriculum/02-talking-to-llms/examples/messages_demo.py

Shows a multi-turn conversation built as a growing Message list against the
mock provider -- no API key needed. See lessons/01-messages-and-roles.md.
"""

from __future__ import annotations

import asyncio

from shared.llm import Message, Role, get_client


async def main() -> None:
    client = get_client("mock")
    client.provider.add_text("4")
    client.provider.add_text("40")

    messages = [Message(role=Role.SYSTEM, content="Be extremely concise.")]

    messages.append(Message(role=Role.USER, content="What's 2+2?"))
    response = await client.complete(messages)
    print("Q: What's 2+2?  A:", response.message.content)
    messages.append(Message(role=Role.ASSISTANT, content=response.message.content))

    messages.append(Message(role=Role.USER, content="And that times 10?"))
    response = await client.complete(messages)
    print("Q: And that times 10?  A:", response.message.content)

    print(f"\nFinal conversation has {len(messages)} messages (including system).")


if __name__ == "__main__":
    asyncio.run(main())
