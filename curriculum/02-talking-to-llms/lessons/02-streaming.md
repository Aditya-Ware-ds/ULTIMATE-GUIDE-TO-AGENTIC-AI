# Streaming

**Last verified:** 2026-09-22
**Difficulty:** ★★☆☆☆ · **Time:** ~30-45 minutes

## Learning objectives

- Explain why streaming exists and what problem it solves.
- Consume a streamed response correctly, including tool calls that arrive mid-stream.
- Know when streaming is worth the added code complexity and when it isn't.

## Intuition

Without streaming, you send a request and wait for the *entire* response to be
generated before you see anything -- for a long response from a reasoning model,
that could be tens of seconds of silence. Streaming sends the response back in
pieces as it's generated, so you can start showing output (or processing it)
immediately, the same way a person speaking gives you their first words before
their last.

## The concept

### Consuming a stream with this repo's client

```python
from shared.llm import Message, Role, get_client

client = get_client("mock")
client.provider.add_text("The answer is forty-two.")

messages = [Message(role=Role.USER, content="What's the answer?")]
full_text = ""
async for chunk in client.stream(messages):
    if chunk.delta:
        full_text += chunk.delta
        print(chunk.delta, end="", flush=True)
    if chunk.tool_call:
        print(f"\n[tool call: {chunk.tool_call.name}]")
    if chunk.done:
        break
print()
```

`shared/llm/types.py`'s `StreamChunk` has three things you check on each chunk:
`delta` (a piece of text, possibly empty), `tool_call` (set if this chunk carries
a completed tool call), and `done` (set on the final chunk). Every provider
adapter in `shared/llm/providers/` translates its own streaming wire format
(Server-Sent Events, in most current implementations) into this same shape.

### Why tool calls complicate streaming

Text streams naturally token-by-token. A tool call is a structured object (name +
arguments) that doesn't make sense to show partially -- you generally can't act on
half a JSON arguments object. So streaming APIs either withhold a tool call until
it's fully formed (most common) or stream its arguments as a raw JSON string
fragment you must buffer and parse only once complete. This repo's `StreamChunk`
models the common case: a `tool_call` field that's only populated once the call is
complete.

## Deeper: streaming doesn't reduce total latency or cost

Streaming improves *perceived* latency (time to first visible output) and
enables progressive UIs, but the model still has to generate every token, so
total time-to-completion and total token cost are the same as a non-streamed
call. Streaming is a UX and pipelining improvement, not a performance
optimization in the "faster overall" sense.

## When not to use this

Don't stream when you need the complete response before doing anything useful
with it anyway -- e.g. an agent step that must parse a full JSON tool-call result
before acting has no benefit from streaming that step; buffering the complete
response and calling `complete()` is simpler code for the same outcome. Streaming
earns its complexity for user-facing text output and for pipelines that can act
on partial results (e.g. a UI rendering markdown as it arrives).

## Common mistakes

- Trying to `json.loads()` a partial JSON string as it streams in, assuming each
  chunk is independently parseable -- it isn't; wait for the full stream (or a
  `done`/complete-tool-call signal) before parsing.
- Forgetting to handle the case where `chunk.delta` is empty but the chunk isn't
  `done` (e.g. a chunk that only carries a `tool_call`) -- naive code that always
  appends `chunk.delta` to a running string is fine here since empty string
  concatenation is a no-op, but code that assumes every chunk has *some* text
  will break.
- Not handling a dropped/interrupted connection mid-stream in production code --
  a partial response with no clean `done` signal needs explicit handling (retry,
  or surface a clear error), not silent truncation.

## Key takeaways

- Streaming sends response pieces as they're generated, improving perceived latency, not total cost or total generation time.
- This repo's `StreamChunk` (`delta`, `tool_call`, `done`) is the same shape across every provider adapter.
- Tool calls generally arrive as complete objects, not incrementally parseable fragments -- buffer before acting.

## Lab

[`labs/01-chat-and-extract/`](../labs/01-chat-and-extract/README.md)
