# Module 00 quiz

Answer each question yourself before expanding the answer.

**1. What does adding a type hint like `def f(x: int) -> str:` actually do at runtime?**

<details><summary>Answer</summary>

Nothing enforced -- Python doesn't check hints at runtime by default. They exist
for human readers and external tools (editors, type checkers). You can still call
`f("hello")` and Python won't stop you.

</details>

**2. Why does `@dataclass` matter for a class like `ToolCall(id, name, arguments)`?**

<details><summary>Answer</summary>

It auto-generates `__init__`, `__repr__`, and `__eq__` from the field list, so you
don't hand-write boilerplate for a class that's just structured data. Without it,
comparing two `ToolCall` instances with `==` would check object identity, not
field equality.

</details>

**3. What's wrong with `def add_item(item, items=[]):`?**

<details><summary>Answer</summary>

The default list is created once, when the function is defined, and reused across
every call that doesn't pass its own `items` -- so items accumulate across
unrelated calls. Use `items: list | None = None` and `items = items or []` inside
the function, or a dataclass's `field(default_factory=list)`.

</details>

**4. Why is `json.dumps({"a": 1,})` (trailing comma) fine in Python but the JSON text `{"a": 1,}` is invalid?**

<details><summary>Answer</summary>

`json.dumps()` takes a Python dict (where trailing commas are fine, that's a
Python syntax feature) and produces valid JSON text as output -- it wouldn't
produce a trailing comma itself. The invalid example is *already-written* JSON
text with a trailing comma, which the JSON spec doesn't allow (unlike Python
dict/list literals).

</details>

**5. An HTTP response comes back with status 429. What does that range (4xx) tell you before you even read the body?**

<details><summary>Answer</summary>

4xx means the *client's* request was the problem (as opposed to 5xx, a server-side
failure). Specifically 429 means "too many requests" -- you're being rate limited,
not that your data was wrong.

</details>

**6. What's the difference between `httpx.get(url)` and `await client.get(url)` inside an `async def`?**

<details><summary>Answer</summary>

`httpx.get(url)` is the synchronous, blocking API -- the whole thread waits.
`await client.get(url)` (with an `httpx.AsyncClient`) yields control back to the
event loop while waiting, so other coroutines can run concurrently. Both make the
same kind of HTTP request; the difference is entirely about whether your program
can do other things while waiting.

</details>

**7. Why does `asyncio.gather(fetch_a(), fetch_b())` finish faster than `await fetch_a(); await fetch_b()`?**

<details><summary>Answer</summary>

Sequential awaits fully wait for `fetch_a()` before even starting `fetch_b()`.
`asyncio.gather()` starts both immediately and lets them overlap while each is
waiting on I/O -- so the total time is closer to the *slower* of the two, not the
*sum* of both.

</details>

**8. What actually happens if you write `result = my_async_func()` and forget the `await`?**

<details><summary>Answer</summary>

`result` becomes a coroutine object, not the function's return value -- the
function body hasn't run yet. No error is raised at that line; the bug usually
surfaces later when you try to use `result` as if it were the real value, or
Python prints a `RuntimeWarning: coroutine '...' was never awaited` if it's
garbage collected unused.

</details>

**9. What does `uv sync` actually set up, and why don't you need to "activate" anything for this repo?**

<details><summary>Answer</summary>

It creates (or updates) a `.venv/` virtual environment and installs this repo's
dependencies into it, isolated from your system Python. You don't manually
activate it because `uv run <command>` automatically runs inside that
environment.

</details>

**10. Why is `git add .` risky compared to `git add <specific-file>`?**

<details><summary>Answer</summary>

`git add .` stages everything changed in the current directory tree, including
files you might not have meant to commit (a stray `.env` with real keys, a large
generated file). Checking `git status` first, or adding specific files, avoids
accidentally committing something sensitive or unwanted.

</details>
