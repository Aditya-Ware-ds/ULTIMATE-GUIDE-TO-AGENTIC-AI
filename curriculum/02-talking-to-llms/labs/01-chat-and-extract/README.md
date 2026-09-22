# Lab 02.01 -- Chat loop, structured extraction, and cost estimation

**Difficulty:** ★★★☆☆ · **Time:** ~2 hours

## Task

Build four small, independent functions on top of `shared.llm` (this repo's
provider-agnostic client from Phase 0) -- one for each of this module's core
ideas: message-array construction, streaming, structured output validation, and
cost estimation. All tests run against `shared.llm.get_client("mock")` -- no API
key needed.

## Files

- `starter/chat.py` -- skeleton with four functions to implement
- `solution/chat.py` -- complete reference implementation
- `tests/` -- tests that exercise both

## Requirements

Implement these functions in `starter/chat.py`:

- `def build_messages(system_prompt: str, history: list[tuple[str, str]]) -> list[Message]`
  -- `history` is a list of `(role, content)` pairs where `role` is `"user"` or
  `"assistant"`. Return `[Message(role=Role.SYSTEM, content=system_prompt)]`
  followed by one `Message` per history entry, in order.

- `async def chat_once(client: LLMClient, system_prompt: str, history: list[tuple[str, str]], user_input: str) -> str`
  -- append `("user", user_input)` to `history`, build messages with
  `build_messages`, call `client.complete(...)`, append
  `("assistant", <reply text>)` to `history`, and return the reply text.
  `history` must end up containing the new turn either way (even if you build it
  differently internally) -- the point is history grows correctly across calls.

- `async def extract_structured(client: LLMClient, text: str, schema: dict) -> dict`
  -- send `text` as a single user message asking the model to extract structured
  data, with `response_schema=schema`. Parse the response as JSON and validate it
  against `schema` with `jsonschema.validate`. Let `json.JSONDecodeError` and
  `jsonschema.ValidationError` propagate -- don't catch them here.

- `async def stream_and_collect(client: LLMClient, messages: list[Message]) -> str`
  -- consume `client.stream(messages)` and return the fully concatenated text
  (ignore any `tool_call` chunks for this lab).

- `def estimate_call_cost(provider: str, usage: Usage) -> float` -- return
  `estimate_cost(provider, usage.input_tokens, usage.output_tokens)` from
  `shared.llm.pricing` (a one-line wrapper -- the point is knowing where to find it).

## Acceptance criteria

- All tests in `tests/` pass against your `starter/chat.py`.
- `chat_once` correctly grows `history` across multiple calls (test this
  yourself by calling it twice in a row and checking the model saw the full
  prior turn on the second call).
- `extract_structured` raises (doesn't swallow) `json.JSONDecodeError` on
  unparsable output and `jsonschema.ValidationError` on schema-violating output.
- `stream_and_collect` returns the same text a non-streamed `complete()` call
  against the same scripted response would return.

## Hints

- `MockLLMProvider.calls` (a list, on `client.provider`) records every call it
  received -- useful for asserting what messages `chat_once` actually sent on
  its second call.
- For `extract_structured`, a simple instruction like
  `f"Extract structured data as JSON from: {text}"` as the user message is
  enough -- the mock provider doesn't care what you ask, it just returns what
  you scripted.

## Running the tests

```bash
uv run pytest curriculum/02-talking-to-llms/labs/01-chat-and-extract/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/02-talking-to-llms/labs/01-chat-and-extract/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 03 -- Tool use / function calling](../../../03-tool-use/README.md)
