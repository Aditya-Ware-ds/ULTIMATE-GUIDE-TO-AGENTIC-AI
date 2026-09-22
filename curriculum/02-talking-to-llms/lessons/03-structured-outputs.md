# Structured outputs

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45-60 minutes

## Learning objectives

- Explain what structured outputs are and why they're more reliable than asking a model to "please respond in JSON."
- Request schema-conforming output using this repo's `shared.llm` client.
- Validate a model's output against a JSON Schema in code, not just by eyeballing it.

## Intuition

If you just tell a model "respond in JSON," it usually will -- but "usually" isn't
good enough for code that calls `json.loads()` on the result and crashes on
malformed output. **Structured outputs** is a provider feature that constrains
generation itself so the response is *guaranteed* to match a JSON Schema you
provide, not merely encouraged to.

## The concept

### The request shape (provider-agnostic, via this repo's client)

```python
from shared.llm import Message, Role, get_client

schema = {
    "type": "object",
    "properties": {
        "city": {"type": "string"},
        "country": {"type": "string"},
    },
    "required": ["city", "country"],
}

client = get_client("mock")
client.provider.add_text('{"city": "Paris", "country": "France"}')

messages = [Message(role=Role.USER, content="Extract the location: I live in Paris, France.")]
response = await client.complete(messages, response_schema=schema)
```

`shared/llm/base.py`'s `complete()` takes `response_schema: dict | None` as a
JSON Schema. Each real provider adapter translates it to that provider's own
current parameter (as of 2026-09-22: Anthropic's `output_config.format` --
GA, no beta header; OpenAI's Responses API `text.format` with `type:
"json_schema"`; Gemini's Interactions API `response_format`). `MockLLMProvider`
doesn't enforce the schema (it's a mock -- it just returns whatever you scripted),
which is exactly why you still validate the result yourself, shown next.

### Validating the result yourself

Even with a provider-enforced schema, defensive code validates before trusting
the shape -- provider guarantees can have edge cases, and your own tests (against
the mock, which doesn't enforce anything) need real validation to be meaningful:

```python
import json
import jsonschema

text = response.message.content or ""
data = json.loads(text)  # can raise json.JSONDecodeError
jsonschema.validate(data, schema)  # can raise jsonschema.ValidationError
```

This two-step pattern -- parse, then validate against the schema -- is what this
module's lab has you build as a reusable function.

## Deeper: structured outputs vs. tool calling for extraction

Anthropic's docs note that tool use and structured outputs are the same
underlying primitive from the model's point of view: "extract structured JSON"
can be implemented either as a native structured-output request, or as a forced
tool call where the tool's input schema *is* your desired JSON shape (a pattern
you'll also see in Module 03). Both are legitimate; native structured outputs are
usually simpler when you just want data extraction with no actual tool execution
involved.

## When not to use this

Don't use structured outputs to force a shape onto genuinely open-ended,
free-text tasks (a long explanation, creative writing) -- you'll get worse output
fighting the model's natural response shape for no benefit. Structured outputs
earn their keep specifically for extraction, classification, and any output your
code needs to parse programmatically.

## Common mistakes

- Skipping schema validation because "the provider guarantees the shape" -- still
  validate; a `required` field that's an empty string, or a schema mismatch from
  hand-editing your schema dict, won't be caught by structure alone.
- Writing an overly permissive schema (e.g. no `required` list, loose types) that
  technically validates almost anything, defeating the purpose.
- Forgetting that `MockLLMProvider` does not enforce your schema -- if a lab test
  passes against the mock, that only proves your *validation code* is correct,
  not that a real provider will always return conforming output (still worth
  testing live, behind the `live` marker, before shipping).

## Key takeaways

- Structured outputs constrain generation to match a JSON Schema, more reliable than prompting alone.
- `shared.llm`'s `response_schema` param is provider-agnostic; each adapter translates it to that provider's current API shape.
- Always validate parsed output against the schema in your own code -- don't rely on provider guarantees alone, and remember the mock provider enforces nothing.

## Lab

[`labs/01-chat-and-extract/`](../labs/01-chat-and-extract/README.md)
