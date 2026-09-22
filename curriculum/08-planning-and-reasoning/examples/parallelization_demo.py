"""Run: uv run python curriculum/08-planning-and-reasoning/examples/parallelization_demo.py

Times sequential vs. concurrent handling of independent sub-questions. See
lessons/03-routing-and-parallelization.md. No API key needed -- uses the mock
provider with a simulated delay to make the timing difference visible.
"""

from __future__ import annotations

import asyncio
import time

from shared.llm import Message, Role, get_client


async def answer_with_delay(client, question: str, delay: float) -> str:
    await asyncio.sleep(delay)  # simulates real network/generation latency
    response = await client.complete([Message(role=Role.USER, content=question)])
    return response.message.content or ""


async def main() -> None:
    client = get_client("mock")
    questions = ["What's the capital of France?", "What's the capital of Japan?", "What's 2+2?"]
    for _ in questions:
        client.provider.add_text("(answer)")

    start = time.perf_counter()
    for q in questions:
        await answer_with_delay(client, q, delay=0.2)
    sequential_time = time.perf_counter() - start

    client2 = get_client("mock")
    for _ in questions:
        client2.provider.add_text("(answer)")

    start = time.perf_counter()
    await asyncio.gather(*(answer_with_delay(client2, q, delay=0.2) for q in questions))
    parallel_time = time.perf_counter() - start

    print(f"Sequential: {sequential_time:.2f}s for {len(questions)} independent questions")
    print(f"Parallel:   {parallel_time:.2f}s for the same {len(questions)} questions")


if __name__ == "__main__":
    asyncio.run(main())
