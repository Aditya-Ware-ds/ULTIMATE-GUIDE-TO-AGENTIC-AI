# Async/await

**Difficulty:** ★★☆☆☆ · **Time:** ~1 hour

## Learning objectives

- Explain why LLM client code in this repo is `async` almost everywhere.
- Write and run basic `async def` functions with `asyncio`.
- Know the difference between concurrency (async) and parallelism (multiprocessing) well enough to not confuse them.

## Intuition

An LLM API call spends almost all of its time *waiting* -- for the network round
trip, for the model to generate tokens. While one call is waiting, your program
could be doing something else: making another API call, handling another user's
request, running a tool. `async`/`await` is Python's way of writing code that says
"start this, and let something else run while we wait for it to finish," all on a
single thread.

This matters enormously for agents: a multi-agent system (Module 12) or an agent
juggling several tool calls (Module 08's parallelization pattern) is fundamentally
about running several waiting-on-I/O operations at once. `shared/llm/base.py`'s
`LLMProvider` interface is `async` for exactly this reason.

## The concept

### The minimum you need

```python
import asyncio


async def say_after(delay: float, message: str) -> None:
    await asyncio.sleep(delay)
    print(message)


async def main() -> None:
    await say_after(1, "hello")
    await say_after(1, "world")
    # ^ this takes ~2 seconds total: each await fully waits before the next starts


asyncio.run(main())
```

- `async def` marks a function as a **coroutine function** -- calling it doesn't
  run the body, it returns a coroutine object.
- `await` runs that coroutine and suspends the current function until it
  completes, *without blocking the whole program* -- other coroutines can run
  during the wait.
- `asyncio.run(...)` is the entry point that actually starts the event loop and
  runs a top-level coroutine to completion. You call this once, at the top of
  your program.

### Running things concurrently

```python
async def main() -> None:
    await asyncio.gather(
        say_after(1, "hello"),
        say_after(1, "world"),
    )
    # ^ this takes ~1 second total: both run concurrently
```

`asyncio.gather()` runs multiple coroutines concurrently and waits for all of
them. This is exactly the shape Module 08's "parallelization" pattern and
Module 12's multi-agent systems use to fan out several LLM calls at once instead
of one after another.

### Async iteration (streaming)

```python
async def stream_words(words: list[str]):
    for word in words:
        await asyncio.sleep(0.1)
        yield word


async def main() -> None:
    async for word in stream_words(["hello", "world"]):
        print(word)
```

`async for` consumes an **async generator** -- this is exactly the shape
`shared/llm/base.py`'s `stream()` method uses, and what you'll consume when
displaying an agent's response token-by-token.

## Deeper: concurrency vs. parallelism

`asyncio` gives you **concurrency** (interleaving waiting tasks on one thread), not
**parallelism** (running CPU-bound work simultaneously on multiple cores). Async
is the right tool for "waiting on a lot of network calls" (LLM APIs, HTTP tools).
It does *not* speed up CPU-heavy work like parsing a huge file or running a local
ML model -- for that, you'd reach for `multiprocessing` or a separate process,
which is out of scope for this repo but worth knowing the boundary exists.

## When not to use this

Don't make a function `async` just because you can -- if it does no I/O (no
network, no `asyncio.sleep`, no awaiting another coroutine), making it async adds
ceremony (callers now need `await` and an event loop) for zero benefit. Plain
synchronous functions are correct and simpler for pure computation.

## Common mistakes

- **Forgetting `await`.** `result = my_async_func()` gives you a coroutine object,
  not the result -- and Python won't error until/unless you try to use `result` in
  a way that reveals it's not what you expected. If you see `<coroutine object ...
  was never awaited>` in a warning, this is the bug.
- **Calling `asyncio.run()` more than once, or from inside already-async code.**
  There can be only one running event loop per thread; `asyncio.run()` is for the
  top level of your program, not for nesting.
- **Blocking calls inside async code.** Calling a synchronous, slow function (like
  `time.sleep()` instead of `asyncio.sleep()`, or a non-async HTTP library) inside
  an `async def` blocks the *entire* event loop, defeating the purpose -- nothing
  else can run while it's blocked. Always use async-native libraries (`httpx.AsyncClient`,
  not `requests`) inside async code.

## Key takeaways

- `async`/`await` gives you concurrency for I/O-bound work (network calls) on a single thread.
- `asyncio.gather()` runs multiple coroutines concurrently; sequential `await`s run one after another.
- Async is for waiting, not for speeding up CPU-bound computation -- know the difference.

## Lab

[`labs/01-async-fetch-cli/`](../labs/01-async-fetch-cli/README.md)
