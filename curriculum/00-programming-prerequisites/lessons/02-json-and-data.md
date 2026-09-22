# JSON and data interchange

**Difficulty:** ★☆☆☆☆ · **Time:** ~30-45 minutes

## Learning objectives

- Read and write JSON confidently, including nested structures.
- Convert between JSON and Python objects with the `json` module.
- Explain why LLM tool schemas and structured outputs are built on JSON Schema specifically.

## Intuition

JSON is a text format for representing the same handful of shapes every
programming language has: numbers, strings, booleans, null, lists, and
key-value maps. It became the universal interchange format for web APIs (and
now LLM APIs) because nearly every language can parse and produce it with one
function call, and it's readable by a human without a spec in hand.

## The concept

### JSON's building blocks

```json
{
  "name": "get_weather",
  "description": "Get the current weather for a city",
  "parameters": {
    "type": "object",
    "properties": {
      "city": { "type": "string" },
      "unit": { "type": "string", "enum": ["celsius", "fahrenheit"] }
    },
    "required": ["city"]
  }
}
```

That's a real shape you'll write by hand in Module 03 -- it's a JSON Schema
describing a tool, the exact format every current LLM provider's function-calling
API expects (see `shared/llm/types.py`'s `ToolDefinition.parameters`).

### Python <-> JSON

```python
import json

data = {"city": "Paris", "temp_c": 18, "conditions": ["cloudy"]}
text = json.dumps(data)  # Python object -> JSON string
parsed = json.loads(text)  # JSON string -> Python object
assert parsed == data
```

`json.dumps(..., indent=2)` pretty-prints for readability; plain `json.dumps(data)`
is what you send over the wire.

### The type mapping to memorize

| JSON | Python |
|---|---|
| object `{}` | `dict` |
| array `[]` | `list` |
| string | `str` |
| number | `int` or `float` |
| `true`/`false` | `bool` |
| `null` | `None` |

## Deeper: why LLM APIs are JSON-native

When you call `client.messages.create(messages=[...], tools=[...])`, both the
request and response are JSON under the hood, and the SDK just wraps that in
Python objects for you. Structured outputs (Module 02) work by giving the model a
JSON Schema and asking it to produce output matching that schema -- which is
exactly the same schema format used to describe tools. Learning JSON Schema once
here pays off in three places later: tool definitions, structured outputs, and
MCP tool schemas (Module 10).

## When not to use this

JSON has no way to represent dates, sets, or custom objects natively -- you'll
often see dates as ISO-8601 strings (`"2026-09-22T00:00:00Z"`) by convention, not
because JSON has a date type. Don't try to `json.dumps()` an arbitrary Python
object (like a class instance) without first converting it to a dict -- it'll
raise `TypeError: Object of type X is not JSON serializable`.

## Common mistakes

- Trailing commas: `{"a": 1, "b": 2,}` is invalid JSON (unlike Python dicts, which
  tolerate a trailing comma). This trips people up constantly when hand-writing
  JSON or debugging a model's malformed tool-call output.
- Assuming a model's JSON output is always valid JSON. It usually is with modern
  structured-output features, but you should still wrap `json.loads()` in a
  `try/except json.JSONDecodeError` when parsing model output you don't fully
  control -- see how the labs in Module 03 handle this.
- Confusing `json.dumps()` (Python object → string) with `json.dump()` (Python
  object → file). The `s` suffix means "string."

## Key takeaways

- JSON has exactly six data shapes; Python's `json` module maps them 1:1 to native types.
- JSON Schema (a JSON document describing the *shape* other JSON must have) is the backbone of tool calling and structured outputs across every current LLM provider.
- Never trust external JSON (including from a model) without handling parse errors.

## Lab

[`labs/01-async-fetch-cli/`](../labs/01-async-fetch-cli/README.md)
