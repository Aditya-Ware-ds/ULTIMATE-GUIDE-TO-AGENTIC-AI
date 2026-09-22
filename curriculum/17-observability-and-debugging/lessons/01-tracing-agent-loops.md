# Tracing agent loops

**Last verified:** 2026-09-22 (span schema verified in `shared/tracing/tracer.py` against [OpenTelemetry's GenAI observability blog](https://opentelemetry.io/blog/2026/genai-observability/))
**Difficulty:** ★★★★☆ · **Time:** ~45 minutes

## Learning objectives

- Wrap an agent loop's model calls and tool calls in `shared/tracing/`'s span context managers.
- Explain why spans need to nest (an `invoke_agent` span containing `chat` and `execute_tool` children), not just exist as a flat list.
- Record real, useful attributes on each span (token usage, tool names) as the run actually happens.

## Intuition

Every agent loop in this curriculum (Module 04's ReAct loop, most directly)
runs a specific, real sequence of model calls and tool calls -- but once
it's done, that sequence is gone unless something recorded it as it
happened. Tracing is that recording: a span for the whole run, with nested
spans for each step inside it, so afterward you can see exactly what
happened, in what order, and how long each piece took.

## The concept

### Wrapping Module 04's loop with spans

```python
from shared.tracing import chat_span, execute_tool_span, invoke_agent_span


async def run_traced_agent(client, user_input: str, max_steps: int = 6) -> str:
    messages = [
        Message(role=Role.SYSTEM, content=_SYSTEM_PROMPT),
        Message(role=Role.USER, content=user_input),
    ]
    with invoke_agent_span("react-agent", **{"gen_ai.request.max_steps": max_steps}):
        for _ in range(max_steps):
            with chat_span(model=client.default_model, provider="mock") as span:
                response = await client.complete(messages, tools=TOOLS)
                span.set_attribute("gen_ai.usage.input_tokens", response.usage.input_tokens)
                span.set_attribute("gen_ai.usage.output_tokens", response.usage.output_tokens)
            if not response.message.tool_calls:
                return response.message.content or ""
            messages.append(response.message)
            for tool_call in response.message.tool_calls:
                with execute_tool_span(tool_call.name):
                    result = dispatch(tool_call, TOOL_REGISTRY)
                messages.append(Message(role=Role.TOOL, tool_result=result))
    return f"Stopped after {max_steps} steps without reaching a final answer."
```

Notice the loop's *logic* is completely unchanged from Module 04 -- tracing
adds spans around existing operations, it never changes what the agent
actually does. This is deliberate: instrumentation that changes behavior is
instrumentation you can't trust.

### Why nesting matters, not just a flat list of events

`shared/tracing/`'s span context managers use OpenTelemetry's own parent-
span tracking (`start_as_current_span`, verified in
`shared/tests/test_tracing.py`'s
`test_chat_span_nested_inside_invoke_agent_span`), so every `chat_span`
opened while an `invoke_agent_span` is active automatically becomes its
child. This is what makes a trace *replayable* as a coherent run (lesson
02) rather than a bag of unordered events you'd have to manually stitch
back together by timestamp alone.

### Recording attributes as the run happens, not after

`span.set_attribute(...)` is called *inside* the `with` block, once the
actual response is known -- token usage isn't available until after
`client.complete()` returns, so it can't be passed as a keyword argument to
`chat_span()` itself (which only has the model name and provider at the
moment the span opens). This ordering -- open the span, do the real work,
record what you learned -- is the general pattern for instrumenting any
operation whose interesting details only become known partway through.

## Deeper: instrumentation should be structural, applied once, not scattered

Notice `run_traced_agent` is a distinct function from Module 04's
`run_react_agent`, not the same function with tracing calls sprinkled
through it conditionally. Keeping tracing as a clean wrapper (or, in a real
production system, an actual middleware/decorator layer) around the same
core logic keeps the agent's actual decision-making code readable and keeps
tracing consistent across every call site, rather than each caller
remembering to add spans by hand.

## When not to use this

Don't trace a tiny, one-off script or a lab meant only for local
experimentation -- tracing infrastructure earns its complexity for agents
running repeatedly, in production, or anywhere a later "what actually
happened in that run" question is likely to come up.

## Common mistakes

- Recording token usage or other response-derived attributes as arguments
  to the span context manager's opening call, before the response actually
  exists -- attributes that depend on the operation's outcome must be set
  with `span.set_attribute(...)` inside the `with` block.
- Adding tracing calls that change control flow (e.g. a try/except around a
  span that swallows an exception the original code would have raised) --
  instrumentation should observe, never alter, behavior.
- Tracing only the top-level `invoke_agent` span and skipping the nested
  `chat`/`execute_tool` spans -- this gives you "an agent ran" with none of
  the step-by-step detail that makes tracing useful for debugging at all.

## Key takeaways

- Wrap Module 04's exact loop logic in span context managers -- tracing adds visibility, it never changes behavior.
- Spans need to nest (invoke_agent containing chat/execute_tool children) to reconstruct a coherent run, not just a flat event list.
- Set outcome-dependent attributes (token usage) inside the span's `with` block, once the real value is known.

## Lab

[`labs/01-traced-react-agent/`](../labs/01-traced-react-agent/README.md)
