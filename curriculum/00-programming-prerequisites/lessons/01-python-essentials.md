# Python essentials for this repo

**Difficulty:** ★☆☆☆☆ · **Time:** ~1 hour if you already know some Python

## Learning objectives

- Read type-hinted Python and know why this repo uses hints everywhere.
- Use dataclasses to model structured data (you'll see this constantly in `shared/llm/types.py`).
- Use f-strings, context managers (`with`), and comprehensions comfortably.
- Know enough OOP (classes, inheritance, abstract methods) to read `shared/llm/base.py`.

## Intuition

Every agent you build in this repo passes structured data between functions:
messages, tool calls, responses. Python's type hints and dataclasses exist to make
that data's *shape* visible in the code itself, instead of only in your head or in
a comment that goes stale. Think of a type hint as a label on a box telling you
what's supposed to be inside -- Python won't stop you from putting the wrong thing
in, but your editor and `ruff`/`mypy`-style tools will flag it, and so will your
own eyes six months later.

## The concept

### Type hints

```python
def greet(name: str, times: int = 1) -> str:
    return ("Hello, " + name + "! ") * times
```

`name: str` and `times: int` are hints, not enforcement -- Python runs this exact
same code even if you pass `greet(42)`. The value is entirely for humans and
tooling. This repo hints everywhere because reading `shared/llm/client.py`'s
`get_client(provider: str | None = None, *, model: str | None = None) -> LLMClient`
tells you the whole contract without reading the body.

### Dataclasses

```python
from dataclasses import dataclass, field


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, object]
```

A `@dataclass` auto-generates `__init__`, `__repr__`, and `__eq__` from the field
list. Compare that to writing all three by hand for every message/response type an
agent needs -- `shared/llm/types.py` has eight of these; without dataclasses it'd
be 5x the code for the same information.

### Context managers

```python
with open("data.json") as f:
    data = f.read()
# file is guaranteed closed here, even if read() raised
```

`with` guarantees cleanup runs even on an exception. You'll write your own context
managers in Module 17 (tracing spans use exactly this pattern -- see
`shared/tracing/tracer.py`'s `@contextmanager`-decorated functions).

### Comprehensions

```python
tool_names = [tc.name for tc in message.tool_calls]
by_id = {tc.id: tc for tc in message.tool_calls}
```

Prefer these over manual `for` loops with `.append()` when building a list/dict
from an existing iterable -- it's shorter and, once you're used to reading it,
faster to parse than the loop version.

### Minimal class with an abstract method

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius**2
```

`shared/llm/base.py`'s `LLMProvider` is exactly this pattern: an abstract base
class that `MockLLMProvider`, `AnthropicProvider`, `OpenAIProvider`, and friends all
implement. You can't instantiate `LLMProvider` directly, and Python will refuse to
let a subclass skip an abstract method -- this is how the repo guarantees every
provider has the same shape.

## Deeper: why this repo hints so aggressively

Every lab in this curriculum is going to be read by someone other than its author
(you, reading `shared/` before you've written a line of your own code). Type hints
turn "what does this function expect?" from an archaeology exercise into a glance.
They cost a few extra characters per function signature and save far more time
reading.

## When not to use this

Don't over-engineer type hints for genuinely dynamic code (e.g. a function that
truly accepts anything and just logs it) -- `Any` exists for a reason, and forcing
a precise type onto something inherently untyped just adds noise. Don't reach for
a dataclass for a single throwaway pair of values where a plain tuple is clearer.

## Common mistakes

- Writing `def f(x: int):` and then passing a string anyway, expecting Python to
  stop you -- it won't. Hints need a checker (`mypy`, `pyright`, or your editor) to
  actually catch mismatches; this repo relies on `ruff` for style/lint, not type
  checking, so hints here are primarily for human readers.
- Mutable default arguments: `def f(items: list = []):` -- the same list object is
  reused across every call with no argument, which causes bugs that look like
  state leaking between unrelated calls. Use `field(default_factory=list)` in
  dataclasses, or `items: list | None = None` plus `items = items or []` in
  regular functions.
- Forgetting `from __future__ import annotations` (or Python 3.10+'s native
  support) when using `str | None` syntax on older Python -- this repo targets
  3.11+, so it's not an issue here, but you'll see the import at the top of most
  `shared/` files as an explicit habit.

## Key takeaways

- Type hints document contracts; dataclasses eliminate boilerplate for structured data.
- `with` guarantees cleanup; comprehensions are the idiomatic way to build lists/dicts from iterables.
- Abstract base classes are how this repo enforces "every provider has the same interface."

## Lab

[`labs/01-async-fetch-cli/`](../labs/01-async-fetch-cli/README.md)
