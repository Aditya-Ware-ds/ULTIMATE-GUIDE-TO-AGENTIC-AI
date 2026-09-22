# Module 17 pitfalls

## Setting span attributes before the value they describe actually exists

It's tempting to write `chat_span(model=..., provider=..., **{"gen_ai.usage.input_tokens": 0})`
as a placeholder and "fill it in later" -- but a span's opening keyword
attributes are recorded immediately, at creation time, before the model
call has even happened. If you never actually call `span.set_attribute(...)`
after the real response comes back, the span permanently records a
meaningless placeholder value instead of the real usage, and nothing in the
test suite will catch this unless a test specifically asserts on the real
number (as this lab's `test_run_traced_agent_records_token_usage_on_chat_span`
does).

## Assuming span export order matches execution order

`get_exported_spans()` returns spans in the order the exporter received
them, which is normally close to execution order but isn't a documented
guarantee to build fragile logic on. `replay_trace`'s explicit
`sorted(spans, key=lambda s: s.start_time)` is what actually guarantees
chronological order -- relying on export order instead works by
coincidence today and can silently break later.

## Computing nesting depth with a hardcoded assumption instead of walking `parent`

It's tempting, for a simple single-agent loop, to assume "chat and
execute_tool spans are always exactly one level under invoke_agent" and
hardcode indentation accordingly. This breaks the moment the trace comes
from something with real nested structure -- Module 12's supervisor-worker
topology, where a worker's own spans are nested under the worker's
`invoke_agent` span, which is itself nested under the supervisor's. Always
compute depth by walking the actual `parent` chain (as this lab's
`replay_trace` does), so the same function works regardless of how deep or
shallow the actual topology is.

## Treating `clear_exported_spans()` as optional between tests

Because `shared/tracing/tracer.py`'s exporter is a module-level singleton
(not re-created per test), spans from one test remain in memory for the
next one unless explicitly cleared. This lab's `conftest.py` clears spans
in an `autouse` fixture specifically to prevent one test's spans from
leaking into and corrupting another's assertions -- removing that fixture
(or writing a new test file that forgets to reuse it) reintroduces
cross-test contamination that can produce confusing, order-dependent test
failures.
