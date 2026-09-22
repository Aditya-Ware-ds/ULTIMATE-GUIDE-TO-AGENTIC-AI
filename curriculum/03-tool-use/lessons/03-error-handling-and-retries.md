# Error handling and retries

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45 minutes

## Learning objectives

- Explain why a tool failure should usually be reported back to the model, not raised as an exception that kills the loop.
- Distinguish errors the model can recover from versus errors that need to stop the loop entirely.
- Design a simple, bounded retry strategy for transient tool failures.

## Intuition

A person using a calculator who mistypes an expression doesn't give up -- they
see the error, fix their input, and try again. An agent should be able to do the
same thing: when a tool fails because of a *fixable* problem (bad arguments,
malformed input), the right move is usually to tell the model what went wrong
and let it try again with corrected arguments -- not to crash the whole agent
run over one bad call.

## The concept

### Reporting failure back to the model, not raising

```python
from shared.llm.types import ToolResult


def calculate(expression: str) -> float: ...  # can raise ValueError on bad input


def dispatch_calculate(tool_call) -> ToolResult:
    try:
        result = calculate(**tool_call.arguments)
        return ToolResult(tool_call_id=tool_call.id, content=str(result))
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        return ToolResult(
            tool_call_id=tool_call.id,
            content=f"Error: {exc}. Please provide a valid arithmetic expression.",
            is_error=True,
        )
```

Setting `is_error=True` and writing a message the model can act on (not just a
raw Python traceback) gives the model a real chance to recover -- it sees the
error as a tool result, understands what went wrong, and can retry with better
arguments in its next turn. This is fundamentally different from letting the
exception propagate out of your loop and crash the whole run.

### Which errors are recoverable, and which aren't

| Error type | Recoverable by the model? | What to do |
|---|---|---|
| Bad/malformed arguments | Usually yes | Return as `ToolResult(is_error=True)` with a clear message |
| Tool's target resource doesn't exist (e.g. unknown city) | Usually yes | Same -- let the model try a different value or tell the user |
| Transient failure (network timeout, rate limit) | Not by *reasoning*, but by *retrying* | Retry the tool call itself (with backoff) a bounded number of times before giving up |
| Programming bug in your tool code | No | Let it surface (log it, alert), don't paper over it as a normal tool error |
| Tool call to a name that doesn't exist in your registry | Only if it's a legitimate near-miss | Report clearly; investigate if it happens often (may mean your tool descriptions are ambiguous) |

### A simple bounded retry for transient failures

```python
import time


def call_with_retry(function, *args, max_attempts: int = 3, **kwargs):
    last_exception: Exception | None = None
    for attempt in range(max_attempts):
        try:
            return function(*args, **kwargs)
        except TransientError as exc:
            last_exception = exc
            time.sleep(2**attempt)  # exponential backoff: 1s, 2s, 4s
    raise last_exception
```

Retries belong around the *specific* operation that might transiently fail (a
network call inside a tool), with a small bounded attempt count and backoff --
not as a blanket "just try the whole agent loop again" strategy, which wastes
tokens re-doing work that already succeeded.

## Deeper: silent failure is worse than a loud one

A tool that catches every exception and returns a generic `"something went
wrong"` string, with no distinction between "you gave bad arguments" and "our
database is down," gives the model nothing useful to act on -- it can't tell
whether retrying with different arguments would help. Specific, actionable error
messages in `ToolResult.content` are what actually let a model self-correct;
vague ones just waste another round trip.

## When not to use this

Don't retry an error that resulted from a genuinely invalid request (e.g. the
model asked for weather in a city that doesn't exist) -- retrying with the exact
same arguments will fail the exact same way. Only retry for genuinely transient
conditions (network blips, rate limits); for everything else, report the error
back so the model (or the user) can correct course.

## Common mistakes

- Catching `Exception` broadly at the tool-dispatch layer (correct, per lesson
  02) but then *also* catching broadly and silently inside individual tool
  functions, hiding bugs from ever reaching the dispatch layer's error handling.
- Retrying indefinitely with no maximum attempt count -- a persistent failure
  becomes an infinite loop burning tokens and time instead of failing cleanly.
- Not distinguishing "the model should see this and adapt" errors from "this is
  a bug in my code" errors -- routing a genuine bug back to the model as if it
  were a normal recoverable tool failure just hides the bug from you.

## Key takeaways

- Report recoverable tool failures back to the model as a `ToolResult(is_error=True)` with an actionable message, instead of raising and crashing the loop.
- Distinguish model-recoverable errors (bad arguments) from retry-worthy transient errors (network blips) from real bugs (let those surface).
- Bound every retry loop with a maximum attempt count and backoff.

## Lab

[`labs/01-tool-calling-loop/`](../labs/01-tool-calling-loop/README.md)
