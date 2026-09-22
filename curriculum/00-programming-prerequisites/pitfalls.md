# Module 00 pitfalls

Mistakes that are easy to make even after your code passes -- read this even if
your lab tests are green.

## "It works on my machine" async bugs that tests don't always catch

If you write `run()` without `await`-ing `fetch_json()` properly (e.g. you call
`fetch_json(client, url)` and forget `await`, then pass the resulting coroutine
object straight to `extract_field`), you'll get a `TypeError` immediately, which
is loud and easy to catch. The sneakier version: calling a blocking, synchronous
function from inside an `async def` (e.g. `time.sleep()` instead of
`asyncio.sleep()`, or a synchronous HTTP call inside async code). It won't crash
-- it'll just silently block the entire event loop for that duration, which only
becomes visible when you run two things concurrently and notice they aren't
actually overlapping. The lab's `local_server` fixture is fast enough that this
particular bug wouldn't show up in the lab's timing, but it matters enormously
once you're juggling several real LLM calls in Module 08's parallelization
pattern.

## Catching exceptions in the wrong place

The lab's spec deliberately asks you to let `fetch_json` and `run` raise, and only
catch `httpx.HTTPStatusError`/`KeyError` inside `main()`. If you instead catch
exceptions inside `run()` and return `None` or an empty string on failure, your
tests for `run()` directly (`test_run_propagates_http_errors`) will fail, and
you'll have silently swallowed information `main()` needs to report a useful error
message. This mirrors a real agent-building pattern: low-level functions should
usually raise with a clear message; only the outermost layer (here, `main()`;
later, an agent's top-level loop) decides how to present a failure to the user.

## Field-path walking off a non-dict value

If `field_path` is `"user.name.first"` but `data["user"]["name"]` is a string, not
a dict, naively doing `value[part]` on a string will index it by character
(`"Ada"[0]` is `"A"`) instead of raising a clear error. `extract_field` needs to
check `isinstance(value, dict)` at each step before indexing further -- this is
exactly the kind of "technically doesn't crash, but silently does the wrong
thing" bug that's worse than a clean exception. Notice the solution's
`extract_field` checks `isinstance(value, dict)` before every `value[part]`.

## Treating "tests pass" as "done" for the wrong reason

The lab's tests use a local HTTP server on `127.0.0.1` with two known routes. That
proves your code handles those specific cases correctly -- it does not prove your
code would handle, say, a response body that isn't valid JSON at all (a
`json.JSONDecodeError` from `response.json()`), because the spec doesn't require
that yet. Knowing exactly what your tests do and don't cover is a habit worth
building now, before Module 16 makes "what does this eval actually measure"
a central topic.
