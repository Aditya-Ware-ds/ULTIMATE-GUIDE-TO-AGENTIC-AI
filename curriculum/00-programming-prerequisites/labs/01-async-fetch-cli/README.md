# Lab 00.01 -- Async fetch + JSON CLI

**Difficulty:** ★★☆☆☆ · **Time:** ~1-2 hours

## Task

Build a small command-line tool that:

1. Fetches JSON from a URL using an async `httpx.AsyncClient`.
2. Extracts a value from the JSON using a dot-separated field path (e.g.
   `"user.address.city"` pulls `data["user"]["address"]["city"]`).
3. Prints the extracted value, or a clear error message if the request failed or
   the field path doesn't exist.

This combines every Module 00 lesson: async/await (fetching), JSON (parsing and
walking nested data), HTTP (status codes and error handling), and Python
essentials (type hints, clean function boundaries).

## Files

- `starter/cli.py` -- skeleton with four functions to implement (see the TODOs)
- `solution/cli.py` -- complete reference implementation
- `tests/` -- tests that exercise both (see "Running the tests" below)

## Requirements

Implement these four functions in `starter/cli.py`:

- `async def fetch_json(client: httpx.AsyncClient, url: str) -> dict` -- GET the
  URL, raise for non-2xx status via `response.raise_for_status()`, return the
  parsed JSON body.
- `def extract_field(data: dict, field_path: str) -> object` -- walk `data`
  following each dot-separated part of `field_path`. Raise `KeyError` with a
  message naming the exact part that was missing if any step fails.
- `async def run(url: str, field_path: str) -> str` -- open an
  `httpx.AsyncClient` as a context manager, call `fetch_json`, call
  `extract_field`, return the result as a string (`str(value)`).
- `def main(argv: list[str] | None = None) -> int` -- parse `argv` as
  `[url, field_path]` (default to `sys.argv[1:]` if `argv` is `None`), run `run()`
  via `asyncio.run(...)`, print the result, and return `0`. On `httpx.HTTPStatusError`
  or `KeyError`, print `f"Error: {exc}"` to `sys.stderr` and return `1`.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/cli.py`.
- A successful fetch + extraction prints just the value and returns exit code 0.
- A 404 (or other error status) prints an error to stderr and returns exit code 1 -- it must not raise an uncaught exception.
- A missing field path prints an error to stderr and returns exit code 1.
- No hardcoded URLs or field paths in your implementation -- everything comes from arguments.

## Hints

- `field_path.split(".")` gives you the parts to walk.
- `response.raise_for_status()` raises `httpx.HTTPStatusError` for 4xx/5xx -- you
  don't need to check `status_code` manually.
- `main()` needs `try/except` around the `asyncio.run(run(...))` call, not inside `run()` itself -- keep `run()`'s exceptions un-caught so the tests can check them directly too.

## Running the tests

By default, tests run against `solution/` (this is what verifies the reference
solution actually works):

```bash
uv run pytest curriculum/00-programming-prerequisites/labs/01-async-fetch-cli/tests
```

To run the same tests against your own `starter/cli.py` as you work on it:

```bash
LAB_TARGET=starter uv run pytest curriculum/00-programming-prerequisites/labs/01-async-fetch-cli/tests
```

Don't look at `solution/cli.py` until your own implementation passes -- see
[HOW_TO_USE.md](../../../../HOW_TO_USE.md) for why.

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 01 -- How LLMs work](../../../01-how-llms-work/README.md)
