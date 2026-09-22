"""Run: uv run python curriculum/00-programming-prerequisites/examples/async_demo.py

Times sequential vs. concurrent awaits to make the asyncio.gather() speedup
concrete, as covered in lessons/04-async-await.md.
"""

from __future__ import annotations

import asyncio
import time


async def fetch_simulated(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} done"


async def sequential() -> float:
    start = time.perf_counter()
    for name in ("a", "b", "c"):
        await fetch_simulated(name, 0.2)
    return time.perf_counter() - start


async def concurrent() -> float:
    start = time.perf_counter()
    await asyncio.gather(*(fetch_simulated(name, 0.2) for name in ("a", "b", "c")))
    return time.perf_counter() - start


async def main() -> None:
    sequential_time = await sequential()
    concurrent_time = await concurrent()
    print(f"Sequential: {sequential_time:.2f}s (roughly 0.6s: 3 x 0.2s, one after another)")
    print(f"Concurrent: {concurrent_time:.2f}s (roughly 0.2s: all three overlap)")


if __name__ == "__main__":
    asyncio.run(main())
