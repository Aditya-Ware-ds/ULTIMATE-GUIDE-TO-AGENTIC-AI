# Tool schemas

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45-60 minutes

## Learning objectives

- Write a `ToolDefinition` (name, description, JSON Schema parameters) a model can use reliably.
- Explain why the *description* matters as much as the schema's structure.
- Recognize schema designs that cause models to pick the wrong tool or fill bad arguments.

## Intuition

A tool definition is the *only* information the model has about what a tool does
and how to call it -- it never sees your Python implementation. If the
description is vague or the schema is ambiguous, the model can only guess, and
it will guess wrong some fraction of the time. Writing a good tool schema is
closer to writing a clear API docstring for a colleague who can't ask you
questions than it is to writing type hints for a compiler.

## The concept

### The shape, in this repo's types

```python
from shared.llm.types import ToolDefinition

get_weather = ToolDefinition(
    name="get_weather",
    description=(
        "Get the current weather for a city. Use this whenever the user asks "
        "about weather, temperature, or conditions in a specific place."
    ),
    parameters={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name, e.g. 'Paris' or 'San Francisco'.",
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit. Defaults to celsius if omitted.",
            },
        },
        "required": ["city"],
    },
)
```

Every current provider's wire format for tools is a thin wrapper around exactly
this: a name, a natural-language description, and a JSON Schema for the
arguments. `shared/llm/providers/*.py` show each provider's exact wrapping.

### What makes a description good

- **Say *when* to use it, not just what it does.** "Get the weather for a city"
  is weaker than "...Use this whenever the user asks about weather, temperature,
  or conditions in a specific place" -- the second version helps the model
  disambiguate against similar-sounding tools.
- **Describe each parameter, including format expectations.** "City name, e.g.
  'Paris' or 'San Francisco'" tells the model what a valid value looks like far
  better than a bare `"type": "string"`.
- **State defaults explicitly in the description**, not just by omission -- "Defaults
  to celsius if omitted" removes ambiguity about what happens if the model skips
  an optional field.

### Naming tools so the model can tell them apart

If you have `get_weather` and `get_weather_forecast`, make the distinction
explicit in both names and descriptions ("current conditions" vs. "multi-day
forecast") -- models pick the more plausible-sounding tool when names are close,
and a subtle naming collision causes real, hard-to-debug wrong-tool-call bugs in
production.

## Deeper: schemas are a UX surface, not just validation

It's tempting to think of a tool's `parameters` schema purely as "what my code
will accept" -- but the model reads that schema too, and it shapes what
arguments the model attempts to produce. An overly permissive schema (e.g. a
freeform `"type": "string"` for something that's really a fixed set of options)
invites the model to invent values you didn't anticipate; a well-constrained
schema (an `enum`, a `pattern`, explicit `required` fields) narrows what the
model will try to produce in the first place, before your code even runs.

## When not to use this

Don't create a tool for something a good prompt already handles reliably (e.g. a
"summarize_text" tool when the model can just... summarize text directly in its
response). Tools exist for actions your code needs to actually perform (an API
call, a calculation needing precision, a database lookup) -- not as a workaround
for prompting.

## Common mistakes

- Vague descriptions ("Gets weather info") that leave the model guessing about
  scope, units, or when to call it versus a similar tool.
- Schemas with no `required` list, so the model can (and sometimes will) omit
  fields your code actually needs, causing a runtime error you could have
  prevented at the schema level.
- Tool names that differ only in a detail a model is likely to miss under time
  pressure (`send_email` vs. `send_email_draft`) -- if the distinction matters,
  make it impossible to miss in both the name and the description.

## Key takeaways

- A tool definition is name + description + JSON Schema -- it's the model's entire view of what the tool does.
- Descriptions should say *when* to use the tool and what valid parameter values look like, not just restate the name.
- Schema constraints (enums, required fields) shape what the model attempts to produce, before your code ever runs.

## Lab

[`labs/01-tool-calling-loop/`](../labs/01-tool-calling-loop/README.md)
